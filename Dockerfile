FROM telminov/ubuntu-14.04-python-3.5

EXPOSE 8080-8081

# remove several traces of debian python
RUN apt-get purge -y python.*
RUN apt-get install -y python-dateutil

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
	&& ln -s easy_install-3.5 easy_install \
	&& ln -s idle3 idle \
	&& ln -s pydoc3 pydoc \
	&& ln -s python3 python \
	&& ln -s python-config3 python-config

# -----------------------------------------------

RUN mkdir /opt/attestation
COPY . /opt/attestation/
WORKDIR /opt/attestation/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN cp project/settings.sample.py project/settings.py
RUN python3 ./manage.py migrate
RUN python3 ./manage.py collectstatic --noinput

CMD python3 ./manage.py runserver

# -----------------------------------------------
