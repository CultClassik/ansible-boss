FROM pypy:3.6-slim-stretch

LABEL "maintainer"="Chris Diehl <cultclassik@gmail.com>"

ENV SSH_USER="ansible"
ENV SSH_HOST="naster.diehlabs.lan"

USER root

RUN \
  #echo 'deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main' >> /etc/apt/sources.list &&\
  #apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 &&\
  #apt update &&\
  #apt install ansible -y
  apt-get update && \
  apt-get install -y software-properties-common && \
  apt-add-repository ppa:ansible/ansible && \
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 &&\
  apt-get update && \
  apt-get install -y --force-yes ansible

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# The private key shoudl be mounted which will be used to connect to systems using Ansible
VOLUME /key.rsa

# The path to the Ansible source
VOLUME /ansible

WORKDIR /ansible

EXPOSE 8000

CMD ["gunicorn", "app:api", "--name", "ansible", "--bind", "0.0.0.0:8000"]