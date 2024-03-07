#
# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Tests de los pipelines y nodos de 'data_engineering'.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
from test_project.pipelines.data_engineering.features.nodes import build_powerful_features
from test_project.pipelines.data_engineering.preparation import create_pipeline
from tests.fixtures import test_runner, test_catalog, test_context_with_spark, test_sample_digits_spark_mock


def test_preparation_pipeline(
    test_context_with_spark,
    test_catalog,
    test_runner
) -> None:
    """
    No usamos mock porque los datos los incluimos desde el propio proyecto, no provienen
    de un almacen externo por lo que en cierto modo están ya mockeados en el sentido
    de que no pueden variarse de forma externa, como sí sucedería si los tomáramos de una
    base de datos Hive, por ejemplo.

    Este pipeline está compuesto de dos nodos por lo que se ha preferido testear el pipeline
    en si, que es una manera de aproximarse a testear el API público, que es lo que
    habríamos hecho en un proyecto SW más tradicional.

    :param test_context_with_spark:
    :param test_catalog:
    :param test_runner:
    :return:
    """
    # Crear el pipeline con un nombre de dataset no incluido en el catálogo para que
    # sea almacenado 'in-memory'
    prep_pipeline = create_pipeline(mnist_cleaned_spark_dataset='cleaned_in_memory')

    # Ejecutar el pipeline anterior en contexto Kedro de test
    output = test_runner.run(prep_pipeline, test_catalog)

    # Comprobar que el dataset MNIST tiene el tamaño esperado
    assert output['cleaned_in_memory'].count() == 70000

    # Asegurar que todas las etiquetas contienen valores en el rango esperado
    assert output['cleaned_in_memory'].filter(output['cleaned_in_memory'].label < 0).count() == 0


def test_build_powerful_features_node(
    test_context_with_spark,
    test_catalog,
    test_runner,
    test_sample_digits_spark_mock
) -> None:
    """
    Al estar el pipeline de ingeniería de variables constituido por un solo nodo vamos a validar el función
    Python que implementa dicho nodo. La prueba del pipeline de ing. de variables se incluirá dentro de la
    verificación del pipeline completo dentro de lo que podría considerarse pruebas de integración.

    Para esta verificación usaremos un doble de prueba del dataset MNIST definido como una fixture en el
    fichero test_fixtures.pyt. Este mock contiene solo dos dígitos en el formato hexadecimal definido para
    almacenarlo dentro del paquete Python.

    La estructura de este test se repetirá frecuentemente y puede tomarse como un patrón de diseño, en
    concreto:
        - test que toma, entro otros parámetros, una fixture con el mock de un dataset controlado
        - Invocación, o ejercicio en terminología de pruebas de la función a verificar
        - Uno o varios comandos assert que se aseguran de que el resultado del paso anterior tiene las
          propiedades esperadas.
    En general deben escribirse tests para verificar el comportamiento de todas las transformaciones
    de datos. Lo importante aquí es validar el comportamiento general y no las distintas funciones que
    intermedias que implementen este comportamiento. Esto es así porque el comportamiento general tiende
    naturalmente a ser más estable, mientras que las funciones intermedias son más cambiantes, por lo
    que si se incluyen en los tests es fácil que un cambio en estas rompa los tests, a pesar de que
    la transformación de datos siga siendo la misma.

    :param test_context_with_spark:
    :param test_catalog:
    :param test_runner:
    :param test_sample_digits_spark_mock:
    :return:
    """
    # Ejecutar la función que constituye el nodo con el dataset de prueba
    res = build_powerful_features(test_sample_digits_spark_mock, {})

    # Realizar algunas comprobaciones sobre le dataset obtenido para obtener cierta
    # certeza de que el resultado es el esperado
    assert len(res['features'].columns) == 785 and \
           res['features'].columns[0] == 'label'

    assert res['features'].count() == 2

    assert sum(list(res['features'].collect()[0])[1:]) > 0 and \
           sum(list(res['features'].collect()[1])[1:]) > 0
