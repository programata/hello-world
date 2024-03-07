# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de entrenamiento del modelo de reconocimiento de dígitos decimales
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from kedro.pipeline import Pipeline, node
from .nodes import train_model


def create_pipeline(outputs: str = 'trained_model'):
    return Pipeline(
        [
            node(
                train_model,
                # El entrenamiento de modelo toma como entrada el dataset de train que incluye etiquetas
                inputs=["x_train_with_features", "y_train_data", "parameters"],
                # Y la salida será, evidentemente, el modelo entrenado, en este caso en un
                # formato compatible con Mlflow, pero no es imprescindible.
                outputs=outputs,
            )
        ]
    )
