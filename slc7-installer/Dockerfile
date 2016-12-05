FROM cern/cc7-base

ADD http://linux.web.cern.ch/linux/centos7/CentOS-CERN.repo /etc/yum.repos.d/CentOS-CERN.repo
RUN chmod 755 /etc/yum.repos.d/CentOS-CERN.repo
ADD http://linuxsoft.cern.ch/cern/centos/7.1/os/x86_64/RPM-GPG-KEY-cern /tmp/RPM-GPG-KEY-cern
ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo

RUN /usr/bin/rpm --import /tmp/RPM-GPG-KEY-cern && /bin/rm /tmp/RPM-GPG-KEY-cern

RUN yum update -y && yum clean all

RUN yum update -y && yum install -y HEP_OSlibs_CC7 finger screen libXpm-devel libXft-devel krb5-devel subversion telnet readline-devel wget \
                                    glibc-devel.x86_64 mesa-libGL-devel.x86_64 mesa-libGLU-devel.x86_64 libXext-devel rsync tcsh zsh tcl tk \
                                    openssl e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu libXcursor libXrandr e2fsprogs-libs \
                                    libXi libXinerama tar perl-Data-Dumper perl-Digest-MD5 perl-Switch perl-Env perl-Thread-Queue bzip2 && \
                                    yum clean all
RUN groupadd -g 350 cvcmsib
RUN adduser -u 350 -g 350 cvcmsib
RUN groupadd -g 101 shared
RUN adduser -u 101 -g 101 shared
RUN yum update -y && yum install -y which file && yum clean all

USER shared

