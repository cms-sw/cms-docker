FROM cmssw/mesos-base

RUN yum install -y iptables ca-certificates lxc e2fsprogs

EXPOSE 5051

ADD run.sh /run.sh

CMD /bin/sh -e -x /run.sh
