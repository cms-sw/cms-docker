FROM centos:centos6

RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
ENV GOPATH /usr/local/go
RUN yum update -y && yum install -y golang git

ENV REPO mesosphere

RUN go get github.com/miekg/dns
RUN go get github.com/$REPO/mesos-dns
RUN cd $GOPATH/src/github.com/$REPO/mesos-dns && go build -o mesos-dns
ADD create-mesos-dns-config.py /

CMD python /create-mesos-dns-config.py && /usr/local/go/bin/mesos-dns ${VERBOSE+-v} -config /config.json
