#!/usr/bin/env bash
# setting up web servers for web_static deployment.

# Check if Nginx is installed
if ! dpkg -l | grep -q "nginx"; then
    sudo apt-get -y update
    sudo apt-get -y upgrade
    sudo apt-get -y install nginx
fi

# Create necessary directory structure
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create test HTML file
echo "Hello, Web Static" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Set up symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership recursively to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Add a location block to Nginx configuration
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Start or restart the Nginx service
sudo service nginx restart
