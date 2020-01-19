# py-ansible-control
[![Build Status](https://dev.azure.com/cultclassik/Diehlabs/_apis/build/status/ansible-boss?branchName=master)](https://dev.azure.com/cultclassik/Diehlabs/_build/latest?definitionId=3&branchName=master)
[Image on Docker Hub](https://hub.docker.com/r/cultclassik/ansible-control/)

Python source to build cultclassik/ansible-control container.

This container will listen for an HTTP POST on the root URL.  Once it receives that request it will clone the repo at GIT_URL into the GIT_DIR,
then it will execute ANSIBLE_CMD as the SSH_USER with the provided SSH key.

## Pre-requisites

Requires a working installation of Docker CE or EE.

A repository containing your Ansible code.

Target systems must have the SSH_USER created and have the public key that corresponds to the mapped private key file.  This user probably needs sudo rights.

## Installation

docker build -t cultclassik/ansible-control .

## Usage

### Environment variables

* SSH_USER: User name of the user that will be used to execute Ansible run
* GIT_URL: Full URL of the Ansible repo that should be cloned and run
* GIT_DIR: Directory name to clone the repo in to
* ANSIBLE_CMD: The command to run to execute Ansible, i.e. "ansible-playbook /ansible/main.yml"

### Docker run

`docker run -name ansible-control \
  -e SSH_USER=myuser \
  -e GIT_URL=https://www.github.com/myurl \
  -e ANSIBLE_CMD=ansible-playbook /ansible/main.yml \
  -l traefik.enable=true \
  -l traefik.frontend.rule=Host:home.diehlabs.com;PathPrefixStrip:/ansible \
  -l traefik.port=8000 \
  -v /data/mysshkey.rsa:/key.rsa \
  cultclassik/ansible-control`

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

18.01.2020: Initial version created

## Credits

Chris Diehl wrote this.  Based on another project I created to initiate r10k deployments for Puppet Open Source Server from Github webhooks.

## License

Use it, improve it.