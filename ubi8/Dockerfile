FROM @BASE_IMAGE_NAME@

ADD bin/rpm-pkg-info.sh /tmp/rpm-pkg-info.sh

RUN sed -i -e 's|enabled=1|enabled=0|' /etc/dnf/plugins/subscription-manager.conf &&\
      dnf install -y bash && /tmp/rpm-pkg-info.sh BASE &&\
      dnf install -y automake bzip2 bzip2-libs bzip2-devel coreutils-single file \
      file-libs fontconfig freetype gcc-c++ libstdc++-static git glibc krb5-libs libaio \
      libcom_err libgomp libICE libidn \
      libSM libX11 libX11-devel libxcrypt libXcursor libXext \
      libXft libXi libXinerama \
      libXmu libXpm libXpm-devel libXrandr libXrender \
      java-1.8.0-openjdk-devel libtool m4 make \
      ncurses ncurses-libs ncurses-devel nspr nss nss-util \
      openssl openssl-devel openssl-libs \
      perl perl-interpreter perl-libs \
      perl-Carp perl-constant perl-Data-Dumper perl-DBI \
      perl-Digest-MD5 perl-Encode perl-Env perl-Exporter perl-ExtUtils-Embed \
      perl-File-Path perl-File-Temp perl-Getopt-Long perl-IO perl-libnet \
      perl-Memoize perl-PathTools perl-Scalar-List-Utils perl-Socket perl-Storable \
      perl-Term-ANSIColor perl-Test-Harness perl-Text-ParseWords perl-Thread-Queue \
      perl-Time-HiRes perl-Time-Local perl-YAML \
      patch popt python2 python3 readline rpm-build \
      rsync tcl time tk wget which zlib &&\
      bc tar zip unzip hostname nano procps-ng dnf-plugins-core python3-requests environment-modules &&\
    dnf install -y http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/centos-gpg-keys-8-3.el8.noarch.rpm &&\
    dnf install -y http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/centos-stream-repos-8-3.el8.noarch.rpm &&\
    dnf install -y epel-release &&\
    dnf install -y libnsl e2fsprogs e2fsprogs-libs libXext-devel libXft-devel \
      libglvnd-opengl mesa-libGLU mesa-libGLU-devel nss-devel perl-CGI \
      popt-devel readline-devel tcsh zsh tcl-devel tk-devel strace \
      voms-clients-cpp krb5-workstation python2-psutil myproxy apptainer python2-requests &&\
    dnf update -y ca-certificates &&\
    dnf config-manager --set-enabled powertools &&\
    ([ "@EXTRA_PACKAGES@" != "" ] && dnf -y install @EXTRA_PACKAGES@ || true) &&\
    alternatives --set python `which python2` &&\
    yum clean all

ADD share/krb5.conf /etc/krb5.conf
ADD share/ca-bundle.crt /etc/pki/tls/certs/ca-bundle.crt
ADD share/fix_ssh_config.sh /tmp/fix_ssh_config.sh
RUN mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /build /data /pool /opt/cms &&\
    touch /etc/tnsnames.ora &&\
    echo el8 > /etc/cmsos &&\
    /tmp/fix_ssh_config.sh /etc/ssh/ssh_config && rm -f /tmp/fix_ssh_config.sh &&\
    sed -i -e s'|^ *allow  *setuid.*|allow setuid = no|;s|^ *enable  *overlay.*|enable overlay = no|;s|^ *enable  *underlay.*|enable underlay = yes|' /etc/apptainer/apptainer.conf &&\
    /tmp/rpm-pkg-info.sh IMAGE
