# smart rainwater cistern

## About this project
A smart rainwater cistern keeps your rainwater tank from drying out. This IoT-system knows when your cistern is getting empty and will fill him automatically afterwards.

The water level of a tank is continuously measured by an ultrasonic sensor. After a preset value has been reached, an electro valve will open causing drinking water to stream into your cistern. 

This way, your rainwater tank will never be out of water ever again!

## Setting things up
### Clone the repository
clone this repository on your Raspberry Pi

    git clone https://github.com/howest-mct/2021-2022-projectone-DauweQuinten.git

 
<br>This repo is structured as mentioned below:
- backend: This folder contains all the logic that keeps the program running.
- database-export: This folder contains a dumb of the  SQL-database. We will import this database later.
- fritzing-schema : Here you can find everything you need to build the electronic circuit. 
- front-end: In this folder you'll find all the code that makes up the website. 


### Install MariaDB

    apt install mariadb-server mariadb-client -y


### Import the database
Now you're ready to import the sql-database. Open mySQL Workbench and make a new connection with your Raspberry Pi.
<br>Open the dumb file of the database en click on execute script
<br>If everyting goes as expected, your database will now be imported! 


### Database configuration
<br>Make a new file named "config.py" and insert the code below.

    [connector_python]
    user = USER_HERE
    host = 127.0.0.1
    port = 3306
    password = PWD_HERE
    database = DATABASENAME_HERE

    [application_config]
    driver = 'SQL Server'

Edit the code ebove so it matches your configuration:
- user
- host
- password
- database name
 
### Install Apache

<html>
 <code>
   apt install Apache2 -y
 </code>
</html>

### Install python
Install python by going to the extensions tab of Visual Studio Code. Search for  "python" and click on "install on *your IP-address*".

### Install Python packages

- `pip install flask-cors`
- `pip install flask-socketio`
- `pip install mysql-connector-python`
- `pip install gevent`
- `pip install gevent-websocket`
- 
### Run app.py

Now you can start the backend by running the file "app.py". You can find this file in the backend folder. You will have some errors if you haven't installed the sensors yet. Those errors should be fixed once every device is connected. You can find the electronic schematics in the "fritzing-schema" folder

### setup Apache server

Open the file below

    nano /etc/apache2/sites-available/000-default.conf
    
Search for the line `DocumentRoot /var/www/html` en change it as below

    DocumentRoot/home/<username>/<name_of_your_repo>/front-end

Close and save the file.

Now you have to restart the server:

    service apache2 restart
    
Now open this file:
    nano /etc/apache2/apache2.conf
    
 search for the text below:
 
    <Directory />
      Options FollowSymLinks
      AllowOverride All
      Require all denied
    </Directory>
 
 and change it to:
 
    <Directory />
      Options Indexes FollowSymLinks Includes ExecCGI
      AllowOverride All
      Require all granted
    </Directory>


Close and save the file.

Now you have to restart the server again:

    service apache2 restart

check if the server is up and running:

    service apache2 status

You should get the output below:

    Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset:enabled)
    Active: active (running) since ...



## Inhoud
Zoals je kan zien is er geen "vaste" structuur voor zo'n document. Je bepaalt zelf hoe je het bestand via markdown structureert. Zorg ervoor dat het document minimaal op volgende vragen een antwoord biedt.

- Wat is de structuur van het project?
- Wat moet er gebeuren met de database? Hoe krijgt de persoon dit up and running?
- Moeten er settings worden veranderd in de backend code voor de database? 
- Runt de back- en front-end code direct? Of moeten er nog commando's worden ingegeven?
- Zijn er poorten die extra aandacht vereisen in de back- en/of front-end code?
  
## Instructables
Plaats zeker een link naar de Instructables zodat het project kan nagebouwd worden!
