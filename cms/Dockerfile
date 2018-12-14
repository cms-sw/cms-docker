#Imported from https://hub.docker.com/r/bbockelm/cms/dockerfile

ARG OSG_WN_TAG=3.4-el7
ARG BUILD_DATE=20181214-0000
ARG EXTRA_PACKAGES=

FROM opensciencegrid/osg-wn:${OSG_WN_TAG}

LABEL name="CMS Worker Node on EL"
LABEL build-date="${BUILD_DATE}"
LABEL maintainer="CMS Build"

# Required
# --------
# - cmsRun fails without stdint.h (from glibc-headers)
#   Tested CMSSW_7_4_5_patch1
#
# Other
# -----
# - ETF calls /usr/bin/lsb_release (from redhat-lsb-core)
# - sssd-client for LDAP lookups through the host
# - SAM tests expect cvmfs utilities
# - gcc is required by GLOW jobs (builds matplotlib)
#
# CMSSW dependencies
# ------------------
# Required software is listed under slc7_amd64_platformSeeds at
# http://cmsrep.cern.ch/cgi-bin/cmspkg/driver/cms/slc7_amd64_gcc820
#
# - 7 Feb 2018: libaio was added to enable the Oracle client, needed for T0 jobs.
# - 14 Dec 2018: Rsync added, needed by cms bootstrap.sh

RUN yum -y install cvmfs \
                   gcc \
                   glibc-headers \
                   openssh-clients \
                   redhat-lsb-core \
                   sssd-client && \
    yum -y install glibc coreutils bash tcsh zsh perl tcl tk readline openssl ncurses e2fsprogs krb5-libs freetype ncurses-libs perl-libs perl-ExtUtils-Embed \
                   fontconfig compat-libstdc++-33 libidn libX11 libXmu libSM libICE libXcursor \
                   libXext libXrandr libXft mesa-libGLU mesa-libGL e2fsprogs-libs libXi libXinerama libXft-devel \
                   libXrender libXpm libcom_err perl-Test-Harness perl-Carp perl-constant perl-PathTools \
                   perl-Data-Dumper perl-Digest-MD5 perl-Exporter perl-File-Path perl-File-Temp perl-Getopt-Long \
                   perl-Socket perl-Text-ParseWords perl-Time-Local libX11-devel libXpm-devel libXext-devel mesa-libGLU-devel \
                   perl-Switch perl-Storable perl-Env perl-Thread-Queue libaio rsync ${EXTRA_PACKAGES} && \
    yum clean all

# Various directories needed for bind mounts (as overlayfs is not available on RHEL6)

RUN mkdir -p /hdfs \
             /mnt/hadoop \
             /hadoop \
             /cms \
             /etc/cvmfs/SITECONF \
             /lfs_roots \
             /storage

