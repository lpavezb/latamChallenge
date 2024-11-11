import numpy as np
import pandas as pd
import xgboost as xgb

from typing import Tuple, Union, List

from .utils import get_period_day, is_high_season, get_min_diff
from .api import THRESHOLD_IN_MINUTES

class DelayModel:

    def __init__(
        self
    ):
        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=4.4402380952380955) # Model should be saved in this attribute.
        self.feature_cols = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]
    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        data['period_day'] = data['Fecha-I'].apply(get_period_day)
        data['high_season'] = data['Fecha-I'].apply(is_high_season)
        data['min_diff'] = data.apply(get_min_diff, axis = 1)
        data['delay'] = np.where(data['min_diff'] > THRESHOLD_IN_MINUTES, 1, 0)

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix = 'MES')], 
            axis = 1
        )
        out_data = features[self.feature_cols]
        if target_column:
            target = data.loc[:, [target_column]]
            return out_data, target
        return out_data

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        self._model.fit(features, target)

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        return self._model.predict(features).tolist()

if __name__ == "__main__":
    DelayModel()