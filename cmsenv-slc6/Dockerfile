FROM centos:centos6

ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD GPG-KEY-EUGridPMA-RPM-3 /etc/pki/rpm-gpg/GPG-KEY-EUGridPMA-RPM-3
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
ADD carepo.repo /etc/yum.repos.d/carepo.repo

RUN     yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
RUN     yum -y install https://repo.grid.iu.edu/osg/3.3/osg-3.3-el6-release-latest.rpm
RUN     yum -y install yum-plugin-priorities

RUN     yum clean all && yum makecache && yum -y upgrade
RUN     yum -y install osg-wn-client
RUN     yum -y install HEP_OSlibs_SL6 CERN-CA-certs git zip
RUN     yum clean all
RUN     wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.3/dumb-init_1.1.3_amd64
RUN     chmod +x /usr/local/bin/dumb-init
ENTRYPOINT ["/usr/local/bin/dumb-init", "-c", "--" ]

