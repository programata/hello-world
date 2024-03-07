# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

import analyticsbk
from analyticsbk import BITACORA_LOGGER
from .pipelines.data_engineering import preparation as prep
from .pipelines.data_engineering import features as ft
from .pipelines.data_engineering import output as ot
from .pipelines.data_science import tt_split as tt
from .pipelines.data_science import training as tr
from .pipelines.data_science import performance as pr
from .pipelines.inference import batch as bt
from .pipelines.cicd import tests as ts


BITACORA_LOGGER.info(f"Iniciando la ejecución del pipeline "
                     f"analyticsBK con versión de framework '{analyticsbk.__version__}'.")


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.
    Returns:
        Un diccionario de pipelines mapeados por nombre
    """
    preparation_pipeline = prep.create_pipeline()
    features_pipeline = ft.create_pipeline()
    split_pipeline = tt.create_pipeline()
    training_pipeline = tr.create_pipeline()
    performance_pipeline = pr.create_pipeline()
    inference_pipeline = bt.create_pipeline()
    test_pipeline = ts.create_pipeline()
    store_pipeline = ot.create_pipeline()

    return {
        "prep": preparation_pipeline,
        "features": preparation_pipeline + split_pipeline + features_pipeline,
        "split": features_pipeline + split_pipeline,
        "train": preparation_pipeline + split_pipeline + features_pipeline + training_pipeline,
        "test_cd": test_pipeline,
        "performance": performance_pipeline,
        "inference": inference_pipeline,
        "__default__": preparation_pipeline + split_pipeline + features_pipeline +
        training_pipeline + inference_pipeline + store_pipeline
    }
