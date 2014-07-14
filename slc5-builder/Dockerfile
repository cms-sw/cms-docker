FROM saltstack/centos-5-minimal

ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
RUN yum update -y
RUN yum install -y HEP_OSlibs_SL5
RUN adduser cmsbuild
RUN install -d /opt
RUN install -d -o cmsbuild /opt/cms
RUN yum install -y wget
RUN yum install -y rpm-build
RUN yum install -y which
ADD http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh /opt/cms/bootstrap.sh
RUN chmod 755 /opt/cms/bootstrap.sh
ENV SCRAM_ARCH slc5_amd64_gcc462
ENV VO_CMS_SW_DIR /opt/cms
USER cmsbuild
RUN sh -x $VO_CMS_SW_DIR/bootstrap.sh setup -path $VO_CMS_SW_DIR -arch $SCRAM_ARCH

