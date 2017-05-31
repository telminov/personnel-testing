FROM telminov/ubuntu-14.04-python-3.5

RUN apt-get update && \
    apt-get install -y \
                    vim \
                    git \
                    supervisor

RUN /var/log/personnel_testing/

RUN mkdir /opt/personnel-testing
COPY . /opt/personnel-testing/
WORKDIR /opt/personnel-testing/

RUN pip3 install -r requirements.txt
RUN cp project/settings.sample.py project/settings.py

COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisor/prod.conf /etc/supervisor/conf.d/personnel-testing.conf

EXPOSE 80

VOLUME /data/
VOLUME /conf/
VOLUME /static/

CMD test "$(ls /conf/settings.py)" || cp project/settings.py /conf/settings.py; \
    rm project/settings.py; ln -s /conf/settings.py project/settings.py; \
    rm -rf static; ln -s /static static; \
    python3 ./manage.py migrate; \
    python3 ./manage.py collectstatic --noinput; \
    /usr/bin/supervisord


