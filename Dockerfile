FROM telminov/ubuntu-14.04-python-3.5

EXPOSE 8080

VOLUME /data/
VOLUME /conf/

RUN mkdir /opt/personnel-testing
COPY . /opt/personnel-testing/
WORKDIR /opt/personnel-testing/

RUN pip3 install -r requirements.txt
RUN cp project/settings.sample.py project/settings.py

COPY supervisor/prod.conf /etc/supervisor/conf.d/personnel-testing.conf

CMD test "$(ls /conf/settings.py)" || cp project/settings.py /conf/settings.py; \
    rm project/settings.py; \
    ln -s /conf/settings.py project/settings.py; \
    python3 ./manage.py migrate; \
    /usr/bin/supervisord

# TODO кнопка ответить блочить

