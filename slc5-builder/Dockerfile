FROM cmssw/slc5-vanilla

RUN yum update -y && yum install -y HEP_OSlibs_SL5
RUN adduser cmsbuild
RUN install -d /opt
RUN install -d -o cmsbuild /opt/cms
RUN yum install -y wget \
                   rpm-build \
                   which \
                   git \
                   screen
ADD http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh /opt/cms/bootstrap.sh
RUN chmod 755 /opt/cms/bootstrap.sh
ENV SCRAM_ARCH slc5_amd64_gcc462
ENV VO_CMS_SW_DIR /opt/cms
RUN install -d -o cmsbuild /build
RUN yum install -y java-1.7.0-openjdk
RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm
RUN yum update -y && yum install -y git-core
ADD scram.sh /etc/profile.d/scram.sh
WORKDIR /build
USER cmsbuild
