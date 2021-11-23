#!/bin/bash

if [ ! -x /var/lib/docker ]; then
  echo "installing docker..."
  sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo apt-key fingerprint 0EBFCD88
  sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
  sudo apt-get update
  sudo apt-cache policy docker-ce
  sudo apt-get install -y docker-ce docker-compose
  sudo groupadd docker
  sudo usermod -aG docker $USER
  sudo systemctl enable docker
  echo "docker installed successfully!"
fi
echo "setting up environment..."
sysctl -w vm.max_map_count=262144
mkdir -p ./data01 ./data02 ./data03
chmod g+rwx ./data*
chgrp 0 ./data*
echo "running docker containers..."
docker-compose up -d
echo "all done! please wait a few minutes, and then access Findexer on port 2021."
