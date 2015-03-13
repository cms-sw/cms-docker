#!/bin/sh -e -x

# Simply starts the mesos slave.
#
# Notice that in case of a frontend, we expose port 53 as well
# as a valid resource.
mesos-slave --master=${MESOS_MASTER_ZK-zk://zk:2181/mesos} \
             --work_dir=${MESOS_MASTER_WORKDIR-/var/lib/mesos} \
             ${MESOS_SLAVE_FRONTEND+--resources='ports(*):[31000-32000, 53-53]'} \
             --containerizers=docker,mesos \
             --port=${MESOS_SLAVE_PORT-5051}
