# Gantt Chart project for DMD2 course
## Instalation
Here you may see the installation process of the application:

1. Download this repository to your local computer.

   ``` git clone https://github.com/Nnigmat/Guntt-chart ```

2. Run the following command in your terminal 

   ```pip3 install -r requirements```.

3. Install postgresql
4. Create user 'postgres' with password 'postgres'
5. Create 'testdb' database

## Run project
After the installation, you need to perform the following commands to run the project:
1. todo: Download and create the Postgres NoSql database 
2. Run the following commands in your terminal
   ```export FLASK_APP = app.py```.

3. To check the queries and run the project finally, you need to write
command ```flask run``` in the terminal.

## Project description
Gantt Charts are one of the most powerful
tools for seeing your path from 0–100%
and identifying where issues might creep up.
In our application you will be able to use
Gantt Chart with visual representation
of events with theirs starting and ending dates.
Also you can easily find events and who is responsible for them, when tasks start and finish
and how long they should take and some other features.

Geospatial search in application is the distance function between the events.
The closest Manhattan distance from the source to the destination, the better
will be score for the destination. Source and destination points is formed from
two values: starting date of the event and ending date of the event.
This project was done by four students from Innopolis University:
* Enes Ayan – B17-07
* Salavat Dinmukhametov – B17-07
* Almir Mullanurov – B17-06
* Nikita Nigmatulling – B17-07
