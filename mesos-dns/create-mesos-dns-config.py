#!/usr/bin/env python
from os import getenv
import json

CONFIG = {
  "masters": getenv("MESOS_DNS_MASTERS", "127.0.0.1:5050").split(";"),
  "refreshSeconds": int(getenv("MESOS_DNS_REFRESH", "60")),
  "ttl": int(getenv("MESOS_DNS_TTL", "60")),
  "domain": getenv("MESOS_DNS_DOMAIN", "mesos"),
  "port": int(getenv("MESOS_DNS_PORT", "53")),
  "resolvers": getenv("MESOS_DNS_RESOLVERS", "8.8.8.8").split(";"),
  "email": getenv("MESOS_DNS_EMAIL", "root.mesos-dns"),
  "timeout": int(getenv("MESOS_DNS_TIMEOUT", "5"))
}

if __name__ == "__main__":
  file("/config.json", "w").write(json.dumps(CONFIG)) 
