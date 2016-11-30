FROM centos:centos6

RUN     groupadd -g 500 cmsinst && adduser -u 500 -g 500 cmsinst && install -d /opt && install -d -o cmsinst /opt/cms
RUN     groupadd -g 501 cmsbld && adduser -u 501 -g 501 cmsbld
RUN     yum -y update  && yum -y install HEP_OSlibs_SL6 wget git tcsh zsh tcl perl-ExtUtils-Embed perl-libwww-perl compat-libstdc++-33 libXmu  libXpm zip e2fsprogs \
        krb5-devel krb5-worstation  tk mesa-libGLU mesa-libGL compat-readline5 libXcursor libXrandr libXi libXinerama
RUN     yum -y update  && yum -y install CERN-CA-certs voms-clients-cpp ca-policy-lcg
RUN     wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.3/dumb-init_1.1.3_amd64
RUN     chmod +x /usr/local/bin/dumb-init
ENTRYPOINT ["/usr/local/bin/dumb-init", "-c", "--" ]

