from cmssw/slc6-vanilla

RUN yum install -y git \
 HEP_OSlibs_SL6 \
 e2fsprogs

RUN useradd dqmgui && install -o dqmgui -d /data

USER dqmgui
WORKDIR /data
EXPOSE 8080
EXPOSE 8060
RUN git clone https://github.com/dmwm/deployment.git cfg && cd cfg && git reset --hard HG1408a && cd ..

RUN cfg/Deploy -R comp@HG1408a -r comp=comp.pre.rovere -t 7.4.5 -s 'prep sw post' /data dqmgui@7.4.5/bare

CMD source /data/current/sw.pre.rovere/slc6_amd64_gcc481/cms/dqmgui/7.4.5/128/etc/profile.d/init.sh && /data/current/config/dqmgui/manage restart "I did read documentation" && while true; do sleep 100; done
