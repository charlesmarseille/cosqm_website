###----------------------------
#Install instructions to setup environment for flask website. 
#Cosqm data is read from the PI server which uploads steadily the data of cosqms are the globe. 
#Some data is corrupted and is neglected in the final form of the code. 
#This serves as a simple data viewer for debug purposes if anything goes wrong with the instruments. 
#When the network expands, the additional stations will be added to #the website for viewing.
###----------------------------

#(mainly following https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps with tweaks,
#perks and special calls (virtualenv selection from .wsgi file) to activate functions. Note that the absolute and relative paths are 
#not always solutions, you must be careful to set them correctly!!)

##Update server, install python 
sudo apt-get update
apt-get install python3.6
sudo chmod -R 777 /home/ 	#if user, no need if root
sudo apt install apache2	#needs to be setup and tested before going further
sudo apt install git
sudo apt install libapache2-mod-wsgi-py3


##Download code from github
sudo mkdir /var/www/cosqm_website
cd /var/www/cosqm_website
git clone https://github.com/charlesmarseille/cosqm_website.git
cd /var/www/cosqm_website/cosqm_website

##Make virtual environment for python3.6
virtualenv flaskenv --python=/usr/bin/python3	#confirm this is indeed 3.6 or higher as of tested versions
source /var/www/cosqm_website/cosqm_website/flaskenv/bin/activate 	#the .wsgi file activates the virtualenv when called by apache2, so here it is just to test the venv

##install dependencies
/var/www/cosqm_website/cosqm_website/flaskenv/bin/python3 -m pip install virtualenv flask matplotlib pytest-shutil wget pandas


##create wsgi server app setting file##

vim /var/www/cosqm_website/cosqm_website.wsgi


#type <i> to input text, copy-paste the following (be sure python version is right!):

activate_this = '/var/www/cosqm_website/cosqm_website/flaskenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.append('/var/www/cosqm_website/cosqm_website/flaskenv/lib/python3.6/site-packages')
sys.path.insert(0,"/var/www/cosqm_website")

from cosqm_website import app as application
application.secret_key = 'lumin007'
#type '<esc> :wq' to save and close file



#configure apache server
sudo vim /etc/apache2/sites-available/cosqm_website.conf

#in which you add all following lines (ServerName is the PUBLIC IP of the server, change this value and email!):
<VirtualHost *:80>
                ServerName 147.253.81.183
                ServerAdmin charles_marseille@hotmail.com
                WSGIScriptAlias / /var/www/cosqm_website/cosqm_website.wsgi
                WSGIApplicationGroup %{GLOBAL}
                <Directory /var/www/cosqm_website/cosqm_website/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/cosqm_website/cosqm_website/static
                <Directory /var/www/cosqm_website/cosqm_website/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
#then save file with ':wq'

#change ownership of folder to write files with wget command
sudo chown -R $USER:$USER /var/www/cosqm_website
sudo chmod 755 /var/www/cosqm_website/cosqm_website

#activate wsgi module
sudo a2enmod wsgi

#activate the server
sudo a2ensite cosqm_website

#restart service
sudo service apache2 restart 

#All done! Now, test to make sure all functionnalities work. Email charles_marseille@hotmail.com if you encounter problems or bugs.
#Type in a browser the ip address you assigned to the server page in the wsgi file to access the server. You can also redirect from a vpn or vps.
