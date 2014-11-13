FROM centos:centos6

ENV SCRAM_ARCH slc6_amd64_gcc481

ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
ADD http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh /opt/bootstrap.sh

RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum update -y && yum install -y HEP_OSlibs_SL6 wget rpm-build which git screen e2fsprogs python-pip jq
RUN adduser cmsbuild
RUN install -d -o cmsbuild /build
RUN pip install pygithub

RUN yum install -y strace vim svn

WORKDIR /build
USER cmsbuild

RUN git clone https://github.com/ktf/cms-bot.git #c
RUN git clone https://github.com/cms-sw/pkgtools.git
#RUN git clone https://github.com/cms-sw/cmsdist.git

# Before starting the shell we copy the bootstrap area in place so that if
# /opt/cms was overridded by a volume, we have the installation available
# immediately.
CMD sh -ex /build/cms-bot/cms-externals-pr-test -a $SCRAM_ARCH -q $RELEASE_QUEUE ${FINAL_PACKAGE+-fp $FINAL_PACKAGE} ${JOBS+-j $JOBS} -pr $PR ${CMSDIST_PR+-cpr $CMSDIST_PR}
