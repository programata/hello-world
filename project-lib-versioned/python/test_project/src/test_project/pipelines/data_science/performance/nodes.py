# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de medición del rendimiento del modelo mediante el conjunto de test.
#
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from typing import Any, Dict
import numpy as np
from pyspark.sql import DataFrame

from analyticsbk.framework.logging import logging_decor

# Dimensiones de las imágenes
IMG_ROWS, IMG_COLS = 28, 28


@logging_decor()
def report_performance(
        test_data: DataFrame,
        model: Any,
        parameters: Dict[str, Any]
) -> None:
    fields = ['pixel' + str(i) for i in range(IMG_COLS * IMG_ROWS)]
    size = test_data.count()

    # Convertir a tensores numpy local con la forma que espera Keras
    test_x = np.asarray(test_data.select(fields).collect()).reshape((size, IMG_ROWS, IMG_COLS))
    test_y = np.asarray(test_data.select(['label']).collect()).reshape((size))

    # Ejecutar el modelo con los datos de test
    predictions = model.predict(test_x)

    # El modelo devuelve un vector de 'probabilidades', tomamos como predicción la más probable
    target = np.argmax(predictions, axis=1)

    # Calculamos el acierto del modelo sobre el conjunto de test.
    accuracy = np.sum(target == test_y) / len(test_y)

    return accuracy
