#!/bin/bash -ex
whoami
cd $WORKSPACE
wget http://cmsrep.cern.ch/cmssw/bootstrap.sh
for gcc in gcc493 gcc530 gcc630 gcc700 ; do
  sh ./bootstrap.sh -a slc7_amd64_$gcc setup
done
echo ALL_OK
