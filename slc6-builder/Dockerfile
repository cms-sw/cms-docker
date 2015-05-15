FROM centos:centos6

ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo

RUN yum update -y && yum install -y HEP_OSlibs_SL6 wget rpm-build which git screen e2fsprogs
RUN groupadd -g 777 cmsbuild
RUN adduser -u 777 -g 777 cmsbuild && install -d /opt && install -d -o cmsbuild /opt/cms /build

RUN yum install -y tcsh \
                   zsh \
                   tcl \
                   tk \
                   e2fsprogs \
                   perl-ExtUtils-Embed \
                   compat-libstdc++-33 \
                   libXmu \
                   e2fsprogs-libs \
                   libXpm \
                   java-1.7.0-openjdk \
                   bc

WORKDIR /build
USER cmsbuild
