#!/bin/bash
# Porción del script Z planificado mediante Control-M incluido como referencia.

# Puertos Spark abierto en el contenedor
SPARK_DRIVER_PORT="$(($(($(date +%s%N)%1000))+24000))"
SPARK_MAPPER_PORT="$(($(($(date +%s%N)%1000))+25000))"

# Usuario de servicio
USER_NAME="bdauser"

# Comando docker
docker run \
-e JAVA_HOME=/usr/java/latest/jre \
-e PATH=/usr/java/latest/jre/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/hadoop/bin:/opt/spark/bin \
-e YARN_CONF_DIR=/opt/spark/conf/yarn-conf/ \
-e HADOOP_USER_NAME=$USER_NAME \
-v /usr/java/latest/jre:/usr/java/latest/jre:ro \
-v /opt/cloudera/:/opt/cloudera/:ro \
-v /etc/krb5.conf:/etc/krb5.conf:ro \
-v /bk/bigdata/working_dir/arq/$USER_NAME/$USER_NAME.keytab:/home/bdausr/keytab/$USER_NAME.keytab:ro \
-v /etc/hadoop/conf.cloudera.yarn/:/opt/hadoop/etc/hadoop/:ro \
-v /etc/spark2/conf.cloudera.spark2_on_yarn:/opt/spark/conf:ro \
-v /etc/hadoop/conf.cloudera.yarn/:/etc/hadoop/conf.cloudera.yarn/:ro \
-v /opt/oracle/bigdatasql/:/opt/oracle/bigdatasql/:ro \
-p $SPARK_DRIVER_PORT:$SPARK_DRIVER_PORT \
-p $SPARK_MAPPER_PORT:$SPARK_MAPPER_PORT \
--rm -it repo.dev.bankinter.bk/bkgs/big/model-deploy_demo:latest \
/bin/sh -c "/home/bdausr/launch/kedro_launch.sh --pipeline=__default__ --env=int --params spark.driver.port:${SPARK_DRIVER_PORT},spark.driver.blockManager.port:${SPARK_MAPPER_PORT}" "$@"
