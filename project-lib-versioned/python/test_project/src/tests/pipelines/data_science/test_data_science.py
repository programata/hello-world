#
# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Tests de los pipelines y nodos de 'data_science'.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
import tensorflow.python.keras.models
from hypothesis import given, settings, HealthCheck
from hypothesis.extra.pandas import column, data_frames, range_indexes
from hypothesis import strategies as st

from test_project.pipelines.data_science.training.pipeline import create_pipeline as create_training_pipeline
from test_project.pipelines.data_science.performance.pipeline import create_pipeline as create_performance_pipeline
from test_project.pipelines.data_science.tt_split.nodes import split_train_test
from tests.fixtures import test_runner, test_catalog, test_context_with_spark, test_sample_digits_spark_mock, \
    test_random_df_mock


TRAIN_TEST_RATIO = 0.10
TEST_DATASET_ROWS = 100
IN_MEMORY_KERAS_MODEL = 'test_memory_trained_model'


@given(hypothesis_df=data_frames(
        index=range_indexes(max_size=TEST_DATASET_ROWS*2, min_size=TEST_DATASET_ROWS),
        columns=[
            column(
                'ID',
                elements=st.integers(min_value=0, max_value=1000000),
                dtype=int,
                unique=False
            ),
            column(
                'PROB',
                elements=st.floats(min_value=0.0, max_value=1.0)
            ),
            column(
                'LABEL',
                elements=st.integers(min_value=0, max_value=9)
            ),
            column(
                'TEXT',
                elements=st.text(min_size=50, max_size=100, alphabet=list('abcdef0123456789'))
            ),
        ]
    )
)
@settings(
    suppress_health_check=[HealthCheck.too_slow],   # El dataset es grande y su generación toma algún tiempo
    max_examples=5,                                 # Número de casos de prueba a generar
    deadline=60000                                  # Duración máxima del tests en ms.
)
def test_split_train_test_node(
    hypothesis_df,
    test_context_with_spark,
    test_catalog,
    test_runner,
    test_random_df_mock
) -> None:
    """
    Comprobación mediante test unitario que una transformación de datos, en este caso la división
    en conjuntos de prueba y entrenamiento es correcta, en general es una buena práctica incluir este
    tipo de tests para todas las transformaciones.

    También es deseable que los tests puedan ejecutarse aisladamente, sin depender de otros tests o de
    otras infraestructuras como bases de datos, sistemas de ficheros etc para lo que resulta muy
    interesante ser capaz, por ejemplo, de generar conjuntos de datos de prueba sintéticos para lo cual
    se recomienda usar la librería 'hypothesis' https://hypothesis.readthedocs.io/en/latest/
    como se muestra en este caso, con la que, simplemente decorando la función de test de manera apropiada,
    se puede disponer de cualquier número de datasets sintéticos en forma de Pandas, y de otros muchos formatos,
    con la estructura que se desee.

    :param test_context_with_spark:
    :param test_catalog:
    :param test_runner:
    :return:
    """
    # Ejercitar el nodo de split en train y test
    result = split_train_test(test_context_with_spark.get_or_create_session().createDataFrame(hypothesis_df), TRAIN_TEST_RATIO)

    # Una forma de aproximada comprobar que el número de registros de entrenamiento es >> que el de test
    assert result['train'].count() > result['test'].count() * 4


def test_training_pipeline(
    test_context_with_spark,
    test_catalog,
    test_runner
) -> None:
    """
    Ejecutar el pipeline de entrenamiento del modelo usando los datasets reales y comprobar
    que efectivamente se genera un modelo de redes Keras.

    Idealmente todos y cada uno de los tests debería poder ejecutarse aisladamente, pero en este
    caso, mockear los 785 campos que contienen el brillo de cada pixel de la imágen del
    dígito MNIST sería realmente arduo. Por lo que se ha recurrido a ejecutar el pipeline auténtico
    de entrenamiento. La buena práctica, y lo aconsejable en un caso real, sería mockear un set de datos de
    entrenamiento preestablecidos para asegurarnos de que el modelo resultante es el correcto.

    :param test_context_with_spark:
    :param test_catalog:
    :param test_runner:
    :return:
    """
    # Construir el pipeline con un dataset de salida definido en en el catálogo
    # porque los modelos keras no soportan el formato pickle necesario para su manejo in-memory
    train_pipeline = create_training_pipeline(outputs=IN_MEMORY_KERAS_MODEL)

    # Ejecutar el pipeline anterior en el contexto Kedro de test
    test_runner.run(train_pipeline, test_catalog)

    # Comprobar que el modelo existe efectivamente y es del tipo esperado
    assert isinstance(test_catalog.load(IN_MEMORY_KERAS_MODEL), tensorflow.keras.models.Sequential)


def test_performance_pipeline_behavior_validation(
    test_context_with_spark,
    test_catalog,
    test_runner
):
    """
    Esta es es validación del modelo respecto a la precisión que alcanza en el conjunto de test.
    En un CdU real, esta validación se debería extender no solo a la precisión en test si no también
    en otros conjuntos de datos que se consideren relevantes, casos especialmente difíciles o
    críticos, por ejemplo, en un scoring de riesgos se deberían validar casos con importes elevados
    o perteneciente a sectores económicos en situación difícil, como la construcción.
    Mientras que en un coche autónomo podría verificarse el comportamiento frente a un ciclista o
    un peatón.

    :param test_context_with_spark:
    :param test_catalog:
    :param test_runner:
    :return:
    """
    # Crear el instanciar el pipeline con resultado in-memory.
    performance_pipeline = create_performance_pipeline(outputs='accu')

    # Ejecutar el pipeline anterior en el contexto Kedro, dado que el nombre del dataset de salida
    # no está definido en el catálogo Kedro generará uno in-memory que recogeremos en la variable
    # 'accuracy'.
    accuracy = test_runner.run(performance_pipeline, test_catalog)

    assert accuracy['accu'] > 0.9
