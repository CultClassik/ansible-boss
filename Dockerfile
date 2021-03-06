FROM pypy:3-stretch

LABEL "maintainer"="Chris Diehl <cultclassik@gmail.com>"

ENV GIT_DIR="/ansible"
ENV ANSIBLE_HOST_KEY_CHECKING=False
ENV WINRM_CERT_VALIDATE="ignore"
ENV ASNIBLE_LOG_PATH="/tmp/ansible_run.log"

ENV WINRM_USER="vagrant"
ENV WINRM_PASS="password"
ENV SSH_USER="ansible"
ENV SSH_PASS="We prefer keys"
ENV GIT_URL="https://github.com/CultClassik/ansible-control.git"
#ENV ANSIBLE_CMD="ansible-playbook /ansible/main.yml --key-file /key.rsa -i /ansible/inventory.yml --check"
ENV ANSIBLE_CMD="ansible-playbook /ansible/main.yml -i /ansible/inventory.yml"


USER root

ADD app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt &&\
  apt-get update && \
  apt-get install python3-apt -y && \
  apt-get remove -y \
  bzr mercurial subversion procps \
  autoconf automake bzip2 dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev libevent-dev libffi-dev libgdbm-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev libmagickcore-dev libmagickwand-dev libmaxminddb-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev &&\
  apt-get autoremove -y &&\
  rm -rf /var/lib/apt/lists/*

# The private key should be mounted which will be used to connect to systems using Ansible
VOLUME /key.rsa

EXPOSE 8000

CMD ["gunicorn", "app:api", "--name", "ansible", "--bind", "0.0.0.0:8000"]