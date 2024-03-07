#
import pandas as pd
import numpy as np
from typing import Any, Dict
from analyticsbk.framework.logging.function_logger import logging_decor

from sklearn.preprocessing import LabelEncoder


@logging_decor()
def read_raw_data(
    raw_train_data: pd.DataFrame,
    raw_validation_data: pd.DataFrame,
    parameters: Dict[str, Any]
) -> dict:
    """"""
    raw_train_data = raw_train_data.drop("PassengerId", axis=1)
    raw_train_data = raw_train_data.drop("Name", axis=1)
    raw_train_data = raw_train_data.drop("Ticket", axis=1)
    raw_train_data = raw_train_data.drop("Cabin", axis=1)

    raw_validation_data = raw_validation_data.drop("PassengerId", axis=1)
    raw_validation_data = raw_validation_data.drop("Name", axis=1)
    raw_validation_data = raw_validation_data.drop("Ticket", axis=1)
    raw_validation_data = raw_validation_data.drop("Cabin", axis=1)

    return dict(train=raw_train_data, validation=raw_validation_data)


@logging_decor()
def clean_data(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    parameters: Dict[str, Any]
) -> dict:
    """"""

    data = [train, validation]

    for dataset in data:
        mean = train["Age"].mean()
        std = validation["Age"].std()
        is_null = dataset["Age"].isnull().sum()
        # compute random numbers between the mean, std and is_null
        rand_age = np.random.randint(mean - std, mean + std, size=is_null)
        # fill NaN values in Age column with random values generated
        age_slice = dataset["Age"].copy()
        age_slice[np.isnan(age_slice)] = rand_age
        dataset["Age"] = age_slice
        dataset["Age"] = train["Age"].astype(int)
        dataset['Fare'] = dataset['Fare'].fillna(dataset['Fare'].mean())

    common_value = 'S'
    train["Embarked"] = train["Embarked"].fillna(common_value)
    validation["Embarked"] = validation["Embarked"].fillna(common_value)

    le = LabelEncoder()
    train["Sex"] = le.fit_transform(train["Sex"])
    print(train["Sex"])

    le = LabelEncoder()
    train["Embarked"] = le.fit_transform(train["Embarked"])
    print(train["Embarked"])

    le = LabelEncoder()
    validation["Sex"] = le.fit_transform(validation["Sex"])
    print(validation["Sex"])

    le = LabelEncoder()
    validation["Embarked"] = le.fit_transform(validation["Embarked"])
    print(train["Embarked"])

    return dict(train=train, validation=validation)
