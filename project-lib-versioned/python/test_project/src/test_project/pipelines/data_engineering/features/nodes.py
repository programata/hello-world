# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Ingeniería de variables. En este caso se tratará de transformar cada pixel de las imágenes
# B/W que componen el dataset de su representación como un dígito hexadecimal en el rango
# 00..FF a un valor real en el rango [0, 1] y devolver este resultado como un array
# Numpy con la forma (, IMAGE_SIZE, IMAGE_SIZE) que puede ser tratado directamente
# mediante Keras.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from typing import Any, Dict
from analyticsbk.framework.logging.function_logger import logging_decor
import pandas as pd

from sklearn.preprocessing import StandardScaler


@logging_decor()
def build_powerful_features(
    x_train_data: pd.DataFrame,
    x_test_data: pd.DataFrame
) -> Dict[str, Any]:
    """"""
    sc = StandardScaler()
    x_train = sc.fit_transform(x_train_data)
    x_test = sc.transform(x_test_data)

    return dict(
        train=x_train,
        test=x_test
    )
