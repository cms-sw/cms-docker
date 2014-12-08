FROM centos:centos6


RUN rpm -Uvh http://repos.mesosphere.io/el/6/noarch/RPMS/mesosphere-el-repo-6-2.noarch.rpm
RUN yum update -y && yum install -y rsync \
                                    openssh-clients \
                                    which \
                                    mesos \
                                    git \
                                    java-1.7.0-openjdk-devel \
                                    tar \
                                    wget

RUN rpm -Uvh ftp://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/Application:/Geo/CentOS_6/noarch/maven-3.0.4-2.2.noarch.rpm

ENV COMMIT b83c01b
ENV BRANCH add-attributes-selection

RUN git clone -b $BRANCH https://github.com/ktf/elasticsearch-mesos
RUN cd elasticsearch-mesos && git reset --hard $COMMIT ; bin/build || bin/build

ADD run.sh /run.sh
CMD sh -ex /run.sh
