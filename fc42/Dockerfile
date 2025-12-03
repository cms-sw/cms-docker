FROM docker.io/fedorariscv/base:42
LABEL maintainer="CMS Build"
LABEL name="CMS Worker Node on FC - Runtime"

#Break package installation in multiple steps to avoid the following error due to large layers
# io: read/write on closed pipe 
RUN dnf install -y \
      bash tcsh tar glibc glibc-devel libgcc libxcrypt openssl-libs libcom_err krb5-libs ncurses-libs \
      libX11 readline tcl tk mesa-libGLU libglvnd-glx libglvnd-opengl libXext libXft libXpm libaio libnsl sssd-client &&\
    dnf clean all
RUN dnf install -y \
      rpm-build nspr rsync wget openssl-devel ncurses-devel \
      libX11-devel readline-devel tcl-devel tk-devel mesa-libGLU-devel libXext-devel libXft-devel \
      libXpm-devel libtool libdrm &&\
    dnf clean all
RUN dnf install -y \
      gcc-c++ libXmu krb5-devel coreutils-single libcom_err-devel python3-cryptography jq \
      man-db time bc strace xauth vim cmake python3 which procps-ng \
      krb5-workstation environment-modules xdg-utils tmux &&\
    dnf clean all
RUN dnf install -y \
      voms-clients-cpp python3-requests python3-psutil python3-pip \
      gfal2-util-scripts gfal2-all python3-gfal2-util xrootd-client openldap-compat myproxy texinfo \
      perl perl-libs &&\
    dnf clean all
RUN dnf install -y \
      git nss java-21-openjdk-devel squid apptainer \
      libgfortran openssl gcc-gfortran elfutils-libelf-devel gettext-devel libatomic &&\
    dnf clean all
RUN echo fc42 > /etc/cmsos &&\
    mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /build /data /pool /opt/cms /etc/ssh &&\
    mkdir -p /hdfs /mnt/hadoop /hadoop /cms /etc/cvmfs/SITECONF /lfs_roots /storage /scratch &&\
    touch /etc/tnsnames.ora &&\
    sed -i -e s'|^ *allow  *setuid.*|allow setuid = no|;s|^ *enable  *overlay.*|enable overlay = no|;s|^ *enable  *underlay.*|enable underlay = yes|' /etc/apptainer/apptainer.conf

ADD share/fix_ssh_config.sh     /root/fix_ssh_config.sh
RUN chmod +x /root/fix_ssh_config.sh &&\
    /root/fix_ssh_config.sh /etc/ssh/ssh_config
