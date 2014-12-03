FROM centos:centos6

ENV MESOS_PLUGIN_VERSION master

RUN rpm -Uvh http://repos.mesosphere.io/el/6/noarch/RPMS/mesosphere-el-repo-6-2.noarch.rpm
RUN yum update -y && yum install -y rsync \
                                    openssh-clients \
                                    which \
                                    mesos \
                                    git \
                                    java-1.7.0-openjdk-devel
RUN rpm -Uvh ftp://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/Application:/Geo/CentOS_6/noarch/maven-3.0.4-2.2.noarch.rpm
RUN yum install -y tar wget

RUN git clone -b $MESOS_PLUGIN_VERSION https://github.com/ktf/elasticsearch-mesos
RUN cd elasticsearch-mesos ; bin/build

CMD cd /elasticsearch-mesos/elasticsearch-mesos-* && bin/elasticsearch-mesos
