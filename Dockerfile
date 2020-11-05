FROM python:3.8-alpine

RUN apk add tor

ADD torrc /etc/tor/torrc
RUN mkdir /etc/torrc.d

ADD main.py main.py
ADD lookup /usr/local/bin/lookup

RUN echo "python3 main.py" >> run.sh
RUN echo "chmod 600 -R /var/lib/tor" >> run.sh
RUN echo "chmod 644 -R /etc/torrc.d" >> run.sh
RUN echo "/usr/bin/tor" >> run.sh

RUN chmod +x run.sh /usr/local/bin/lookup
RUN chown root:root -R /etc/tor* /var/lib/tor

ENTRYPOINT ["/bin/sh", "run.sh"]
