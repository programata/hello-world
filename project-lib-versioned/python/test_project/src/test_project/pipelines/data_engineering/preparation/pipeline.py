# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipelone de preparación de datos, el dataset resultado 'mnist_cleaned_spark_dataset' se
# materializará en hdfs tal como está configurado en el catálogo.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from kedro.pipeline import Pipeline, node
from .nodes import clean_data, read_raw_data


def create_pipeline(
    raw_train_data='titanic_train_data',
    raw_test_data='titanic_validation_data'
) -> Pipeline:
    return Pipeline(
        [
            node(
                read_raw_data,
                inputs=[raw_train_data, raw_test_data, "parameters"],
                outputs=dict(
                    train='raw_train_data_read',
                    validation='raw_validation_data_read'
                )
            ),
            node(
                clean_data,
                inputs=['raw_train_data_read', 'raw_validation_data_read', "parameters"],
                outputs=dict(
                    train='raw_train_data_cleaned',
                    validation='raw_validation_data_cleaned'
                )
            )
        ]
    )
