FROM cmssw/cmssw:CMSSW_8_0_16
USER    cmsinst
ENV     SCRAM_ARCH=slc6_amd64_gcc481
RUN     sh /opt/cms/bootstrap.sh setup -r cms -architecture $SCRAM_ARCH -server cmsrep.cern.ch
RUN     source /opt/cms/$SCRAM_ARCH/external/apt/*/etc/profile.d/init.sh && apt-get install -y cms+local-cern-siteconf+sm111124 cms+cmssw+CMSSW_7_1_24 && apt-get clean

USER    root
RUN     chown cmsinst:cmsinst /opt/cms/COMP

USER    cmsbld

