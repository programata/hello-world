# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de ejecución del modelo para obtener sus predicciones para el dataset
# variable predictoras proporcionado por 'predictor_data'
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from typing import Any, Dict
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from analyticsbk.framework.logging.function_logger import logging_decor
from sklearn.preprocessing import LabelEncoder


@logging_decor()
def prepare_inference_data(
    inference_data: pd.DataFrame,
    parameters: Dict[str, Any]
):
    """ """
    inference_data = inference_data.drop("PassengerId", axis=1)
    inference_data = inference_data.drop("Name", axis=1)
    inference_data = inference_data.drop("Ticket", axis=1)
    inference_data = inference_data.drop("Cabin", axis=1)

    mean = inference_data["Age"].mean()
    inference_data["Embarked"] = inference_data["Embarked"].fillna('S')

    std = inference_data["Age"].std()
    is_null = inference_data["Age"].isnull().sum()
    # compute random numbers between the mean, std and is_null
    rand_age = np.random.randint(mean - std, mean + std, size=is_null)
    # fill NaN values in Age column with random values generated
    age_slice = inference_data["Age"].copy()
    age_slice[np.isnan(age_slice)] = rand_age
    inference_data["Age"] = age_slice
    inference_data["Age"] = inference_data["Age"].astype(int)
    inference_data['Fare'] = inference_data['Fare'].fillna(inference_data['Fare'].mean())

    le = LabelEncoder()
    inference_data["Sex"] = le.fit_transform(inference_data["Sex"])

    le = LabelEncoder()
    inference_data["Embarked"] = le.fit_transform(inference_data["Embarked"])

    sc = StandardScaler()
    return sc.fit_transform(inference_data)


@logging_decor()
def execute_model(
    raw_inference_data: pd.DataFrame,
    prepared_inference_data: pd.DataFrame,
    model: RandomForestClassifier,
    parameters: Dict[str, Any]
) -> pd.DataFrame:
    """ """
    y_pred = model.predict(prepared_inference_data)

    raw_data_with_predictions = raw_inference_data
    raw_data_with_predictions['Survived'] = y_pred

    return raw_data_with_predictions
