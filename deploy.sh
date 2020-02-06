sudo yum install python3

sudo mkdir -p /var/www
sudo chmod 777 /var/www
cd /var/www
git clone git@github.com:thymiannne/deriberable-flask.git
cd /var/www/deriberable-flask

python3 -m venv ./venv
. ./venv/bin/activate

# pip install flask
sudo yum groupinstall "Development Tools"
# sudo yum install python-devel
sudo yum install python3-devel
# pip install uwsgi
pip install --upgrade pip
pip install -r requirements.txt

sudo yum install nginx
# When Amazon Linux 2 AMI
sudo amazon-linux-extras
sudo amazon-linux-extras info nginx1
sudo amazon-linux-extras install nginx1
sudo amazon-linux-extras

sudo cp ./default.conf /etc/nginx/conf.d/
echo "Commentout parts related to the server in nginx.conf"
sudo service nginx restart

screen
. ./venv/bin/activate
uwsgi --ini uwsgi.ini
