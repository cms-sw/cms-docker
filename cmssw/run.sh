#!/bin/sh -ex

source /opt/cms/cmsset_default.sh
scram project CMSSW_7_3_0
cd CMSSW_7_3_0
eval `scram run -sh`
mkdir -p /data
cd /data
runTheMatrix.py ${WORKFLOW+-l $WORKFLOW} ${OPTIONS}
