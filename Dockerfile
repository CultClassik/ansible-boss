FROM pypy:3-stretch

LABEL "maintainer"="Chris Diehl <cultclassik@gmail.com>"

ENV SSH_USER="ansible"
ENV SSH_HOST="naster.diehlabs.lan"
ENV GIT_URL="https://cultclassik@dev.azure.com/cultclassik/Diehlabs/_git/ansible-boss"
ENV GIT_DIR="/ansible"
ENV ANSIBLE_CMD="ansible-playbook /ansible/main.yml --private-key /key.rsa"
ENV ANSIBLE_HOST_KEY_CHECKING=False
ENV ANSIBLE_VERSION="2.4.6"

USER root

RUN \
  echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" >> /etc/apt/sources.list &&\
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 &&\
  apt update &&\
  apt install ansible=${ANSIBLE_VERSION} -y

ADD app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt &&\
    mkdir /ansible

# The private key should be mounted which will be used to connect to systems using Ansible
VOLUME /key.rsa

EXPOSE 8000

CMD ["gunicorn", "app:api", "--name", "ansible", "--bind", "0.0.0.0:8000"]