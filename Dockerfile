FROM python:3.8.2-alpine3.11
LABEL description="Gitlab Merge Requests exporter" \
  version="1.0" \
  maintainer="Laurent Dumont - ldumont@northernsysadmin.com"

COPY requirements.txt requirements.txt

RUN \
  pip3 install -r requirements.txt;

COPY gitlab-mr-exporter.py gitlab-mr-exporter.py

ENTRYPOINT ["python3", "gitlab-mr-exporter.py"]
