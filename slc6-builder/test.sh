#!/bin/bash -ex
whoami
cd $WORKSPACE
wget http://cmsrep.cern.ch/cmssw/bootstrap.sh
for gcc in gcc472 gcc481 gcc491 gcc493 gcc530 gcc630 gcc700 ; do
  sh ./bootstrap.sh -a slc6_amd64_$gcc setup
done
echo ALL_OK
