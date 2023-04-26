FROM @BASE_IMAGE_NAME@
LABEL maintainer="CMS Build"
LABEL name="CMS Worker Node on EL"

ADD CERN.repo               /tmp/CERN.repo
ADD RPM-GPG-KEY-kojiv2      /tmp/RPM-GPG-KEY-kojiv2
ADD fix_ssh_config.sh       /tmp/fix_ssh_config.sh

RUN dnf install -y \
    automake bash bzip2 bzip2-libs bzip2-devel coreutils-single e2fsprogs e2fsprogs-libs \
    perl file file-libs fontconfig freetype gcc-c++ git glibc glibc-headers krb5-libs libaio \
    libcom_err libcom_err-devel libgomp libICE \
    libSM libX11 libX11-devel libxcrypt libXcursor libXext \
    libXext-devel libXft libXft-devel libXi libXinerama \
    libXmu libXpm libXpm-devel libXrandr libXrender \
    libglvnd-opengl mesa-libGL mesa-libGLU mesa-libGLU-devel \
    java-1.8.0-openjdk-devel libtool m4 make cmake man-db \
    ncurses ncurses-libs ncurses-devel nspr nss nss-devel nss-util \
    openssl openssl-devel openssl-libs \
    patch popt popt-devel python3 readline readline-devel rpm-build \
    rsync tcl tcsh time tk wget which zlib zsh tcl-devel tk-devel krb5-devel \
    bc strace tar zip unzip hostname nano libnsl procps-ng environment-modules && \
    dnf install -y epel-release &&\
    dnf install -y @EPEL_PACKAGES@ xrootd-client \
      python3-requests python3-psutil dnf-plugins-core \
      voms-clients-cpp krb5-workstation myproxy apptainer &&\
    dnf install -y gfal2-all gfal2-util-scripts python3-gfal2-util &&\
    dnf install -y java-11-openjdk-devel xauth xdg-utils vim &&\
    dnf --enablerepo=crb install -y texinfo &&\
    xcmd="@EXTRA_COMMAND@" &&\
    if [ "$xcmd" = "" ] ; then xcmd=true; fi &&\
    eval $xcmd &&\
    echo el9 > /etc/cmsos &&\
    cp /tmp/CERN.repo /etc/yum.repos.d/CERN.repo &&\
    rpm --import /tmp/RPM-GPG-KEY-kojiv2 &&\
    dnf install -y cern-gpg-keys CERN-CA-certs &&\
    update-ca-trust &&\
    dnf update -y ca-certificates &&\
    dnf clean all &&\
    mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /build /data /pool /opt/cms &&\
    mkdir -p /hdfs /mnt/hadoop /hadoop /cms /etc/cvmfs/SITECONF /lfs_roots /storage &&\
    touch /etc/tnsnames.ora &&\
    /tmp/fix_ssh_config.sh /etc/ssh/ssh_config &&\
    rm -f /tmp/CERN.repo /tmp/RPM-GPG-KEY-kojiv2 /tmp/fix_ssh_config.sh &&\
    echo "Timestamp: @BUILD_DATE@"   > /image-build-info.txt &&\
    sed -i -e s'|^ *allow  *setuid.*|allow setuid = no|;s|^ *enable  *overlay.*|enable overlay = no|;s|^ *enable  *underlay.*|enable underlay = yes|' /etc/apptainer/apptainer.conf

LABEL build-date="@BUILD_DATE@"
