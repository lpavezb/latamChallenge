# **Part1**
### exploration.ipynb bugs ands fixes:
- sns.set is deprecated, replaced with sns.set_theme
- sns.barplot needs x and y arguments
- in the get_rate_from_column function, the rate is calculated as "total / delay[name]", when it should be "delay[name] / total" 

### Chosen model: XGBClassifier with Feature Importance and Balance

This decision was made because of the recall of class 1, beacuse we need to correctly identify the delays, and the models with best recall are XGBoost and LogisticRegression, both with Feature Importance and Balance. 

The difference between both models is minimal, so the final choice is preference.

### model.py
- the model class has a is_loaded variable in order to know if the model can use the predict function
- preprocess takes the values of OPERA, TIPOVUELO and MES to get the encoded one hot features, and after that it reindex the features to the top 10 necessary to the model.
- fit is the normal fit method of the sklearn models, but also changes the is_loaded class variable
- predict checks is_loaded, if not, then loads the model, else proceeds to predict with the provided features

# **Part2**
### api.py
- Using pydantic models is posible to define the request structure and verify it. Here the model checks that the request has a list of dictionaries, each with an OPERA and TIPOVUELO that exists, and MES between 1 and 12.

- The api loads the model and the predict endpoint uses it to predict the request, this way the model is loaded only one time.

# **Part3**
The api is deployed in GCP using the GCP console, the url is "https://api-service-546017129522.southamerica-west1.run.app"
The stress test runs without problem

# **Part4**
The ci.yaml runs on push of all flow branches, and runs the model-test and api-test
The cd is provided by a GCP trigger, it runs each time there is a push in the main branch  