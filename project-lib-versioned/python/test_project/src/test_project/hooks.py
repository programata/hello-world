#
# (c) 2020 Bankinter S.A.
#
# Hook base de Framework. Los casos de uso pueden modificarlo pero manteníendo la funcionalidad.
#
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Union, List

from kedro.config import ConfigLoader, TemplatedConfigLoader
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.versioning import Journal

from analyticsbk.common.crypto_utils import decrypt_base64_string
from analyticsbk.framework.globals import ExtraParamsSingleton


def _decrypt_key(key: str) -> str:
    return key


def _decrypt_value(key: str, value: str) -> str:
    if not key.startswith('CRYPTO_'):
        return value
    return decrypt_base64_string(value)


def _decrypt_secret_params(
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """

    :param params:
    :return:
    """
    clear_params = {_decrypt_key(k): _decrypt_value(k, v)
                    for (k, v) in deepcopy(params).items()}
    return deepcopy(clear_params)


class CryptoTemplatedConfigLoader(TemplatedConfigLoader):
    """

    """
    def _load_configs(self, config_filepaths: List[Path]) -> Dict[str, Any]:
        aux = super()._load_configs(config_filepaths)
        return _decrypt_secret_params(aux)

    def get(self, *patterns: str) -> Dict[str, Any]:
        aux = super().get(*patterns)
        return aux

    def __init__(
        self,
        conf_paths: Union[str, Iterable[str]],
        *,
        globals_pattern: Optional[str] = None,
        globals_dict: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(conf_paths, globals_pattern=globals_pattern, globals_dict=globals_dict)


class ProjectHooks:
    def __init__(self) -> None:
        super().__init__()
        self._extra_params = {}

    @property
    def extra_params(self):
        return self._extra_params

    @extra_params.setter
    def extra_params(self, value):
        if value is None:
            value = {}
        self._extra_params = value

    @hook_impl
    def register_config_loader(self, conf_paths: Iterable[str]) -> ConfigLoader:
        params = _decrypt_secret_params(ExtraParamsSingleton().params)
        return CryptoTemplatedConfigLoader(
            conf_paths,
            globals_pattern="*globals.yml",
            globals_dict={**dict(os.environ), **params},
        )

    @hook_impl
    def register_catalog(
        self,
        catalog: Optional[Dict[str, Dict[str, Any]]],
        credentials: Dict[str, Dict[str, Any]],
        load_versions: Dict[str, str],
        save_version: str,
        journal: Journal,
    ) -> DataCatalog:
        return DataCatalog.from_config(
            catalog, credentials, load_versions, save_version, journal
        )


project_hooks = ProjectHooks()
