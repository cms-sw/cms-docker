FROM cmssw/docker-lxr:v0

CMD /bin/rm -rf /lxr/glimpse_db
ADD custom.d/lxr.conf /lxr/lxr.conf
RUN addgroup --gid 500 lxr
RUN adduser  --uid 500 --gid 500 lxr
COPY scripts/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/bash"]
