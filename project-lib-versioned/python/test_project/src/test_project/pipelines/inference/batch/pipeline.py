# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Pipeline de ejecución del modelo para obtener sus predicciones para el dataset
# variable predictoras proporcionado por 'predictor_data'
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from kedro.pipeline import Pipeline, node
from .nodes import execute_model, prepare_inference_data


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                prepare_inference_data,
                # Dataset de predictores y modelo como entrada...
                inputs=["titanic_validation_data", "parameters"],
                # ... y las predicciones como salida.
                outputs="inference_data_with_features"
            ),
            node(
                execute_model,
                # Dataset de predictores y modelo como entrada...
                inputs=["titanic_validation_data", "inference_data_with_features", "trained_model", "parameters"],
                # ... y las predicciones como salida.
                outputs="predictions"
            )
        ]
    )
