FROM cmssw/slc6-base

ARG SCRAM_ARCH=slc6_amd64_gcc472
USER    cmsinst
WORKDIR /opt/cms
RUN     wget -O /opt/cms/bootstrap.sh http://cmsrep.cern.ch/cmssw/repos/bootstrap.sh
RUN     sh /opt/cms/bootstrap.sh setup -r cms -architecture $SCRAM_ARCH -server cmsrep.cern.ch 
RUN     /opt/cms/common/cmspkg -a $SCRAM_ARCH install -y cms+local-cern-siteconf+sm111124
ARG     CMSSW_VERSION=CMSSW_5_3_38
RUN     /opt/cms/common/cmspkg -a $SCRAM_ARCH install -y cms+cmssw+$CMSSW_VERSION
RUN     /opt/cms/common/cmspkg -a $SCRAM_ARCH clean

USER    root
RUN     /bin/cp -f /opt/cms/cmsset_default.sh  /etc/profile.d/
RUN     /bin/cp -f /opt/cms/cmsset_default.csh /etc/profile.d/
USER    cmsbld
