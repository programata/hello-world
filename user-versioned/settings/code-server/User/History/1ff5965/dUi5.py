#
# (c) 2021 Bankinter S.A.
# Esqueleto de proyecto de Caso de uso Analytics
#
# ESQUELETO EJEMPLO. MODIFICAR COMO CORRESPONDA.
#
import pandas as pd
from pathlib import Path

import pyspark.sql as sp
import pytest
from typing import Union, Dict, Any

from kedro.framework.session import get_current_session
from kedro.framework.session.session import _activate_session, KedroSession
from kedro.runner import SequentialRunner
from pyspark.sql.session import SparkSession
from hypothesis.extra.pandas import column, data_frames, range_indexes
from hypothesis import strategies as st

from test_project.context import ProjectContext

TRAIN_TEST_RATIO = 0.10
TEST_DATASET_ROWS = 10


class BasicTestContextWithSparkSession(ProjectContext):
    """
    Contexto de ejecución Kedro para los tests. Básicamente es el mismo que el del proyecto, pero se
    considera buena práctica definir uno específico para incluir en él las especializaciones que
    puedan ser necesarias, como por ejemplo: usar un catálogo específico de pruebas.
    """
    def __init__(self, package_name: str, project_path: Union[Path, str], env: str = None,
                 extra_params: Dict[str, Any] = None, spark: bool = True):
        if get_current_session(silent=True) is None:
            _activate_session(KedroSession.create(package_name))
        super().__init__(package_name, project_path, env, extra_params, spark)

    @property
    def session(self):
        return self.get_or_create_session()


@pytest.fixture(scope='session')
def test_context_with_spark(path: str = str(Path.cwd())):
    """
    El contexto Kedro de pruebas, que contiene a su vez la sesión Spark, se define como una 'fixture'
    para que sea facilmente reutilizado por los distintos tests unitarios.
    """
    return BasicTestContextWithSparkSession("test_project", path)


@pytest.fixture(scope='session')
def test_catalog(test_context_with_spark):
    """
    El catálogo asociado al contexto Kedro expuesto como fixture.
    """
    return test_context_with_spark.catalog


@pytest.fixture(scope='session')
def test_runner():
    """
    La instancia de SequentialRunner que será compartido por los distintos tests.
    """
    return SequentialRunner()


def _generate_sample_digits():
    digit7 = '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000061f1df8b3b0000000000000000000000000000000000000000000000cafefefefcde82541d03000010120000000000000000000000000044fdfefefefefefefefec1bcbcdfe2210000000000000000000000005cfefefea2c5c5fbfefefefefefffe5b0000000000000000000000000efbfefe1200002475c8f4fefefefa0e00000000000000000000000000fbfefe6a00000000002893fefed90000000000000000000000000000c2fefe6a0000000000007ffefe9900000000000000000000000000009afefe6a000000000000cafefe4a000000000000000000000000000045f2e32300000000000edbfee3120000000000000000000000000000000c090000000000002cfefed80000000000000000000000000000000000000000000000007bfefed80000000000000000000000000000000000000000000000008cfefed80000000000000000000000000000000000000000000000008cfefe7f0000000000000000000000000000000000000000000000008cfefe780000000000000000000000000000000000000000000000008cfefe780000000000000000000000000000000000000000000000008cfefe780000000000000000000000000000000000000000000000008cfefec20000000000000000000000000000000000000000000000008cfefed80000000000000000000000000000000000000000000000008cfefed80000000000000000000000000000000000000000000000008cfefed800000000000000000000000000000000000000000000000000000000000000000000000000'
    digit8 = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000032ecfd77000000000000000000000000000000000000000000000087e5fcfc760000000000000000000000000000000000000000000733ddfcf7db2a00000000000000000000000000000000000000000069fcfcfcb1000000000000000000000000000000000000000000002decfcfcd82500000000000000000000000000000000000000000032defdfc872700000000000000000000000000000000000000000030e0fcfddc2a00000000000000000000000000000000000000000000e6fcfc9a0b00000000000000000000000000000000000000000012acf8fcfc3551c1c13e0d00000000000000000000000000000000006acbfcfcfcc0fcfcfccf1e0000000000000000000000000000000000b3fdfdfdfdfffdb995f1df00000000000000000000000000000000005bfcfcfcfcfded9b0087ef4600000000000000000000000000000005b7fcfcfcfcf7d8350087ef4600000000000000000000000000000028d9fcfcfcfcc6150000dfde00000000000000000000000000000000c6f3fcfcfccf1d053adfb61900000000000000000000000000000047f0fcfcfc841e0d99e2b5370000000000000000000000000000000000dffcfcfce786b7fcfcbc0e000000000000000000000000000000000053fcfcfcfcfcfdfcc1560000000000000000000000000000000000003eeffcfcfcfcfdd82400000000000000000000000000000000000000004a676781fcfdfc5800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

    sample = pd.DataFrame({
        'image_hex_bytes': [digit7, digit8],
        'label': [7, 6]
    })
    return sample


