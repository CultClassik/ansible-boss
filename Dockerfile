FROM pypy:3-stretch

LABEL "maintainer"="Chris Diehl <cultclassik@gmail.com>"

ENV SSH_USER="ansible"
ENV SSH_HOST="naster.diehlabs.lan"
ENV GIT_URL="https://github.com/CultClassik/ansible-control.git"
ENV GIT_DIR="/ansible"
ENV ANSIBLE_CMD="ansible-playbook /ansible/main.yml --private-key /key.rsa"
ENV ANSIBLE_HOST_KEY_CHECKING=False
ENV ANSIBLE_VERSION="2.9.3-1ppa~trusty"

USER root

RUN \
  echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" >> /etc/apt/sources.list &&\
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 &&\
  apt update &&\
  # output available ansible versions for troubleshooting cicd builds
  apt-cache madison ansible &&\
  apt install ansible=${ANSIBLE_VERSION} -y &&\
  apt-get remove -y \
  bzr mercurial openssh-client subversion procps \
  autoconf automake bzip2 dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev libevent-dev libffi-dev libgdbm-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev libmagickcore-dev libmagickwand-dev libmaxminddb-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev &&\
  rm -rf /var/lib/apt/lists/*

ADD app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt &&\
    mkdir /ansible

# The private key should be mounted which will be used to connect to systems using Ansible
VOLUME /key.rsa

EXPOSE 8000

CMD ["gunicorn", "app:api", "--name", "ansible", "--bind", "0.0.0.0:8000"]