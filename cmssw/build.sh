#!/bin/bash -ex
cd $(dirname $0)

if [ "$1" = "" ] ; then
  echo "Usage: $0 <CMSSW_VERSION>"
  exit 1
fi
CMSSW_VERSION=$1
DockerFile="Dockerfile.${CMSSW_VERSION}"
if [ ! -f ${DockerFile} ] ; then
  RELDATA=$(curl -s https://raw.githubusercontent.com/cms-sw/cms-bot/master/releases.map | grep "=$CMSSW_VERSION;" | grep 'prodarch=1')
  ITEM_COUNT=$(echo "$RELDATA" | tr ';' '\n' | grep 'architecture=' | wc -l)
  if [ $ITEM_COUNT -eq 0 ] ; then
    echo "ERROR: Unable to find Release $CMSSW_VERSION in https://github.com/cms-sw/cms-bot/blob/master/releases.map"
    exit 1
  elif [ $ITEM_COUNT -gt 1 ] ; then
    echo "ERROR: Multiple entries found for $CMSSW_VERSION in https://github.com/cms-sw/cms-bot/blob/master/releases.map"
    exit 1
  fi
  eval "$RELDATA"
  BASE_IMG="cmssw/cms:rhel6"
  case $architecture in
    slc6_* ) BASE_IMG="cmssw/cms:rhel6-m20200612" ;;
    slc7_* ) BASE_IMG="cmssw/cms:rhel7-m20200615" ;;
  esac
  cp Dockerfile.tmpl ${DockerFile}
  sed -i -e "s|@BASE_IMAGE_NAME@|${BASE_IMG}|;s|@SCRAM_ARCH@|${architecture}|g;s|@IMAGE_TAG@|$1|g" ${DockerFile}
  if [ $(echo $CMSSW_VERSION | grep _patch | wc -l) -gt 0 ] ; then
    sed -i -e 's|cms+cmssw+|cms+cmssw-patch+|' ${DockerFile}
  fi
fi

docker build -f ${DockerFile} -t cmssw/cmssw:$CMSSW_VERSION .
