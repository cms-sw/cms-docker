FROM @BASE_IMAGE_NAME@
RUN dnf install -y \
    automake bash bzip2 bzip2-libs bzip2-devel coreutils-single e2fsprogs e2fsprogs-libs \
    perl file file-libs fontconfig freetype gcc-c++ git glibc glibc-headers krb5-libs libaio \
    libcom_err libcom_err-devel libgomp libICE \
    libSM libX11 libX11-devel libxcrypt libXcursor libXext \
    libXext-devel libXft libXft-devel libXi libXinerama \
    libXmu libXpm libXpm-devel libXrandr libXrender \
    libglvnd-opengl mesa-libGL mesa-libGLU mesa-libGLU-devel \
    java-1.8.0-openjdk-devel libtool m4 make man-db \
    ncurses ncurses-libs ncurses-devel nspr nss nss-devel nss-util \
    openssl openssl-devel openssl-libs \
    patch popt popt-devel python3 readline readline-devel rpm-build \
    rsync tcl tcsh time tk wget which zlib zsh tcl-devel tk-devel krb5-devel \
    bc strace tar zip unzip hostname nano libnsl procps-ng environment-modules && \
    dnf install -y epel-release &&\
    dnf install -y @EPEL_PACKAGES@ xrootd-client gfal2-all gfal2-util-scripts \
      python3-requests python3-psutil dnf-plugins-core \
      voms-clients-cpp krb5-workstation myproxy singularity &&\
    dnf update -y ca-certificates &&\
    dnf --enablerepo=crb install -y texinfo &&\
    xcmd="@EXTRA_COMMAND@" &&\
    if [ "$xcmd" = "" ] ; then xcmd=true; fi &&\
    eval $xcmd &&\
    echo el9 > /etc/cmsos &&\
    dnf clean all

ADD fix_ssh_config.sh /tmp/fix_ssh_config.sh
RUN mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /build /data /pool /opt/cms &&\
    touch /etc/tnsnames.ora &&\
    echo el9 > /etc/cmsos &&\
    /tmp/fix_ssh_config.sh /etc/ssh/ssh_config && rm -f /tmp/fix_ssh_config.sh &&\
    sed -i -e s'|^ *allow  *setuid.*|allow setuid = no|;s|^ *enable  *overlay.*|enable overlay = no|;s|^ *enable  *underlay.*|enable underlay = yes|' /etc/apptainer/apptainer.conf
WORKDIR /build
