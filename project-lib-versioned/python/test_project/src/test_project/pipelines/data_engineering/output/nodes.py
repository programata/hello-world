# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de preparación inicial de datos incluye un único nodo de construcción de la tabla master
# y otro de limpieza de datos para el caso canónico de reconocimiento de dígitos MNIST.
# El nodo de construcción de la tabla master 'build_master_table' simplemente genera un dataset
# Spark que contendrá la base de datos MNIST leida de un fichero NPZ numpy desde local mediante
# el dataset de tipo MnistTfData definido en el catálogo.
# A continuación el nodo de limpieza de datos realiza una limpieza de etiquetas inválidas en el
# dataset y lo devuelve para que sea repositado en hdfs conforme a como se ha configurado en
# catalog.yml para evitar repetir innecesariamente este proceso que es además lento
# realizarse en local en su parte correspondiente al nodo 'build_master_table'.
#
# El usuario deberá modificar este pipeline para adecuarlo a sus necesidades de volcado de resultados
# del modelo. Tal como está definido escribirá la salida del modelo en un dataset CSV adaptado al
# formato de plataforma informacional Bankinter.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from pathlib import Path

import pandas as pd
from typing import Any, Dict

from kedro.framework.context import load_context
from pyspark.sql import SparkSession

from analyticsbk.framework.globals import ExtraParamsSingleton
from analyticsbk.framework.io import CSVOutputPIBDataSet
from analyticsbk.framework.logging.function_logger import logging_decor


@logging_decor()
def store_results(
        predictions: pd.DataFrame,
        parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Almacenar las predicciones en dos formatos: como fichero y como tabla particionada
    """
    if load_context(Path.cwd()).env == 'local':
        # Usar una directorio temporal para pruebas y desarrollo
        ExtraParamsSingleton().params[CSVOutputPIBDataSet.PREFIX_OS_VAR_NAME] = '/tmp/staging'

    filtered = predictions[['PassengerId', 'Name', 'Survived']]
    return dict(
        pred_file=filtered,
        pred_table=SparkSession.builder.getOrCreate().createDataFrame(filtered).repartition(64)
    )
