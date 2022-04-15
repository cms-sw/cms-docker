FROM @BASE_IMAGE_NAME@
RUN dnf install -y \
    automake bash bzip2 bzip2-libs bzip2-devel coreutils-single e2fsprogs e2fsprogs-libs \
    perl file file-libs fontconfig freetype gcc-c++ git glibc krb5-libs libaio \
    libcom_err libcom_err-devel libgomp libICE \
    libSM libX11 libX11-devel libxcrypt libXcursor libXext \
    libXext-devel libXft libXft-devel libXi libXinerama \
    libXmu libXpm libXpm-devel libXrandr libXrender \
    libglvnd-opengl mesa-libGL mesa-libGLU mesa-libGLU-devel \
    java-1.8.0-openjdk-devel libtool m4 make \
    ncurses ncurses-libs ncurses-devel nspr nss nss-devel nss-util \
    openssl openssl-devel openssl-libs \
    patch popt popt-devel python3 readline readline-devel rpm-build \
    rsync tcl tcsh time tk wget which zlib zsh tcl-devel tk-devel krb5-devel \
    bc strace tar zip unzip hostname nano libnsl procps-ng && \
    dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm &&\
    dnf install -y voms-clients-cpp krb5-workstation python3-psutil myproxy singularity \
        python3-requests &&\
    dnf update -y ca-certificates &&\
    dnf install -y dnf-plugins-core &&\
    ([ "@EXTRA_PACKAGES@" != "" ] && dnf -y install @EXTRA_PACKAGES@ || true) &&\
    dnf clean all

ADD fix_ssh_config.sh /tmp/fix_ssh_config.sh
RUN mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /build /data /pool /opt/cms &&\
    touch /etc/tnsnames.ora &&\
    echo el9 > /etc/cmsos &&\
    /tmp/fix_ssh_config.sh /etc/ssh/ssh_config && rm -f /tmp/fix_ssh_config.sh &&\
    sed -i -e s'|^ *allow  *setuid.*|allow setuid = no|;s|^ *enable  *overlay.*|enable overlay = no|;s|^ *enable  *underlay.*|enable underlay = yes|' /etc/singularity/singularity.conf
WORKDIR /build
