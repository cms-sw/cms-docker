from cmssw/slc6-vanilla

RUN yum install -y git HEP_OSlibs_SL6
RUN yum install -y e2fsprogs
RUN useradd dqmgui && install -o dqmgui -d /data

USER dqmgui
WORKDIR /data
RUN git clone https://github.com/dmwm/deployment.git cfg

RUN cfg/Deploy -R cmsweb@HG1302b -r comp=comp.pre.rovere -t 7.4.5 -s "prep sw post" /data dqmgui@7.4.5/bare

