#!/usr/bin/sh

cat << EOF > /etc/zookeeper/conf/zoo.cfg
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
dataDir=${ZK_DATADIR-/var/lib/zookeeper/data}
# the port at which the clients will connect
clientPort=${ZK_CLIENT_PORT-2181}
EOF

#ZK_NODES is the list of nodes which will have zookeeper running on it.
if [ "X$ZK_NODES" = X ]; then
  # Single node setup.
  if [ ! -x /var/lib/zookeeper/data/myid ]; then
    zookeeper-server-initialize --myid=1
  fi
else
  # Handle the case for more than 1 node.
  # Generate the configuration starting from specified environment variables.
  # For the moment we assume that servers all have the same kind of hostname
  # in the for XYZ<ID>
  for x in ${ZK_NODES}; do
    ZK_NODE_ID=`echo $x | sed -e's/^[a-zA-Z0-]*//;s/[.].*//'`
    echo "server.$ZK_NODE_ID=$x:${ZK_PEERS_PORT-2888}:${ZK_ELECTION_PORT-3888}" >> /etc/zookeeper/conf/zoo.cfg
  done
  echo >> /etc/zookeeper/conf/zoo.cfg
  if [ ! -e /var/lib/zookeeper/data/myid ]; then
    zookeeper-server-initialize --myid=`hostname | sed -e 's/^[a-zA-Z0-]*//;s/[.].*//'`
  fi
fi

env
cat /etc/hosts
cat /etc/zookeeper/conf/zoo.cfg
cat /var/lib/zookeeper/data/myid
which java
/usr/lib/zookeeper/bin/zkServer.sh start-foreground
