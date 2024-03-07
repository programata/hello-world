import numpy as np

from test_project.pipelines.data_engineering.features.nodes import build_powerful_features
from tests.fixtures import test_runner, test_catalog, test_context_with_spark, test_sample_digits_pandas_mock, \
    test_random_df_mock, test_sample_digits_spark_mock

# Dimensiones de las imágenes
IMG_ROWS, IMG_COLS = 28, 28


def _build_test_image_features_with_bright(images, bright=1.0):
    features = build_powerful_features(images)
    size = images.count()

    # Construir un tensor numpy con la forma esperada por el modelo Keras
    fields = ['pixel' + str(i) for i in range(IMG_COLS * IMG_ROWS)]
    predictors = np.asarray(features['features'].select(fields).collect()).reshape((size, IMG_ROWS, IMG_COLS))

    return predictors * bright


def test_model_basic_validation(
    test_catalog,
    test_sample_digits_spark_mock
) -> None:
    """
    En este tipo de tests de 'propiedades' en general se validan invariantes del modelo,
    evidentemente estas dependen del CdU concreto, pero por ejemplo en nuestro ejemplo de
    reconocimiento de dígitos podrían ser pruebas válidas aumentar o disminuir el brillo de
    una serie de casos para verficar que el carácter identificado sigue siendo el mismo.

    En este primer caso se comprobará que las imágenes de dos dígitos conocidos se reconocen
    correctamente.

    :param test_catalog:
    :param test_sample_digits_spark_mock:
    :return:
    """
    predictors = _build_test_image_features_with_bright(test_sample_digits_spark_mock)

    # El modelo debe existir con anterioridad al test, esto no es muy ortodoxo ya que cada test
    # debería ser autocontenido y poder ejecutarse de manera aislada.
    model = test_catalog.load('trained_model')

    predictions = model.predict(predictors)

    # El primer dígito es un siete y el segundo un séis
    assert np.argmax(predictions[0]) == 7 and np.argmax(predictions[1]) == 6


def test_bright_invariance_validation(
    test_catalog,
    test_sample_digits_spark_mock
) -> None:
    """
    En este ejemplo comprobaremos la invarianza del modelo frente al brillo de los pixels de la imagen

    :param test_catalog:
    :param test_sample_digits_spark_mock:
    :return:
    """
    # Imágenes con el brillo normal
    predictors_normal = _build_test_image_features_with_bright(test_sample_digits_spark_mock, 1.0)

    # Imágenes con brillo reducido a la mitad
    predictors_dark = _build_test_image_features_with_bright(test_sample_digits_spark_mock, 0.5)

    model = test_catalog.load('trained_model')

    # Predecir con brillo normal y reducido
    predict_normal = model.predict(predictors_normal)
    predict_dark = model.predict(predictors_dark)

    # Comprobar que las predicciones son las mismas en ambos casos
    assert np.argmax(predict_normal[0]) == np.argmax(predict_dark[0]) and \
           np.argmax(predict_normal[1]) == np.argmax(predict_dark[1])
