#!/bin/bash

# Update package list and install required packages
sudo apt-get -y update
sudo apt-get -y install python3 python3-venv python3-dev nginx git supervisor

# Set MySQL root password and preconfigure the MySQL APT configuration for unattended installation
echo "mysql-apt-config mysql-apt-config/select-server select mysql-8.0" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password password FlaskPassword1" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password FlaskPassword1" | sudo debconf-set-selections

# Download and install MySQL APT configuration package
wget https://dev.mysql.com/get/mysql-apt-config_0.8.32-1_all.deb
sudo DEBIAN_FRONTEND=noninteractive dpkg -i mysql-apt-config_0.8.32-1_all.deb

# Update package list and install MySQL server
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server

# Enable and start MySQL service
sudo systemctl enable mysql
sudo systemctl start mysql

# MySQL database setup with new password for the fitnesstracker user
sudo mysql -u root -prootpassword <<MYSQL_SCRIPT
CREATE DATABASE fitnesstracker;
CREATE USER 'fitnesstracker'@'localhost' IDENTIFIED BY 'FlaskPassword1';
GRANT ALL PRIVILEGES ON fitnesstracker.* TO 'fitnesstracker'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

# Clone the fitnesstracker repository from the master branch
cd /root
git clone --branch main https://github.com/M143-5is16lyhuber/fitnesstracker.git

# Install dependencies using the existing virtual environment
/root/fitnesstracker/venv/bin/pip install -r /root/fitnesstracker/requirements.txt

# Set environment variables for Flask
export FLASK_APP=/root/fitnesstracker/app.py
export FLASK_ENV=production

# Run Flask database migrations
/root/fitnesstracker/venv/bin/python3.11 -m flask db init
/root/fitnesstracker/venv/bin/python3.11 -m flask db migrate -m "initial fitnesstracker DB"
/root/fitnesstracker/venv/bin/python3.11 -m flask db upgrade

# Configure firewall
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow 443/tcp
sudo ufw --force enable
sudo ufw status


# Configure Nginx for the fitness tracker app
sudo tee /etc/nginx/sites-available/fitnesstracker > /dev/null <<EOF
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
EOF

# Enable the fitness tracker Nginx configuration and remove the default Nginx configuration (to remove the default page)
sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-available/default
sudo ln -s /etc/nginx/sites-available/fitnesstracker /etc/nginx/sites-enabled/fitnesstracker
sudo systemctl restart nginx

# Supervisor configuration for fitness tracker app
sudo tee /etc/supervisor/conf.d/fitnesstracker.conf > /dev/null <<EOF
[program:fitnesstracker]
command=/root/fitnesstracker/venv/bin/gunicorn -b localhost:8000 -w 4 fitnesstracker:app
directory=/root/fitnesstracker
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
EOF

# Reload Supervisor to apply the new configuration
sudo supervisorctl reload
