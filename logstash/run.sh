if [ X$LOGSTASH_CONFIG = X ]; then
  echo Please specify a logstash config adding -e LOGSTASH_CONFIG=XXX
  exit 1
fi
cp $LOGSTASH_CONFIG /logstash.conf
sed -i -e "s/[@]ES_HOSTNAME[@]/$ES_HOSTNAME/" /logstash.conf
sed -i -e "s/[@]ES_PORT[@]/$ES_PORT/" /logstash.conf

if [ ! "X$DEBUG" = X ]; then
  echo 'output {stdout { codec => rubydebug }}' >> /logstash.conf
fi

/opt/logstash/bin/logstash -f /logstash.conf
