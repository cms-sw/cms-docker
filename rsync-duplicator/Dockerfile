FROM arkii/centos65

RUN yum update -y
RUN yum install -y rsync
RUN yum install -y openssh which

CMD rsync -av $SOURCE_USER@$SOURCE_SERVER:$SOURCE_DIR/ $DEST_DIR/
