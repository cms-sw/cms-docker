# A generic ssh server.
#
# Notice you'll need to pass the keyfiles via:
# 
# docker -v <private-key-on-host>:/etc/ssh/ssh_host_dsa_key \
#        -v <private-authorized-keys-on-host>:/home/cmsbuild/authorized_keys
#
# do not commit keyfiles in this repository!
#
FROM arkii/centos65

RUN yum update -y
RUN yum install -y rsync
RUN yum install -y openssh-server which
RUN adduser cmsbuild

# Only use dsa key.
CMD /usr/bin/sshd -D -d -h /etc/ssh/ssh_host_dsa_key
