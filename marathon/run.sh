#!/bin/sh -e -x
java -Djava.library.path=/usr/local/lib:/usr/lib:/usr/lib64 \
     -Djava.util.logging.SimpleFormatter.format=%2$s%5$s%6$s%n \
     -Xmx512m -cp /usr/bin/marathon mesosphere.marathon.Main \
     --zk zk://${MARATHON_ZK-zk}:2181/marathon \
     --master zk://${MARATHON_ZK-zk}:2181/mesos
