# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de division en conjunto de entrenamiento y conjunto de prueba del
# dataset MNIST
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from typing import Dict
from analyticsbk.framework.logging.function_logger import logging_decor
import pandas as pd
import numpy as np


@logging_decor()
def split_train_test(
    raw_train_data_cleaned: pd.DataFrame,
) -> Dict[str, pd.DataFrame]:
    """"""

    # Una forma sencilla de dividir el dataset en train y test
    msk = np.random.rand(len(raw_train_data_cleaned)) < 0.8

    test_df = raw_train_data_cleaned[~msk]
    raw_train_data_cleaned = raw_train_data_cleaned[msk]

    return dict(
        X_train=raw_train_data_cleaned.drop("Survived", axis=1),
        y_train=raw_train_data_cleaned["Survived"],
        X_test=test_df.drop("Survived", axis=1),
        y_test=test_df["Survived"]
    )
