FROM cmssw/slc7-vanilla

ADD http://linux.web.cern.ch/linux/centos7/CentOS-CERN.repo /etc/yum.repos.d/CentOS-CERN.repo
RUN chmod 755 /etc/yum.repos.d/CentOS-CERN.repo
ADD http://linuxsoft.cern.ch/cern/centos/7.1/os/x86_64/RPM-GPG-KEY-cern /tmp/RPM-GPG-KEY-cern
ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
ADD krb5.conf /etc/krb5.conf

RUN /usr/bin/rpm --import /tmp/RPM-GPG-KEY-cern && /bin/rm /tmp/RPM-GPG-KEY-cern

RUN yum update -y && yum clean all

RUN yum update -y && yum install -y HEP_OSlibs_CC7 java-1.7.0-openjdk
RUN groupadd -g 777 cmsbuild
RUN adduser -g 777 -u 777 cmsbuild
RUN install -d -o cmsbuild /build
RUN yum update -y && yum install -y git-core
RUN yum update -y && yum install -y openssl \
                                    glibc-devel.x86_64 \
                                    mesa-libGL-devel.x86_64 \
                                    mesa-libGLU-devel.x86_64 \
                                    libXext-devel
RUN yum install -y tcsh zsh tcl tk e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu e2fsprogs-libs libXpm bc libaio
RUN yum install -y tar patch krb5-devel perl-Data-Dumper
RUN yum install -y gcc unzip zip perl-libwww-perl libXpm-devel libXft-devel svn cvs gcc-c++ strace cern-wrappers krb5-workstation 
RUN yum install -y wget hostname readline-devel
WORKDIR /build
USER cmsbuild
