
from typing import Any, Dict
import pandas as pd
import numpy as np
from kedro.io import AbstractDataSet


class MnistTfData(AbstractDataSet):
    """
    Un dataset custom para el esqueleto de proyecto Kedro que permite leer el ejemplo canónico
    de MNIST desde el formato NPZ de numpy para generar un dataset pandas con cada una de las
    70000 imágenes de 28x28 pixels que componen el dataset según la siguiente disponición:
    ------------------------------------------------------------------------------------------
    |                            image_hex_bytes                          |      label       |
    ----------------------------------------------------------------------|-------------------
    0000000000fefecc.............................................cdcd0000 |         7
    0000000000aecfcc.............................................bcbc0000 |         1
    0000000000bcefff.............................................cbde0000 |         2
    00000000aabcbbbb.............................................ccdd0000 |         3

    Donde image_hex_bytes es de tipo string y codifica el valor 0..255 de cada pixel mediante dos
    caracters hexadecimales en el rango 00..FF y label es un valor entero indicando el dígito
    representado en la imagen y por lo tanto en el intervalo 0..9

    """
    def _save(self, data: pd.DataFrame) -> None:
        ...

    def _describe(self) -> Dict[str, Any]:
        return dict(dontcare='')

    def __init__(
        self,
        filepath
    ) -> None:
        self.filepath = filepath

    @staticmethod
    def _load_from_npz_data(path='data/01_raw/mnist.npz'):
        with np.load(path, allow_pickle=True) as f:
            x_train, y_train = f['x_train'], f['y_train']
            x_test, y_test = f['x_test'], f['y_test']

        return (x_train, y_train), (x_test, y_test)

    @staticmethod
    def _build_dataframe_from_numpy(obs, labels):
        return pd.DataFrame({
            'pixels': [obs[i] for i in range(len(obs))],
            'label': labels
        })

    def _load(self) -> pd.DataFrame:
        (x_train, train_label), (x_test, test_label) = self._load_from_npz_data(self.filepath)

        train_label = train_label.astype('int')
        test_label = test_label.astype('int')

        pixels = np.concatenate((x_test, x_train))
        size = pixels.shape[1] * pixels.shape[2]
        byte_pixels = [bytearray([int(x) for x in r]).hex() for r in np.reshape(pixels, (pixels.shape[0], size))]
        labels = np.concatenate((test_label, train_label))

        mnist = pd.DataFrame(byte_pixels, columns=['image_hex_bytes'])
        mnist['label'] = labels
        return mnist
