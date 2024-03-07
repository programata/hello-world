"""Entry point for running a Kedro pipeline as a Python package."""
from pathlib import Path
from typing import Any, Dict, Union

from kedro.framework.context import KedroContext
from pyspark import SparkConf
from pyspark.sql import SparkSession


class ProjectContext(KedroContext):
    """A subclass of KedroContext to add Spark initialisation for the pipeline."""

    project_name = "test_project".replace('_', '')
    # `project_version` is the version of kedro used to generate the model
    project_version = "0.17.6"
    package_name = "test_project"

    def __init__(
        self,
        package_name: str,
        project_path: Union[Path, str],
        conda: str = "python3.6",
        env: str = None,
        spark: bool = True,
        extra_params: Dict[str, Any] = None,
        config_loader: Any = None,
        hook_manager: Any = None
    ):
        super().__init__(package_name, project_path, env, extra_params)
        self.init_spark_session()

    def init_spark_session(self) -> None:
        """Initialises a SparkSession using the config
        defined in project's conf folder.
        """

        # Load the spark configuration in spark.yaml using the config loader
        parameters = self.config_loader.get("spark*", "spark*/**")
        spark_conf = SparkConf().setAll(parameters.items())

        # Initialise the spark session
        spark_session_conf = (
            SparkSession.builder.appName(self.package_name)
            .enableHiveSupport()
            .config(conf=spark_conf)
        )
        _spark_session = spark_session_conf.getOrCreate()
        _spark_session.sparkContext.setLogLevel("WARN")
