FROM @BASE_IMAGE_NAME@
LABEL maintainer="CMS Build"
LABEL name="CMS Worker Node on EL"

ADD extra          /tmp/extra

RUN sed -i -e 's|^mirrorlist=|#mirrorlist=|;s|#baseurl=|baseurl=|;s|mirror.centos.org|vault.centos.org|' /etc/yum.repos.d/CentOS-Base.repo &&\
    yum install -y \
        java-1.8.0-openjdk python-devel java-1.8.0-openjdk-devel java-11-openjdk-devel ntp \
        git subversion bc finger zip unzip which bzip2 \
        zlib nss nspr popt nss-util sssd-client \
        openssl openssl-devel openssl-libs \
        glibc coreutils bash tcsh zsh perl tcl tk readline readline-devel ncurses e2fsprogs krb5-libs freetype fontconfig \
        libstdc++ libidn libX11 libXmu libSM libICE libXcursor libXext libXrandr libXft mesa-libGLU mesa-libGL \
        e2fsprogs-libs libXi libXinerama libXrender libXpm gcc-c++ libcom_err libXpm-devel libXft-devel libX11-devel \
        libXext-devel mesa-libGLU mesa-libGLU-devel libGLEW glew perl-Digest-MD5 perl-ExtUtils-MakeMaker patch \
        perl-libwww-perl krb5-libs krb5-devel perl-Data-Dumper perl-WWW-Curl texinfo hostname time perl-Carp \
        perl-Text-ParseWords perl-PathTools perl-ExtUtils-MakeMaker perl-Exporter perl-File-Path perl-Getopt-Long \
        perl-constant perl-File-Temp perl-Socket perl-Time-Local perl-Storable glibc-headers perl-threads \
        perl-Thread-Queue perl-Module-ScanDeps perl-Test-Harness perl-Env perl-Switch perl-ExtUtils-Embed \
        ncurses-libs perl-libs file wget perl-LWP-Protocol-https python-setuptools \
        libaio tcl-devel tk-devel man-db vim perl-Time-Piece \
        setroubleshoot-server autofs gdb attr python-requests-kerberos libgfortran time python3 strace &&\
    mv /tmp/extra/krb5.conf /etc/krb5.conf &&\
    mv /tmp/extra/epel.repo /etc/yum.repos.d/ &&\
    mv /tmp/extra/epel-testing.repo /etc/yum.repos.d/ &&\
    rpm --import /tmp/extra/RPM-GPG-KEY-EPEL-7 &&\
    yum install -y voms-clients-cpp krb5-workstation myproxy fetch-crl python2-psutil libstdc++-static jq &&\
    ([ "@EXTRA_PACKAGES@" != "" ] && yum install -y @EXTRA_PACKAGES@ || true) &&\
    yum install -y xrootd-client &&\
    mv /tmp/extra/cern.repo /etc/yum.repos.d/cern.repo &&\
    rpm --import /tmp/extra/RPM-GPG-KEY-cern &&\
    yum install -y CERN-CA-certs &&\
    update-ca-trust &&\
    yum update -y ca-certificates &&\
    yum clean all &&\
    mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /data /pool /build &&\
    mkdir -p /hdfs /mnt/hadoop /hadoop /cms /etc/cvmfs/SITECONF /lfs_roots /storage &&\
    touch /etc/tnsnames.ora &&\
    rm -rf /tmp/extra &&\
    conf=/etc/singularity/singularity.conf &&\
    [ ! -f /etc/apptainer/apptainer.conf ] || conf=/etc/apptainer/apptainer.conf &&\
    echo "Timestamp: @BUILD_DATE@"   > /image-build-info.txt &&\
    sed -i -e s'|^ *allow  *setuid.*|allow setuid = no|;s|^ *enable  *overlay.*|enable overlay = no|;s|^ *enable  *underlay.*|enable underlay = yes|' $conf

# Python pip needed to install rucio client
# Gfal packages needed for CRAB
RUN yum install -y python3-pip python2-pip gfal2-util-scripts gfal2-all python3-gfal2-util python2-gfal2-util && yum clean all

#User packages
RUN yum install -y emacs screen && yum clean all

LABEL build-date="@BUILD_DATE@"
