#!/bin/bash
# Requested by Marco Mascheroni: To setup osg-wn-client env
# 17.8.2021
export CMS_SINGULARITYD_ENV="none"
ARCH=$(uname -i)
if [[ "$ARCH" != "x86_64" ]]; then
    # Only have x86_64 in /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.6/current/
    return 0
fi
if [[ -f "/image-source-info.txt" ]]; then
    OSG_VERSION=$(cat /image-source-info.txt | cut -d: -f3 | cut -d- -f1)
    OS_VERSION=$(cat /image-source-info.txt | cut -d: -f3 | cut -d- -f2)
    export CMS_SINGULARITYD_ENV="$OSG_VERSION/$OS_VERSION-x86_64"
    source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/$OSG_VERSION/current/$OS_VERSION-x86_64/setup.sh
    return 0 # Ignore failures during source
fi
