# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de medición del rendimiento del modelo mediante el conjunto de test.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from kedro.pipeline import Pipeline, node
from .nodes import report_performance


def create_pipeline(outputs="accuracy"):
    return Pipeline(
        [
            node(
                report_performance,
                # Dataset de test etiquetado como entrada
                inputs=["mnist_test_xy", "trained_model", "parameters"],
                # Un escalar en el rango [0..1] como resultado del pipeline
                outputs=outputs,
            )
        ]
    )
