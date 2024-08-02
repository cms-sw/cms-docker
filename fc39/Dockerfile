FROM docker.io/fedorariscv/base:39
LABEL maintainer="CMS Build"
LABEL name="CMS Worker Node on FC - Runtime"

RUN rm -f /tmp/pkgs.txt &&\
    for pkg in bash tcsh tar glibc glibc-devel libgcc libxcrypt openssl-libs libcom_err krb5-libs ncurses-libs \
      libX11 readline tcl tk mesa-libGLU libglvnd-glx libglvnd-opengl libXext libXft libXpm libaio libnsl sssd-client \
      rpm-build nspr rsync wget openssl-devel ncurses-devel \
      libX11-devel readline-devel tcl-devel tk-devel mesa-libGLU-devel libXext-devel libXft-devel \
      libXpm-devel libtool libdrm \
      gcc-c++ libXmu krb5-devel coreutils libcom_err-devel python3-cryptography jq \
      man-db time bc strace xauth vim cmake python3 which procps-ng \
      krb5-workstation environment-modules xdg-utils tmux \
      voms-clients-cpp python3-requests python3-psutil python3-pip \
      gfal2-util-scripts gfal2-all python3-gfal2-util xrootd-client openldap-compat myproxy texinfo \
      perl perl-libs \
      git nss java-17-openjdk-devel squid apptainer ; do \
        dnf5 install -y $pkg || echo " $pkg " >> /tmp/pkgs.txt ;\
    done ;\
    [ -s /tmp/pkgs.txt ] && dnf5 install -y $(cat /tmp/pkgs.txt) &&\
    rm -f /tmp/pkgs.txt &&\
    echo fc39 > /etc/cmsos &&\
    dnf5 clean all &&\
    mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /build /data /pool /opt/cms /etc/ssh &&\
    mkdir -p /hdfs /mnt/hadoop /hadoop /cms /etc/cvmfs/SITECONF /lfs_roots /storage /scratch &&\
    touch /etc/tnsnames.ora &&\
    sed -i -e s'|^ *allow  *setuid.*|allow setuid = no|;s|^ *enable  *overlay.*|enable overlay = no|;s|^ *enable  *underlay.*|enable underlay = yes|' /etc/apptainer/apptainer.conf

ADD share/fix_ssh_config.sh     /root/fix_ssh_config.sh
RUN dnf5 install -y libgfortran openssl gcc-gfortran elfutils-libelf-devel gettext-devel libatomic && dnf5 clean all &&\
    chmod +x /root/fix_ssh_config.sh &&\
    /root/fix_ssh_config.sh /etc/ssh/ssh_config
