#!/bin/bash


#actualizar el sistema
apt update -y
apt upgrade -y


#instalar dependencias necesarias
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev pyinstaller -y

#instalar python
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz

#descomprimir
tar -xf Python-3.11.0.tgz
cd Python-3.11.0

#montamos la build
./configure --enable-optimizations

#le tiramos varios procesos para que tire mas rapido
make -j$(nproc)

#instalamos
make altinstall


#confirmamos instalacion
python3 --version

#montamos el python en la ruta del sistema
python3.11 -m pip install -U pip
echo '$alias pip3="python3.7 -m pip"' >> ~/.bashrc

#instalar biblios

pip install -r requirements.txt
pip install --upgrade pip
