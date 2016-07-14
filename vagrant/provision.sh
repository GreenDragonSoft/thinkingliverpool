#!/bin/sh -eux


update_apt() {
  apt-get update
}

install_postgresql() {
  apt-get install -y postgresql libpq-dev
}

install_system_dependencies() {
  apt-get install -y python3 python3-dev python-virtualenv libjpeg-dev libxml2-dev libxslt1-dev unzip nodejs-legacy npm
  gem install sass
}

run_as_vagrant() {
  su vagrant -c "$1"
}

setup_virtualenv() {
  run_as_vagrant "virtualenv -p $(which python3) ~/venv"
  run_as_vagrant "bash -c '. ~/venv/bin/activate && pip install -r ~/app/requirements.txt'"
}

create_postgresql_database_and_user() {
    # We make a user and a database both called vagrant, then the vagrant
    # username will automatically access that database.
    CREATE_USER="createuser --superuser vagrant"
    CREATE_DATABASE="createdb --owner vagrant vagrant"

    # Run as postgres user, it has permission to do this
    su -c "${CREATE_USER}" postgres || true
    su -c "${CREATE_DATABASE}" postgres || true
}

install_ngrok() {
  if [ ! -f "/usr/local/bin/ngrok" ] ; then
    cd /tmp/download
    wget -c https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
    unzip -o ngrok-stable-linux-amd64.zip
    mv ngrok /usr/local/bin/ngrok
    cd -
  fi
}


update_apt
install_postgresql
install_system_dependencies
setup_virtualenv
create_postgresql_database_and_user
install_ngrok
