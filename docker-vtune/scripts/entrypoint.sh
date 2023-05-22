#!/bin/sh
if [ ! -d /vtune/profiles ] ; then
  echo "ERROR: Missing /vtune/profiles directory."
  echo "       Please start docker with '-v <vtune_config_dir>:/vtune/profiles:z'"
  exit 1
fi

su vtune -c "$(which vtune-backend) --web-port 8080 --data-directory /vtune/profiles --allow-remote-access --no-https --suppress-automatic-help-tours --log-to-console"
