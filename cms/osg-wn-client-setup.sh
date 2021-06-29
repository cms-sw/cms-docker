#!/bin/sh
# Requested by Marco Mascheroni: To setuposg-wn-client env
# 29.6.2021
export CMS_SINGULARITYD_ENV="none"
if [[ "$SINGULARITY_CONTAINER" =~ ^/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel6(-itb)?$ ]] && [ -e "/cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.4/current/el6-x86_64/setup.sh" ]; then
    export CMS_SINGULARITYD_ENV="3.4/el6-x86_64"
    source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.4/current/el6-x86_64/setup.sh
elif [[ "$SINGULARITY_CONTAINER" =~ ^/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel7(-itb)?$ ]] && [ -e "/cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.4/current/el7-x86_64/setup.sh" ]; then
    export CMS_SINGULARITYD_ENV="3.4/el7-x86_64"
    source /cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/3.4/current/el7-x86_64/setup.sh
fi

