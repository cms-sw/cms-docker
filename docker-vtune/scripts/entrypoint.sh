#!/bin/sh
if [ ! -d /vtune/profiles ] ; then
  echo "ERROR: Missing /vtune/profiles directory."
  echo "       Please start docker with '-v <vtune_config_dir>:/vtune/profiles:z'"
  exit 1
fi
/etc/init.d/nginx start
su vtune -c "$(which vtune-server) --web-port 4000 --data-port 4040 --no-https --log-to-console --suppress-automatic-help-tours --log-level info --data-directory /vtune/profiles --base-url https://cmssdt.cern.ch/vtune/"
