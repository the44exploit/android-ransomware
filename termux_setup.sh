#!/bin/bash

pkg update -y
pkg upgrade -y

pkg install -y python
pkg install -y openjdk-17


echo "Setup complete!"

