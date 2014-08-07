FROM ubuntu

MAINTAINER  Patrick Gartung "gartung@fnal.gov"

RUN apt-get update -y && apt-get install -y \
	git rinse sudo tar build-essential npm && \
	ln -sf /usr/bin/nodejs /usr/local/bin/node && \
	apt-get install -y sphinx-common && \
	apt-get install -y libapache2-mod-wsgi python-pip &&\
	pip install virtualenv virtualenvwrapper python-hglib nose &&\
	apt-get install -y apache2-dev apache2 && \
	apt-get install -y libsqlite3-dev sqlite3 git mercurial llvm-3.3 libclang-3.3-dev clang-3.3 pkg-config &&\
	apt-get clean all &&\
	update-alternatives --install /usr/local/bin/llvm-config llvm-config /usr/bin/llvm-config-3.3 0

RUN git clone --recursive \
	https://github.com/gartung/dxr.git \
	/dxr && cd /dxr/trilite && make &&\ 
	cp -p libtrilite.so /usr/lib && \
	cp -p libtrilite.so /usr/lib64 && \
	/sbin/ldconfig && cd /dxr && ./peep.py install -r requirements.txt &&\
	make && python setup.py install && cd tests/test_basic && make

RUN mkdir -p /etc/apache2/sites-enabled

ADD dxr.conf /etc/apache2/sites-enabled/dxr.conf

RUN chmod 0644 /etc/apache2/sites-enabled/dxr.conf && a2enmod rewrite && a2enmod proxy && a2enmod wsgi && a2dissite 000-default 

EXPOSE 8000

EXPOSE 80

RUN mkdir -p /target

ADD dxr.sh /dxr.sh

CMD ["/dxr.sh"]
