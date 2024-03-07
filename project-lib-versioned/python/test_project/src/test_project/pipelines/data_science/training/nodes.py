# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de entrenamiento del modelo Keras convolucional multiclase que realizará la clasificación de
# las imágenes según el dígito que representen.
# El modelo se recubre para exponer la interfaz esperada por Mlflow al objeto de que pueda ser
# registrado y consumido como un API Rest por clientes externos.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
import pandas as pd
from typing import Any, Dict
from analyticsbk.framework.logging.function_logger import logging_decor

from sklearn.ensemble import RandomForestClassifier


@logging_decor()
def train_model(
    x_train_with_features: pd.DataFrame,
    y_train_data: pd.DataFrame,
    parameters: Dict[str, Any]
):
    """ """
    classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
    classifier.fit(x_train_with_features, y_train_data)

    classifier.score(x_train_with_features, y_train_data)

    return classifier
