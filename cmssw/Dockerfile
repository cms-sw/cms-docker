FROM cmssw/cmssw:CMSSW_base

USER    cmsinst
RUN     /bin/mkdir /opt/cms/COMP
WORKDIR /opt/cms
RUN     wget -O /opt/cms/bootstrap.sh http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh
ENV     SCRAM_ARCH=slc6_amd64_gcc530
RUN     sh /opt/cms/bootstrap.sh setup -r cms -architecture $SCRAM_ARCH -server cmsrep.cern.ch
RUN     source /opt/cms/$SCRAM_ARCH/external/apt/*/etc/profile.d/init.sh && apt-get install -y cms+local-cern-siteconf+sm111124 cms+cmssw+CMSSW_8_0_16 && apt-get clean

USER    root
RUN     /bin/cp -f /opt/cms/cmsset_default.sh  /etc/profile.d/
RUN     /bin/cp -f /opt/cms/cmsset_default.csh /etc/profile.d/
USER    cmsbld
