#!/bin/sh
if [ ! -d /vtune/profiles ] ; then
  echo "ERROR: Missing /vtune/profiles directory."
  echo "       Please start docker with '-v <vtune_config_dir>:/vtune/profiles:z'"
  exit 1
fi

su vtune -c "$(which vtune-backend) --web-port 8080 --data-directory /vtune/profiles --allow-remote-access --tls-certificate /etc/httpd/conf/apache-cert.pem --tls-certificate-key /etc/httpd/conf/apache-key.pem"
