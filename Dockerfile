from python:alpine

RUN pip install requests
COPY src/ /opt/resource/python
ENV PYTHONPATH=${PYTHONPATH}:/opt/resource/python
# TODO: run the testz

COPY cmd/check /opt/resource/check
RUN chmod +x /opt/resource/check
