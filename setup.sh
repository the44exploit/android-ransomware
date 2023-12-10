#!/bin/bash

sudo apt update
sudo apt upgrade -y

sudo apt install default-jre -y
sudo apt install default-jdk -y

sudo apt install python3 python3-pip -y
pip3 install Pillow
sudo apt install wget -y

wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
wget -O apktool.jar https://github.com/iBotPeaches/Apktool/releases/download/v2.9.1/apktool_2.9.1.jar

sudo mv apktool.jar apktool /usr/local/bin
chmod +x /usr/local/bin/apktool /usr/local/bin/apktool.jar
