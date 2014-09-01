FROM arkii/centos65

ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
RUN yum update -y
RUN yum install -y HEP_OSlibs_SL6
RUN adduser cmsbuild
RUN install -d /opt
RUN install -d -o cmsbuild /opt/cms
RUN yum install -y wget rpm-build which git screen e2fsprogs
ADD http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh /opt/cms/bootstrap.sh
RUN chmod 755 /opt/cms/bootstrap.sh
ENV SCRAM_ARCH slc6_amd64_gcc481
ENV VO_CMS_SW_DIR /opt/cms
RUN install -d -o cmsbuild /build
WORKDIR /build
USER cmsbuild
RUN /opt/cms/bootstrap.sh -a $SCRAM_ARCH -path /opt/cms setup
RUN source /opt/cms/slc6_amd64_gcc481/external/apt/0.5.16/etc/profile.d/init.sh && apt-get install cms+local-cern-siteconf+sm111124
USER root
RUN cp /opt/cms/slc6_amd64_gcc481/external/apt/0.5.16/etc/profile.d/init.* /etc/profile.d
RUN cp /opt/cms/cmsset_default.* /etc/profile.d
WORKDIR /build
USER cmsbuild

CMD /bin/bash --login
