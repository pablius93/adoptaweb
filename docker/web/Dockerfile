FROM python:3.6-onbuild
ENV PYTHONUNBUFFERED 1
RUN mkdir /web
WORKDIR /web
ADD . /web/
RUN pip install -r requirements/development.txt
RUN sh /web/scripts/install_system_requirements.sh
