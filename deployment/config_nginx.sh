sudo cp flask_app_nginx /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/flask_app_nginx /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo service nginx restart
sudo service nginx status
