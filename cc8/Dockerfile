FROM @BASE_IMAGE_NAME@
RUN yum update -y && \
    yum install -y \
    automake bash bzip2 bzip2-libs bzip2-devel coreutils-single e2fsprogs e2fsprogs-libs \
    file file-libs fontconfig freetype gcc-c++ git glibc krb5-libs libaio \
    libcom_err libgomp libICE libidn \
    libSM libX11 libX11-devel libxcrypt libXcursor libXext \
    libXext-devel libXft libXft-devel libXi libXinerama \
    libXmu libXpm libXpm-devel libXrandr libXrender \
    libglvnd-opengl mesa-libGL mesa-libGLU mesa-libGLU-devel \
    java-1.8.0-openjdk-devel libtool m4 make \
    ncurses ncurses-libs ncurses-devel nspr nss nss-devel nss-util \
    openssl openssl-devel openssl-libs \
    perl perl-interpreter perl-libs \
    perl-Carp perl-CGI perl-constant perl-Data-Dumper perl-DBI \
    perl-Digest-MD5 perl-Encode perl-Env perl-Exporter perl-ExtUtils-Embed \
    perl-File-Path perl-File-Temp perl-Getopt-Long perl-IO perl-libnet \
    perl-Memoize perl-PathTools perl-Scalar-List-Utils perl-Socket perl-Storable \
    perl-Term-ANSIColor perl-Test-Harness perl-Text-ParseWords perl-Thread-Queue \
    perl-Time-HiRes perl-Time-Local perl-YAML \
    patch popt popt-devel python2 readline readline-devel rpm-build \
    rsync tcl tcsh time tk wget which zlib zsh \
    bc strace tar zip unzip hostname nano libnsl && \
    alternatives --set python `which python2` && \
    yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm && \
    yum install -y voms-clients-cpp krb5-workstation python2-psutil &&\
    yum clean all

ADD krb5.conf /etc/krb5.conf
ADD ca-bundle.crt /etc/pki/tls/certs/ca-bundle.crt
ADD fix_ssh_config.sh /tmp/fix_ssh_config.sh
RUN mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /build /data /pool /opt/cms &&\
    touch /etc/tnsnames.ora &&\
    /tmp/fix_ssh_config.sh /etc/ssh/ssh_config ; rm -f /tmp/fix_ssh_config.sh
WORKDIR /build
