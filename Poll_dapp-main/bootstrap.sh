#!/bin/sh

add-apt-repository -y ppa:ethereum/ethereum
add-apt-repository -y ppa:ethereum/ethereum-dev
sudo apt-get update
sudo apt-get install -y build-essential solc ethereum nginx curl vim

wget https://deb.nodesource.com/setup_10.x
chmod +x setup_10.x
sudo -E ./setup_10.x
sudo apt-get install -y nodejs
npm install -g ganache-cli truffle

cd poll_dapp

sudo apt install pip3
pip3 install web3