# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipelone de ejecución de tests para el ciclo de vida.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from kedro.pipeline import Pipeline, node
from .nodes import test_model


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                test_model,
                inputs=["mnist_test_xy", "trained_model", "parameters"],
                outputs="passed",
            )
        ]
    )