@pytest.fixture(scope='session')
def test_sample_digits_pandas_mock() -> pd.DataFrame:
    """

    :return:
    """
    return _generate_sample_digits()


@pytest.fixture(scope='session')
def test_sample_digits_spark_mock() -> sp.DataFrame:
    """
    Ejemplo de construcción de un mock de datos recubierto como una fixture pytest para su reutilización. En
    este caso se compone de manera manual usando para ello una cadena de texto codificada como dígitos
    hexadecimales 00..ff, que es el mismo esquema usado en el ejemplo de referencia, de este modo es
    posible usar el dataset generado en este fixture como datos de prueba equivalentes a los reales, y
    con la ventaja de que su generación vía código no precisa de accesos a bases de datos que pueden ser
    complejos en entornos de prueba y además mucho más lento que su proceso in-memory.

    La estructura del fixture es como se puede ver idéntica al del dataset de catalog.yml correspondiente,
    es decir:

        mnist_local_npz_dataset:
              type: analyticsbk.framework.io.MnistTfData
              filepath: 'data/01_raw/mnist.npz'

    en cuanto a campos y valores lo que permite que pueda actuar como doble de prueba de
    mnist_local_npz_dataset.

    :return: DataFrame Spark con dos dígitos MNIST en el formato definido en la implementación de ref.
    """

    return SparkSession.builder.getOrCreate().createDataFrame(_generate_sample_digits())


@pytest.fixture(scope='session')
def test_random_df_mock():
    """
    Construir una otra 'fixture' pytests de ejemplo, utilizando para ello la librería hypothesis.
    En este caso la fixture estará compuesta por un data frame pandas con la siguiente estructura:
        Columna ID:
            Tipo: Entero
            Valores: Aleatorios entre 0 y 1000000
            Permitidas repeticiones: No
        Columna TEXT:
            Tipo: Cadena de texto
            Valores: Aleatorios de entre 10 y 25 caracteres de longitud tomados del alfabeto: 'abcdef'
            Permitidas repeticiones: Sí
        Columna PROB:
            Tipo: Coma flotante
            Valores: Aleatorios en el cerrado [0, 1]
            Permitidas repeticiones: Sí
        Columna LABEL:
            Tipo: Entero
            Valores: Aleatorios del intervalo [0..9]
            Permitidas repeticiones: Sí
    El dataframe tendrá entre TEST_DATASET_ROWS y 2xTEST_DATASET_ROWS filas de longitud.

    :return: Finalmente el dataframe pandas se materializa como un dataframe Spark.
    """
    return SparkSession.builder.getOrCreate().createDataFrame(data_frames(
        columns=[
                column(
                    'ID',
                    elements=st.integers(min_value=0, max_value=1000000),
                    dtype=int,
                    unique=True
                ),
                column(
                    'TEXT',
                    elements=st.text(min_size=10, max_size=25, alphabet=list('abcdef'))
                ),
                column(
                    'PROB',
                    elements=st.floats(min_value=0.0, max_value=1.0)
                ),
                column(
                    'LABEL',
                    elements=st.integers(min_value=0, max_value=9)
                )
            ],
        index=range_indexes(max_size=TEST_DATASET_ROWS * 2, min_size=TEST_DATASET_ROWS)
        ).example()
    )
