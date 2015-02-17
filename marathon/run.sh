#!/bin/sh -e -x
cat << EOF > /etc/mesos/zk
zk://${MARATHON_ZK-zk}:2181/mesos
EOF

marathon
