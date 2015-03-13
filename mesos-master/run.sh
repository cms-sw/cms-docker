#!/bin/sh -e -x
mesos-master --zk=${MESOS_MASTER_ZK-zk://zk:2181/mesos} \
             --quorum=${QUORUM-1} \
             --work_dir=${MESOS_MASTER_WORKDIR-/var/lib/mesos} \
             --log_dir=${MESOS_LOG_DIR-/var/log/mesos} \
             --port=${MESOS_MASTER_PORT-5050}
