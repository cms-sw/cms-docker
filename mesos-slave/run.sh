#!/bin/sh -e -x
mesos-slave --master=${MESOS_MASTER_ZK-zk://zk:2181/mesos} \
             --work_dir=${MESOS_MASTER_WORKDIR-/var/lib/mesos} \
             --containerizers=mesos \
             --port=${MESOS_SLAVE_PORT-5051}
