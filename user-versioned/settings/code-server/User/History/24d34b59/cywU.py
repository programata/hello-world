# (c) 2020 Bankinter S.A.
# Esqueleto de proyecto ejemplo de Caso de Uso Analytics
#
"""Application entry point."""
import os
import uuid
from copy import deepcopy
from pathlib import Path
from typing import Dict, Union, Any, Optional

from pyspark import SparkConf
from pyspark.sql import SparkSession

from analyticsbk.framework.globals import ExtraParamsSingleton
from analyticsbk.framework.logging.function_logger import logging_decor
from kedro.framework.context import KedroContext

from analyticsbk.plugin.hooks import DynamicParamsHook


class ProjectContext(KedroContext):
    """Users can override the remaining methods from the parent class here,
    or create new ones (e.g. as required by plugins)
    """
    project_name = "test_project".replace('_', '')
    # `project_version` is the version of kedro used to generate the model
    project_version = "0.17.6"
    package_name = "test_project"

    SPARK_LEVEL_PARAM_NAME = 'SPARK_LOG_LEVEL'
    FECHADATO_PARAM_NAME = 'FECHADATO'
    MODEL_CHECKPOINT_HDFS_PATH_NAME = 'MODEL_CHECKPOINT_HDFS_PATH'

    initiated = False

    def __init__(
        self,
        package_name: str,
        project_path: Union[Path, str],
        conda: str = "python3.6",
        env: str = None,
        spark: bool = True,
        extra_params: Dict[str, Any] = None
    ):
        # No he podido dar con un mecanismo mas elegante para comunicarme con el Hook
        ExtraParamsSingleton().params = self._process_fechadato_in_params(extra_params)

        super().__init__(package_name, project_path, env, extra_params)

        if spark:
            self.get_or_create_session()

    @logging_decor()
    def _process_fechadato_in_params(
        self,
        extra_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        if extra_params is None:
            return {}
        else:
            params_copy = deepcopy(extra_params)
            upper_extra_params = {k.upper(): v for (k, v) in extra_params.items()}
            if ProjectContext.FECHADATO_PARAM_NAME in upper_extra_params:
                params_copy[ProjectContext.FECHADATO_PARAM_NAME] = \
                    '{:d}'.format(upper_extra_params[ProjectContext.FECHADATO_PARAM_NAME])
        return deepcopy(params_copy)

    @staticmethod
    def parse_params_dictionary(
        params: dict,
        res: dict,
        prefix='spark'
    ) -> None:
        """Transformar una diccionario de diccionarios de profundidad arbitraria en uno con la estructura
        {'spark.nive1.nivel2...niveln' = valor1, ...} habitual en la parametrización de Spark."""
        for k, v in params.items():
            if isinstance(v, dict):
                ProjectContext.parse_params_dictionary(v, res, prefix + '.' + k)
            else:
                res[prefix + '.' + k] = v

    @logging_decor()
    def _set_spark_log_level(self):
        if ExtraParamsSingleton().exists(self.SPARK_LEVEL_PARAM_NAME):
            SparkSession.builder.getOrCreate() \
                .sparkContext \
                .setLogLevel(ExtraParamsSingleton().params[self.SPARK_LEVEL_PARAM_NAME])
        else:
            SparkSession.builder.getOrCreate().sparkContext.setLogLevel('INFO')

    @logging_decor()
    def _read_spark_parameters(self):
        parameters = self.config_loader.get("spark*", "spark*/**")
        parameters = DynamicParamsHook.eval_dynamic_params(parameters)

        if 'spark' in self.params:
            spark_params = {}
            ProjectContext.parse_params_dictionary(self.params['spark'], spark_params)
            parameters.update((k, spark_params[k]) for k in spark_params.keys())
        return parameters

    @staticmethod
    @logging_decor()
    def _set_checkpoint_dir():
        if ExtraParamsSingleton().exists(ProjectContext.MODEL_CHECKPOINT_HDFS_PATH_NAME):
            SparkSession.builder \
                .getOrCreate() \
                .sparkContext \
                .setCheckpointDir(ExtraParamsSingleton().get_value(ProjectContext.MODEL_CHECKPOINT_HDFS_PATH_NAME))

    @logging_decor()
    def get_or_create_session(
        self,
        yarn=True
    ) -> Optional[SparkSession]:
        """
        Initialises a SparkSession using the config defined in model's conf folder.
        """

        # La versión de Arrow soportada es la 0.17.1 y no debería modificarse ni en local ni en remoto
        # pero se deja esta opción como salvaguarda.
        os.environ["ARROW_PRE_0_15_IPC_FORMAT"] = '1'

        if ProjectContext.initiated:
            return SparkSession.builder.getOrCreate()

        parameters = self._read_spark_parameters()

        if not parameters['spark.enabled']:
            return None
        else:
            del parameters['spark.enabled']

        spark_conf = SparkConf().setAll(parameters.items())
        #os.environ["PYSPARK_PYTHON"] = parameters['spark.yarn.appMasterEnv.PYSPARK_PYTHON']
        spark_session_conf = (
            SparkSession.builder.appName(
                "anlbk_{}_{}".format(self.project_name, uuid.uuid4().hex[:6])
            )
                .enableHiveSupport()
                .config(conf=spark_conf)
        )

        if yarn:
            session = spark_session_conf.master("yarn").getOrCreate()
        else:
            session = spark_session_conf.getOrCreate()

        self._set_spark_log_level()
        self._set_checkpoint_dir()
        ProjectContext.initiated = True

        return session
