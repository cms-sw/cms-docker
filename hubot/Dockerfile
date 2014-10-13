FROM dockerfile/nodejs

ENV HUBOT_XMPP_HOST some-meaningless-default
ENV HUBOT_XMPP_PORT some-meaningless-default
ENV HUBOT_GITHUB_REPO some-meaningless-default
ENV HUBOT_NAME some-meaningless-default

RUN npm install -g hubot coffee-script underscore
RUN apt-get update -y
RUN apt-get install -y redis-server git libicu-dev
ADD hubot-scripts.json /root/$HUBOT_NAME/hubot-script.json
ADD hubot-conf /etc/sysconfig/hubot
RUN cd /root && hubot --create $HUBOT_NAME
ADD hubot-package.json /root/$HUBOT_NAME/package.json
RUN cd /root/$HUBOT_NAME && npm install

CMD service redis-server start ; cd /root/$HUBOT_NAME && . /etc/sysconfig/hubot && bin/hubot -a xmpp -n $HUBOT_NAME
