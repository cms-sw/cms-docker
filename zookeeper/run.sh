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
dataDir=/var/lib/zookeeper/data
# the port at which the clients will connect
clientPort=2181
EOF


if [ X$ZK_NUM_NODES = X ]; then
  # Single node setup.
  if [ ! -x /var/lib/zookeeper/data/myid ]; then
    zookeeper-server-initialize --myid=1
  fi
else
  # Handle the case for more than 1 node.
  # Generate the configuration starting from specified environment variables.
  for x in `seq 1 ${ZK_NUM_NODES}`; do
    # ZK_PEER has incremental numer if ZH_HOSTNAME is actually defined.
    # If the ZK_HOSTNAME is not defined, we use different port for each
    # zookeeper instance so that they can survive on the same ip.
    ZK_PEER=${ZK_HOSTNAME-localhost}${ZK_HOSTNAME+0$x}${ZK_DOMAIN+.$ZK_DOMAIN}
    ZK_PORT1=`echo 2888 + ${ZK_HOSTNAME-$x - 1}  | bc`
    ZK_PORT2=`echo 3888 + ${ZK_HOSTNAME-$x - 1}  | bc`
    echo "server.$x=$ZK_PEER:$ZK_PORT1:$ZK_PORT2" >> /etc/zookeeper/conf/zoo.cfg
  done
  if [ ! -x /var/lib/zookeeper/data/myid ]; then
    zookeeper-server-initialize --myid=`hostname | sed -e 's/^[a-zA-Z0]*//'`
  fi
fi


env
cat /etc/hosts
cat /etc/zookeeper/conf/zoo.cfg
cat /var/lib/zookeeper/data/myid
which java
/usr/lib/zookeeper/bin/zkServer.sh start-foreground
