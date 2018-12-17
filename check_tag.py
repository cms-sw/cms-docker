#!/usr/bin/env python
import json, sys
from commands import getstatusoutput as run_cmd

e, o = run_cmd('curl --silent -f -lSL https://index.docker.io/v1/repositories/%s/tags' % sys.argv[1])
if e:
  print o
  sys.exit(1)

data=json.loads(o)
for container in data:
  if container['name']==sys.argv[2]:
    print "FOUND:%s" % sys.argv[2]
    break

sys.exit(0)
