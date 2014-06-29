FROM dockerfile/nodejs

RUN npm install -g hubot coffee-script underscore
RUN apt-get install -y redis-server git libicu-dev
ADD hubot-scripts.json /root/cmsbot/hubot-script.json
ADD hubot-conf /etc/sysconfig/hubot
RUN cd /root && hubot --create cmsbot
ADD hubot-package.json /root/cmsbot/package.json
RUN cd /root/cmsbot && npm install
ENV HUBOT_XMPP_HOST jabber.cern.ch
ENV HUBOT_XMPP_PORT 5222
ENV HUBOT_GITHUB_REPO cms-sw/cmssw

CMD cd /root/cmsbot && . /etc/sysconfig/hubot && bin/hubot -a xmpp -n cmsbot
