import os
import numpy as np
import pandas as pd
import xgboost as xgb

from typing import Tuple, Union, List

from .utils import get_min_diff
from .api import THRESHOLD_IN_MINUTES, DATA_PATH, MODEL_PATH

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
        self.is_loaded = False

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

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix = 'MES')], 
            axis = 1
        )
        features = features.reindex(columns=self.feature_cols, fill_value=0)
        if target_column:
            data['min_diff'] = data.apply(get_min_diff, axis = 1)
            data['delay'] = np.where(data['min_diff'] > THRESHOLD_IN_MINUTES, 1, 0)
            target = data.loc[:, [target_column]]
            return features, target
        return features

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
        self.is_loaded = True

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
        if not self.is_loaded:
            print("loading model...")
            self.load_model()
            print("loading model...ok")
        return self._model.predict(features).tolist()

    def save_model(self):
        self._model.save_model("0001.model")
    
    def load_model(self):
        if not os.path.exists("0001.model"):
            data = pd.read_csv(filepath_or_buffer=DATA_PATH)
            features, target = self.preprocess(data, "delay")
            self.fit(features, target)
            self.save_model()        
        else:
            self._model.load_model("0001.model")

if __name__ == "__main__":
    model = DelayModel()
    data_path = "../data/data.csv"
    data = pd.read_csv(filepath_or_buffer=data_path)
    features, target = model.preprocess(data, "delay")
    model.fit(features, target)
    model.save_model()    