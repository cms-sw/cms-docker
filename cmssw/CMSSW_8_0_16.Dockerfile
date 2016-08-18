FROM centos:centos6

ADD     krb5.conf        /etc/krb5.conf
RUN     rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
RUN     rpm -Uvh https://repo.grid.iu.edu/osg/3.3/osg-3.3-el6-release-latest.rpm
RUN     yum -y install yum-plugin-priorities
RUN     yum -y install osg-ca-certs
RUN     yum -y install osg-wn-client
RUN     yum update -y && yum install -y HEP_OSlibs_SL6 wget git \
 tcsh zsh tcl \
 perl-ExtUtils-Embed perl-libwww-perl \
 compat-libstdc++-33 \
 libXmu  libXpm \
 zip e2fsprogs \
 CERN-CA-certs voms-clients-cpp ca-policy-lcg \
 krb5-devel cern-wrappers krb5-workstation \
 strace
RUN     yum -y install tk compat-readline5 mesa-libGLU mesa-libGL
RUN      yum clean all
RUN     groupadd -g 500 cmsinst && adduser -u 500 -g 500 cmsinst && install -d /opt && install -d -o cmsinst /opt/cms
RUN     groupadd -g 501 cmsbld && adduser -u 501 -g 501 cmsbld
RUN     /bin/mkdir /opt/cms/COMP

USER    cmsinst
WORKDIR /opt/cms
RUN     wget -O /opt/cms/bootstrap.sh http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh
ENV     SCRAM_ARCH=slc6_amd64_gcc530
RUN     sh /opt/cms/bootstrap.sh setup -r cms -architecture $SCRAM_ARCH -server cmsrep.cern.ch
RUN     source /opt/cms/$SCRAM_ARCH/external/apt/*/etc/profile.d/init.sh && apt-get install -y cms+local-cern-siteconf+sm111124 cms+cmssw+CMSSW_8_0_16 && apt-get clean

ENV     SCRAM_ARCH=slc6_amd64_gcc481
RUN     sh /opt/cms/bootstrap.sh setup -r cms -architecture $SCRAM_ARCH -server cmsrep.cern.ch
RUN     source /opt/cms/$SCRAM_ARCH/external/apt/*/etc/profile.d/init.sh && apt-get install -y cms+local-cern-siteconf+sm111124 cms+cmssw+CMSSW_7_1_24 && apt-get clean

USER    root
RUN     /bin/cp -f /opt/cms/cmsset_default.sh  /etc/profile.d/
RUN     /bin/cp -f /opt/cms/cmsset_default.csh /etc/profile.d/
USER    cmsbld

