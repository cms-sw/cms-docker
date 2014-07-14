FROM arkii/centos65

ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
RUN yum update -y
RUN yum install -y HEP_OSlibs_SL6
RUN adduser cmsbuild
RUN install -d /opt
RUN install -d -o cmsbuild /opt/cms
RUN yum install -y wget
RUN yum install -y rpm-build
RUN yum install -y which
RUN yum install -y git
RUN yum install -y screen
ADD http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh /opt/cms/bootstrap.sh
RUN chmod 755 /opt/cms/bootstrap.sh
ENV SCRAM_ARCH slc5_amd64_gcc462
ENV VO_CMS_SW_DIR /opt/cms
RUN install -d -o cmsbuild /build
WORKDIR /build
USER cmsbuild
