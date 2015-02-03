FROM centos:centos6

RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
ENV GOPATH /usr/local/go
RUN yum update -y && yum install -y golang git

RUN go get github.com/miekg/dns
RUN go get github.com/mesosphere/mesos-dns
RUN cd $GOPATH/src/github.com/mesosphere/mesos-dns && go build -o mesos-dns main.go
ADD create-mesos-dns-config.py /
RUN python /create-mesos-dns-config.py

CMD /usr/local/go/bin/mesos-dns -config /config.json
