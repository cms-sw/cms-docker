FROM @BASE_IMAGE_NAME@

RUN dnf install -y automake bzip2 bzip2-libs bzip2-devel coreutils-single e2fsprogs \
    e2fsprogs-libs perl file file-libs fontconfig freetype gcc-c++ git glibc krb5-libs \
    libaio libcom_err libcom_err-devel libgomp libICE \
    libSM libX11 libX11-devel libxcrypt libXcursor libXext \
    libXext-devel libXft libXft-devel libXi libXinerama \
    libXmu libXpm libXpm-devel libXrandr libXrender \
    libglvnd-opengl mesa-libGL mesa-libGLU mesa-libGLU-devel \
    java-1.8.0-openjdk-devel java-11-openjdk-devel java-17-openjdk-devel libtool m4 make \
    ncurses ncurses-libs ncurses-devel nspr nss nss-devel nss-util \
    openssl openssl-devel openssl-libs sssd-client \
    patch popt popt-devel python3 readline readline-devel rpm-build \
    rsync tcl tcsh time tk wget which zlib zsh tcl-devel tk-devel krb5-devel \
    bc strace tar zip unzip hostname nano libnsl procps-ng environment-modules && \
    dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm &&\
    dnf install -y voms-clients-cpp krb5-workstation python3-psutil myproxy apptainer \
        python3-requests openldap-compat python3-cryptography jq &&\
    dnf update -y ca-certificates &&\
    dnf install -y dnf-plugins-core &&\
    ([ "@EXTRA_PACKAGES@" != "" ] && dnf -y install @EXTRA_PACKAGES@ || true) &&\
    yum clean all

ADD share/fix_ssh_config.sh /tmp/fix_ssh_config.sh
RUN mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /build /data /pool /opt/cms &&\
    touch /etc/tnsnames.ora &&\
    echo el9 > /etc/cmsos &&\
    /tmp/fix_ssh_config.sh /etc/ssh/ssh_config && rm -f /tmp/fix_ssh_config.sh &&\
    sed -i -e s'|^ *allow  *setuid.*|allow setuid = no|;s|^ *enable  *overlay.*|enable overlay = no|;s|^ *enable  *underlay.*|enable underlay = yes|' /etc/apptainer/apptainer.conf
WORKDIR /build
