FROM python:3.7.2-alpine3.8

WORKDIR /opt/app

ENV FLASK_APP="junos-route-stat-exporter.py"

COPY requirements.txt ./
RUN apk add build-base libffi-dev openssl-dev libxml2-dev libxslt-dev \
     && pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY junos-route-stat-exporter.py .
 
CMD [ "/usr/bin/env", "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080" ]