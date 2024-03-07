# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipelone de salida de datos, el dataset resultado 'mnist_cleaned_spark_dataset' se
# materializará en formato CSV usando le clase definida en catálogo.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from kedro.pipeline import Pipeline, node
from .nodes import store_results


def create_pipeline(**kwargs):
    """Almacenar las predicciones en dos formatos: como fichero y como tabla particionada
    """
    return Pipeline(
        [
            node(
                store_results,
                inputs=["predictions", "parameters"],
                outputs=dict(
                    pred_file="file_store_predictions",
                    pred_table="partitioned_store_predictions"
                )
            )
        ]
    )
