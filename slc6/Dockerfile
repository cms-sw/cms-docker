FROM @BASE_IMAGE_NAME@

ADD slc6.repo /etc/yum.repos.d/slc6.repo 
ADD ca.repo /etc/yum.repos.d/ca.repo 
ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD GPG-KEY-EUGridPMA-RPM-3 /etc/pki/rpm-gpg/GPG-KEY-EUGridPMA-RPM-3

RUN yum update -y && \
    yum install -y http://linuxsoft.cern.ch/epel/epel-release-latest-6.noarch.rpm && \
    yum install -y git-core openssl glibc-devel.x86_64 mesa-libGL-devel.x86_64 mesa-libGLU-devel.x86_64 \
                   libXext-devel tcsh zsh tcl tk e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu e2fsprogs-libs \
                   libXpm bc libaio tar patch krb5-devel gcc unzip zip perl-libwww-perl libXpm-devel libXft-devel svn \
                   cvs gcc-c++ strace cern-wrappers krb5-workstation wget readline-devel nano bzip2 \
                   CERN-CA-certs tk-devel tcl-devel which python-pip file voms-clients-cpp \
                   java-1.8.0-openjdk java-1.8.0-openjdk-devel compat-readline5 libXcursor libXrandr libXinerama \
                   PyYAML python-requests-kerberos xz libxslt xrootd-client time && yum clean all
ADD krb5.conf /etc/krb5.conf
RUN mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /data /pool /build &&\
    touch /etc/tnsnames.ora
WORKDIR /build
