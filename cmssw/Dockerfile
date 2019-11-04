FROM @BASE_IMAGE_NAME@

RUN     groupadd -g 500 cmsinst && \
        adduser -u 500 -g 500 cmsinst && \
        /bin/mkdir -p /opt/cms && \
        chown cmsinst:cmsinst -R /opt/cms

RUN     su - cmsinst sh -c "cd /opt/cms &&\
        wget -q -O /opt/cms/bootstrap.sh http://cmsrep.cern.ch/cmssw/repos/bootstrap.sh &&\
        sh /opt/cms/bootstrap.sh setup -r cms -architecture @SCRAM_ARCH@ -server cmsrep.cern.ch &&\
        /opt/cms/common/cmspkg -a @SCRAM_ARCH@ install -y cms+local-cern-siteconf+sm111124 &&\
        /opt/cms/common/cmspkg -a @SCRAM_ARCH@ install -y cms+cmssw+@IMAGE_TAG@ &&\
        /opt/cms/common/cmspkg -a @SCRAM_ARCH@ clean"

RUN     /bin/cp -f /opt/cms/cmsset_default.sh  /etc/profile.d/ && \
        /bin/cp -f /opt/cms/cmsset_default.csh /etc/profile.d/
