FROM centos:centos6

RUN     groupadd -g 500 cmsinst && adduser -u 500 -g 500 cmsinst && install -d /opt && install -d -o cmsinst /opt/cms
RUN     groupadd -g 501 cmsbld && adduser -u 501 -g 501 cmsbld
RUN     yum -y update  && yum -y install  wget git tcsh zsh tcl perl-ExtUtils-Embed perl-libwww-perl compat-libstdc++-33 libXmu  libXpm zip e2fsprogs \
        krb5-devel krb5-worstation  tk mesa-libGLU mesa-libGL compat-readline5 libXcursor libXrandr libXi libXinerama
RUN     yum -y install https://ecsft.cern.ch/dist/cvmfs/cvmfs-release/cvmfs-release-latest.noarch.rpm
RUN     yum -y install cvmfs cvmfs-config-default
RUN     /usr/bin/cvmfs_config setup
RUN     /bin/touch /etc/cvmfs/default.local && /bin/echo "CVMFS_REPOSITORIES=cms.cern.ch,grid.cern.ch" > /etc/cvmfs/default.local
RUN     /bin/echo "CVMFS_HTTP_PROXY=http://ca-proxy.cern.ch:3128" >> /etc/cvmfs/default.local
RUN     echo "#!/bin/bash" > /etc/profile.d/run.sh && echo "/sbin/service autofs restart" >> /etc/profile.d/run.sh
RUN     echo "/usr/bin/cvmfs_config probe" >> /etc/profile.d/run.sh
#RUN    echo 'if [ "X$CMS_CMD" = "X" ] ; then /bin/bash ; else $CMS_CMD ; fi' >> /etc/profile.d/run.sh
RUN     /bin/chmod +x /etc/profile.d/run.sh
RUN     wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.3/dumb-init_1.1.3_amd64
RUN     chmod +x /usr/local/bin/dumb-init
