FROM centos:centos6

ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo

RUN yum update -y && yum clean all

RUN yum update -y && yum install -y HEP_OSlibs_SL6 finger screen libXpm-devel libXft-devel krb5-devel subversion telnet readline-devel wget \
                                    glibc-devel.x86_64 mesa-libGL-devel.x86_64 mesa-libGLU-devel.x86_64 libXext-devel rsync tcsh zsh tcl tk \
                                    openssl e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu libXcursor libXrandr e2fsprogs-libs \
                                    libXi libXinerama tar perl-Data-Dumper perl-Digest-MD5 perl-Switch perl-Env perl-Thread-Queue
RUN groupadd -g 101 shared
RUN adduser -u 101 -g 101 shared

USER shared

