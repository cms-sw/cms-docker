#!/bin/sh

# Wrapper script to run this in docker, modifying configuation on the fly.
# You can specify the following parameters:
MESOS_EXECUTOR_URL=${MESOS_EXECUTE_URL-http://downloads.mesosphere.io/elasticsearch/elasticsearch-mesos-1.0.0-1.tgz}
MESOS_MASTER=${MESOS_MASTER-zk://localhost:2128/mesos}
MESOS_JAVA_PATH=${MESOS_JAVA_PATH-/usr/local/lib}
ES_N_OF_NODES=${N_OF_NODES-1}
ES_BASEDIR=${ES_BASEDIR-es}

RESOURCE_CPUS=${RESOURCE_CPUS-1.0}
RESOURCE_MEM=${RESOURCE_MEM-2048}
RESOURCE_DISK=${RESOURCE_DISK-1000}

cat > /elasticsearch-mesos/config/mesos.yml << EOF
mesos.executor.uri: '$MESOS_EXECUTOR_URL'

# Where the Mesos master is located
mesos.master.url: '$MESOS_MASTER'

# Where we can find the Mesos library
java.library.path: '$MESOS_JAVA_PATH'
# No of HW nodes we want it to run on
# Driver will block until we have enough nodes# (We can't start multiple Elastic Search nodes of the same cluster on the same HW node due to port conflicts)
elasticsearch.noOfHwNodes: $ES_N_OF_NODES 

# Mesos resource requests
resource.cpus: $RESOURCE_CPUS
resource.mem: $RESOURCE_MEM
resource.disk: $RESOURCE_DISK

${MESOS_ATTRIBUTES+# Mesos attributes required.}
EOF

for a in `echo $MESOS_ATTRIBUTES | tr \; \\n | sed -e 's/:/: /'`; do
  echo attribute.$a >> /elasticsearch-mesos/config/mesos.yml
done

cat > /elasticsearch-mesos/config/elasticsearch.yml << EOF
path.conf: $ES_BASEDIR/conf
path.data: $ES_BASEDIR/data
path.work: $ES_BASEDIR/work
path.logs: $ES_BASEDIR/logs
path.plugins: $ES_BASEDIR/plugins

# We use mesos for discovery.
discovery.zen.ping.multicast.enabled: false
discovery.zen.ping.unicast.hosts: [\${seedNodes}]
EOF

cd /elasticsearch-mesos
bin/elasticsearch-mesos
