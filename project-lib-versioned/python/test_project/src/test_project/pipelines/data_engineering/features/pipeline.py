# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de ingeniería de variables que genera un dataset que reprenta la luminisidad
# de cada
#
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from kedro.pipeline import Pipeline, node
from .nodes import build_powerful_features


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                build_powerful_features,
                inputs=["x_train_data", "x_test_data"],
                outputs=dict(
                    train="x_train_with_features",
                    test="x_test_with_features"
                )
            )
        ]
    )
