FROM cmssw/mesos-base

ENV PATH=/cms-marathon:/bin:/usr/bin
RUN yum install -y python-argparse PyYAML vim
ADD motd /etc/motd
#RUN ln -sf /cms-marathon/deploy /usr/bin/deploy
