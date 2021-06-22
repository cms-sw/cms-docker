#!/bin/sh
# Requested by Marco Mascheroni: To setuposg-wn-client env
export TEST_VARIABLE="test"
if [[ $GLIDEIN_Factory == "CERN-ITB" ]]; then
    if [[ "$GWMS_SINGULARITY_IMAGE_HUMAN" =~ ^/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel6(-itb)?$ ]] && [ -e "/cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.4/current/el6-x86_64/setup.sh" ]; then
        source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.4/current/el6-x86_64/setup.sh
    elif [[ "$GWMS_SINGULARITY_IMAGE_HUMAN" =~ ^/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel7(-itb)?$ ]] && [ -e "/cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.4/current/el7-x86_64/setup.sh" ]; then
        source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.4/current/el7-x86_64/setup.sh
    fi
fi
