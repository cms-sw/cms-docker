FROM centos:centos6

ENV SCRAM_ARCH slc6_amd64_gcc481
ENV VO_CMS_SW_DIR /opt/cms

ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
ADD http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh /opt/bootstrap.sh

RUN yum update -y && yum install -y HEP_OSlibs_SL6 wget rpm-build which git screen e2fsprogs
RUN adduser cmsbuild
RUN install -d /opt
RUN install -d -o cmsbuild /opt/cms

RUN install -d -o cmsbuild /build
WORKDIR /build
USER cmsbuild
RUN sh -x /opt/bootstrap.sh -a $SCRAM_ARCH -path /opt/cms setup
RUN source /opt/cms/slc6_amd64_gcc481/external/apt/0.5.16/etc/profile.d/init.sh && apt-get install cms+local-cern-siteconf+sm111124
USER root
RUN cp /opt/cms/slc6_amd64_gcc481/external/apt/0.5.16/etc/profile.d/init.* /etc/profile.d
RUN cp /opt/cms/cmsset_default.* /etc/profile.d
# We save the installation so that we can start from there when passing a new installation volume via -v.
RUN rsync -av /opt/cms/ /opt/cms.safe/
WORKDIR /opt/cms

# Before starting the shell we copy the bootstrap area in place so that if
# /opt/cms was overridded by a volume, we have the installation available
# immediately.
CMD rsync -av /opt/cms.safe/ /opt/cms/  && chown -R cmsbuild /opt/cms && su - cmsbuild
