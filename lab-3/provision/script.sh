#!/bin/bash

apt-get update
apt-get install -y git htop nginx

sed -i 's|/var/www/html|/vagrant/html|' /etc/nginx/sites-available/default

systemctl restart nginx