# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de division en conjunto de entrenamiento y conjunto de prueba del
# dataset MNIST
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from kedro.pipeline import Pipeline, node
from .nodes import split_train_test


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                split_train_test,
                inputs=["raw_train_data_cleaned"],
                # Los dos datasets mnist_train_xy y mnist_test_xy, están definidos el
                # fichero de catálogo lo que implica que se materializarán del modo
                # indicado en él. Esto es útil, por ejemplo, durante el desarrollo para no
                # reejecutar una y ota vez partes del pipeline que ya funcionan correctamente
                # con la ganancia en tiempo que ello significa.
                outputs=dict(
                    X_train="x_train_data",
                    y_train="y_train_data",
                    X_test="x_test_data",
                    y_test="y_test_data"
                )
            )
        ]
    )
