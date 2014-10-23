FROM centos:centos6

ENV SCRAM_ARCH slc6_amd64_gcc481
ENV VO_CMS_SW_DIR /opt/cms

ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
ADD http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh /opt/bootstrap.sh

RUN yum update -y && yum install -y HEP_OSlibs_SL6 wget rpm-build which git screen e2fsprogs
RUN adduser cmsbuild && install -d /opt && install -d -o cmsbuild /opt/cms /build
RUN chmod 775 /opt/bootstrap.sh

WORKDIR /build
USER cmsbuild
RUN /bin/sh -x /opt/bootstrap.sh -a $SCRAM_ARCH -path /opt/cms setup
RUN source /opt/cms/slc6_amd64_gcc481/external/apt/0.5.16/etc/profile.d/init.sh && apt-get install cms+local-cern-siteconf+sm111124
USER root
RUN cp /opt/cms/slc6_amd64_gcc481/external/apt/0.5.16/etc/profile.d/init.* /etc/profile.d
RUN cp /opt/cms/cmsset_default.* /etc/profile.d
USER cmsbuild

CMD login
