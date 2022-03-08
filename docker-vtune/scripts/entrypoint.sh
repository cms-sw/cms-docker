#!/bin/sh
if [ $# -lt 1 ] ; then
  echo "you must specify the public_ip_address and at least one version name for your source code"
  exit 1
fi


if [ ! -d /vtune/profiles ] ; then
  echo "ERROR: Missing /vtune/profiles directory."
  echo "       Please start docker with '-v <vtune_config_dir>:/vtune/profiles:z'"
#  exit 1
fi

find /vtune

echo $@
public_ip=$1
sed -i.bak s/public_ip_address/$1/g /home/vtune/config.yml

cp /home/vtune/config.yml /opt/intel/oneapi/vtune/latest/backend/config.yml
su vtune -c "$(which vtune-backend) --web-port 8080 --data-directory /vtune/profiles --allow-remote-access --log-to-console --log-level debug"
