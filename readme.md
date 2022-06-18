# smart rainwater cistern

## About this project
A smart rainwater cistern keeps your rainwater tank from drying out. This IoT-system knows when your cistern is getting empty and will fill him automatically afterwards.

The water level of a tank is continuously measured by an ultrasonic sensor. After a preset value has been reached, an electro valve will open causing drinking water to stream into your cistern. 

This way, your rainwater tank will never be out of water ever again!

## Setting things up
### Clone the repository
clone this repository on your Raspberry Pi
<html>
 <code>
   git clone https://github.com/howest-mct/2021-2022-projectone-DauweQuinten.git
 </code>
</html>
 
<br>This repo is structured as mentioned below:
- backend: This folder contains all the logic that keeps the program running.
- database-export: This folder contains a dumb of the  SQL-database. We will import this database later.
- fritzing-schema : Here you can find everything you need to build the electronic circuit. 
- front-end: In this folder you'll find all the code that makes up the website. 


### Import the database
Now you're ready to import the sql-database.<br>
Open mySQL Workbench and make a new connection with your Raspberry Pi. Your Raspberry Pi will need MariaDB for this project.<br>
Install MariaDB
<html>
 <code>
   apt install mariadb-server mariadb-client -y
 </code>
</html><br>
- Open the dumb file of the database en click on execute script
- If everyting goes as expected, your database will now be imported! 


## Inhoud
Zoals je kan zien is er geen "vaste" structuur voor zo'n document. Je bepaalt zelf hoe je het bestand via markdown structureert. Zorg ervoor dat het document minimaal op volgende vragen een antwoord biedt.

- Wat is de structuur van het project?
- Wat moet er gebeuren met de database? Hoe krijgt de persoon dit up and running?
- Moeten er settings worden veranderd in de backend code voor de database? 
- Runt de back- en front-end code direct? Of moeten er nog commando's worden ingegeven?
- Zijn er poorten die extra aandacht vereisen in de back- en/of front-end code?
  
## Instructables
Plaats zeker een link naar de Instructables zodat het project kan nagebouwd worden!
