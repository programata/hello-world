#
# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# Test del pipeline completo que se pude considerar como de integración.
# Por defecto está desactivado.
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
import pytest

from tests.fixtures import test_runner, test_catalog, test_context_with_spark, test_sample_digits_spark_mock
from test_project.pipeline_registry import register_pipelines


@pytest.mark.skip(reason="Considerado de integración. Activar cuando sea preciso.")
def test_default_pipeline(
    test_context_with_spark,
    test_catalog,
    test_runner,
        test_sample_digits_spark_mock
) -> None:
    # Crear el pipeline con un nombre de dataset no incluido en el catálogo para que
    # sea almacenado 'in-memory'
    default_pipeline = register_pipelines()['__default__']

    # Ejecutar el pipeline anterior en contexto Kedro de test
    output = test_runner.run(default_pipeline, test_catalog)

    assert output['accuracy'] > 0.9
