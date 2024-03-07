#!/bin/bash
# Cambiar al directorio que corresponda si es necesario
cd /home/bdausr/test_project \
&& source activate python3.6 \
&& kinit -kt "/home/bdausr/keytab/${HADOOP_USER_NAME}.keytab" "${HADOOP_USER_NAME}@BANKINTER.BK" \
&& kedro run --pipeline=inference "$@"