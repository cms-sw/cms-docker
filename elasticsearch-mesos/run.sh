#!/bin/sh

# Wrapper script to run this in docker, modifying configuation on the fly.
# You can specify the following parameters:

ZOOKEEPER=${ZOOKEEPER-zk://localhost:2128/mesos}
cd /elasticsearch-mesos/elasticsearch-mesos-*
bin/elasticsearch-mesos
