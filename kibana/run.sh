#!/bin/sh -ex

# Use configuration from commandline.
KIBANA_ES=${KIBANA_ES-localhost:9200}
KIBANA_INDEX=${KIBANA_INDEX-kibana-int}

cat <<EOF >/kibana/config/kibana.yml
port: 5601
host: "0.0.0.0"
elasticsearch_url: ${KIBANA_ES-http://localhost:9200}
elasticsearch_preserve_host: true
kibana_index: ".kibana"
default_app_id: "${KIBANA_DEFAULT_APP-discover}"
request_timeout: 300000
shard_timeout: 0
bundled_plugin_ids:
 - plugins/dashboard/index
 - plugins/discover/index
 - plugins/doc/index
 - plugins/kibana/index
 - plugins/markdown_vis/index
 - plugins/metric_vis/index
 - plugins/settings/index
 - plugins/table_vis/index
 - plugins/vis_types/index
 - plugins/visualize/index
EOF
# Start the crontab and run nginx
cd /kibana
bin/kibana
