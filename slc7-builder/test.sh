#!/bin/bash -ex
ARCH="amd64"
GCC_VER="gcc493 gcc530 gcc630 gcc700"
if [ $(uname -m) = "aarch64" ] ; then 
  ARCH="aarch64"
  GCC_VER="gcc700"
fi
whoami
cd $WORKSPACE
wget http://cmsrep.cern.ch/cmssw/bootstrap.sh
for gcc in ${GCC_VER} ; do
  sh ./bootstrap.sh -a slc7_${ARCH}_${gcc} setup
done
echo ALL_OK
