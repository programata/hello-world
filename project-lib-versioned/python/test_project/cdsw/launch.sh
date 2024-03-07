#!/bin/bash
##########################################################################################
# Plantilla de ejecución de procesos desatendidos mediante la funcionalidad Jobs de CDSW #
##########################################################################################

#
# Modificar el comando Kedro para adaptarlo a las necesidades específicas del caso o bien
# sustituirlo por otro tipo de comando no necesariamente Kedro.
#
source activate python3.6 && kedro run --env=local --pipeline=inference --params epochs:100,batch_size:128,FECHADATO:$1

if [ $? -eq 0 ]
then
  exit 0
else
  exit 1
fi