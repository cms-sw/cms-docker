#!/bin/sh -ex

# Use configuration from commandline.

KIBANA_ES=${KIBANA_ES-localhost:9200}
KIBANA_DEFAULT_ROUTE=${KIBANA_DEFAULT_ROUTE-/dashboard/file/default.json}
KIBANA_INDEX=${KIBANA_INDEX-kibana-int}

cat <<EOF >/usr/share/nginx/html/kibana/config.js
define(['settings'],
function (Settings) {
  return new Settings({
    elasticsearch: window.location.protocol + "//${KIBANA_ES}",
    default_route     : '${KIBANA_DEFAULT_ROUTE}',
    kibana_index: "${KIBANA_INDEX}",
    panel_names: [
      'histogram',
      'map',
      'goal',
      'table',
      'filtering',
      'timepicker',
      'text',
      'hits',
      'column',
      'trends',
      'bettermap',
      'query',
      'terms',
      'stats',
      'sparklines'
    ]
  });
});
EOF
# Start the crontab and run nginx
nginx 
