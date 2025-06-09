FROM @BASE_IMAGE_NAME@
LABEL maintainer="CMS Build"
LABEL name="CMS Worker Node on EL - Buildtime dependencies"

# Dependency on libXmu might be cleaned up in the future
# Extra packages comparing with el8: krb5-devel libcom_err-devel (coreutils-single in el8 config file)
RUN dnf install --disablerepo=epel -y rpm-build git nspr nss rsync wget openssl openssl-devel ncurses-devel \
	libX11-devel readline-devel tcl-devel tk-devel mesa-libGLU-devel libXext-devel libXft-devel \
	libXpm-devel java-21-openjdk-devel libtool libdrm \
 	gcc-c++ libXmu krb5-devel coreutils-single libcom_err-devel \
  python3-cryptography jq && dnf clean all

# Please add user packages in the RUN command below
RUN dnf install --disablerepo=epel -y man-db time bc nano strace xauth vim cmake \
	krb5-workstation environment-modules xdg-utils squid tmux emacs lua &&\
    dnf install -y screen &&\
    arch=$(uname -m) &&\
    wget https://kojihub.stream.centos.org/kojifiles/vol/koji02/packages/lua-posix/36.2.1/8.el10/${arch}/lua-posix-36.2.1-8.el10.${arch}.rpm &&\
    wget https://kojihub.stream.centos.org/kojifiles/vol/koji02/packages/copy-jdk-configs/4.1/7.el10/noarch/copy-jdk-configs-4.1-7.el10.noarch.rpm &&\
    wget https://kojihub.stream.centos.org/kojifiles/vol/koji02/packages/java-17-openjdk/17.0.11.0.9/2.el10/${arch}/java-17-openjdk-devel-17.0.11.0.9-2.el10.${arch}.rpm &&\
    wget https://kojihub.stream.centos.org/kojifiles/vol/koji02/packages/java-17-openjdk/17.0.11.0.9/2.el10/${arch}/java-17-openjdk-17.0.11.0.9-2.el10.${arch}.rpm &&\
    wget https://kojihub.stream.centos.org/kojifiles/vol/koji02/packages/java-17-openjdk/17.0.11.0.9/2.el10/${arch}/java-17-openjdk-headless-17.0.11.0.9-2.el10.${arch}.rpm &&\
    rpm -Uvh lua-posix*.rpm copy-jdk-configs*.rpm java-17-openjdk*.rpm &&\
    rm -f lua-posix*.rpm copy-jdk-configs*.rpm java-17-openjdk*.rpm &&\
    dnf clean all

RUN dnf --enablerepo=crb install -y texinfo libstdc++-static &&\
	epel_pkgs="@EPEL_PACKAGES@" &&\
	if [ -n "$epel_pkgs" ] ; then dnf install -y $epel_pkgs; fi &&\
	xcmd="@EXTRA_COMMAND@" &&\
	if [ "$xcmd" = "" ] ; then xcmd=true; fi &&\
	eval $xcmd &&\
	dnf update -y ca-certificates &&\
	dnf clean all &&\
        /root/fix_ssh_config.sh /etc/ssh/ssh_config &&\
	echo "Timestamp: @BUILD_DATE@" > /image-build-info.txt

LABEL build-date="@BUILD_DATE@"
