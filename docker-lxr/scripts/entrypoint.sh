#!/bin/sh

if [ ! -d /var/lib/mysql/lxr ] ; then
  if [ ! -d /host/mysql ] ; then
    echo "ERROR: MySQL database is not initialize yet."
    echo "       Please start docker with '-v <host_mysql_dir>:/host/mysql:z'"
    exit 1
  fi
  service mysql start
  expect /lxr/expect_initdb
  service mysql stop
  rsync -a /var/lib/mysql/ /host/mysql/
  exit 0
fi

if [ $# -lt 1 ] ; then
  echo "you must specify the public_ip_address and at least one version name for your source code"
  exit 1
fi

if [ ! -d /lxr/glimpse_index ] ; then
  echo "ERROR: Missing /lxr/glimpse_index directory."
  echo "       Please start docker with '-v <host_glimpse_index>:/lxr/glimpse_index:z'"
  exit 1
fi

for conf_file in versions default sourceroot ; do
  if [ ! -e /lxr/host_config/${conf_file} ] ; then
    echo "ERROR: Missing /lxr/host_config/${conf_file} file."
    echo "       Please start docker with '-v <host_config_dir>/host_config:/lxr/host_config:Z'"
    exit 1
  fi
done

echo $@
public_ip=$1
sed -i.bak s/public_ip_address/$1/g /lxr/custom.d/apache-lxrserver.conf

cp /lxr/custom.d/apache-lxrserver.conf  /etc/apache2/conf-available
a2enconf apache-lxrserver.conf

echo Creating glimpse index version directories
su lxr -c "mkdir -p /lxr/glimpse_index/lxr"
for ver in $(cat /lxr/host_config/versions) ; do
  su lxr -c "mkdir -p /lxr/glimpse_index/lxr/$ver"
done

service mysql start
service apache2 start

cd /lxr
exec "/bin/bash"
