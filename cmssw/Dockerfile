FROM centos:centos6

ADD     RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD     GPG-KEY-EUGridPMA-RPM-3 /etc/pki/rpm-gpg/GPG-KEY-EUGridPMA-RPM-3
ADD     HEP_OSlibs.repo  /etc/yum.repos.d/HEP_OSlibs.repo
ADD     carepo.repo      /etc/yum.repos.d/carepo.repo
ADD     slc6-os.repo     /etc/yum.repos.d/slc6-os.repo
ADD     krb5.conf        /etc/krb5.conf

RUN     yum update -y && yum install -y HEP_OSlibs_SL6 wget git \
 tcsh zsh tcl \
 perl-ExtUtils-Embed perl-libwww-perl \
 compat-libstdc++-33 \
 libXmu  libXpm \
 zip e2fsprogs \
 CERN-CA-certs voms-clients-cpp ca-policy-lcg \
 krb5-devel cern-wrappers krb5-workstation \
 strace

RUN     groupadd -g 500 cmsinst && adduser -u 500 -g 500 cmsinst && install -d /opt && install -d -o cmsinst /opt/cms
RUN     groupadd -g 501 cmsbld && adduser -u 501 -g 501 cmsbld
USER    cmsinst
WORKDIR /opt/cms
RUN     wget -O /opt/cms/bootstrap.sh http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh
ENV     SCRAM_ARCH=slc6_amd64_gcc530
RUN     sh /opt/cms/bootstrap.sh setup -r cms -architecture $SCRAM_ARCH -server cmsrep.cern.ch
RUN     source /opt/cms/$SCRAM_ARCH/external/apt/*/etc/profile.d/init.sh && apt-get install -y cms+local-cern-siteconf+sm111124 cms+cmssw+CMSSW_8_0_4 && apt-get clean
USER    root
RUN     /bin/cp -f /opt/cms/cmsset_default.sh  /etc/profile.d/
RUN     /bin/cp -f /opt/cms/cmsset_default.csh /etc/profile.d/
RUN     rpm -i http://research.cs.wisc.edu/htcondor/yum/stable/rhel6/condor-external-libs-8.4.2-1.el6.i686.rpm
RUN     rpm -i http://research.cs.wisc.edu/htcondor/yum/stable/rhel6/condor-external-libs-8.4.2-1.el6.x86_64.rpm
USER    cmsbld
