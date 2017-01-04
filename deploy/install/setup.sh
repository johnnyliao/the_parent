
datebase_root_password="liao12345"
datebase_name="the_parent"

if [ "$datebase_root_password" = "" ]; then
    echo "please set up the datebase_root_password"
    exit
fi

cd ~

# DNS settings
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
echo "nameserver 8.8.4.4" >> /etc/resolv.conf

apt-get -y update
apt-get -y upgrade

apt-get -y install python-pip
apt-get -y install git-core
apt-get -y install python-dev
apt-get -y install build-essential
apt-get -y install libxml2-dev
apt-get -y install libxslt-dev

echo "mysql-server-5.1 mysql-server/root_password password $datebase_root_password" | debconf-set-selections
echo "mysql-server-5.1 mysql-server/root_password_again password $datebase_root_password" | debconf-set-selections
apt-get -y install mysql-server

apt-get -y install libmysqlclient-dev
apt-get -y install mysql-client
apt-get -y install apache2
apt-get -y install libapache2-mod-wsgi
apt-get -y install tcl8.4

if [ "$datebase_name" != "" ]; then
    echo "CREATE DATABASE $datebase_name default character set utf8;" > tmp.sql
    mysql -u root -p"$datebase_root_password" < tmp.sql
    rm tmp.sql
fi

apt-get -y install libjpeg8-dev
apt-get -y install zlib1g-dev
apt-get -y install libfreetype6-dev
apt-get -y install liblcms1-dev
ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/
ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/
ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/
ln -s /usr/lib/x86_64-linux-gnu/liblcms.so /usr/lib/

# for mysql-python
easy_install -U distribute

adduser --system --no-create-home --disabled-login --disabled-password --group celery

mkdir /var/www/django
cd /var/www/django/

git clone https://github.com/johnnyliao/the_parent.git

cd the_parent/
chmod 777 -R *
pip install -r requirements/project.txt
python manage.py collectstatic --noinput
chmod 777 -R *
python manage.py createdb

cp deploy/envvars /etc/apache2/
cp deploy/rc.local /etc/

cp deploy/000-the_parent /etc/apache2/sites-enabled/
rm -f /etc/apache2/sites-enabled/000-default

reboot
