# Team and Project Tracking

Note: 
This project was only implemented as class project for a Software Engineering Course at the University of Louisville. The project has only been run in ubuntu 18.04 however, the following instructions should work in any python 3.6 virtual env.

To run this project in your local environment;

1. clone the repo by pasting this line in your terminal
    > git clone git@github.com:dmj2x/team_and_project_tracking.git

2. create a virtual environment (if you don't have one already) by pasting the following line in your terminal. This assumes you already have python 3 installed.
    > python3 -m venv myenv

3. while in the same folder, Activate your virtual environment by running the following line in your terminal
    > myenv/bin/activate

4. Install postgres database, [link to postgresql downloads](https://www.postgresql.org/download/) Then create a database and a user, and grant all access to the user created on the database.


5. Install the project dependencies. Go back to the terminal, navigate to the project folder, activate your virtual environment and run the following command
    > pip3 install -r requirements

6. create a .env file in the root folder of your project using the provide template, .env_temp file. Make sure to fill in the following fields appropriately. You may copy the .env_temp and and paste the text in your .env file however the following fields must be filled appropriatelu
   * SECRET_KEY= This should should be a unique sting like the used in .env_temp
   * DB_NAME= This shouls be the name of the database create in step 3.
   * DB_USER= This should be the user created in step 3.
   * DB_PASSWORD= This should be the password for the user created in step 3.


7. Apply migrations by running the following lines
    > python3 manage.py showmigrations
    > python3 manage.py makemigrations
    > python3 manage.py migrate

   if you are getting errors, check if you have all the dependencies, check file paths and project structure. At this stage, your project directory look like this;  
  
    - team_and_project_tracking
      - env
      - team_and_project_tracking
      - team_project_tracking
      - LICENSE
      - manage.py
      - README.md
      - requirements.text
      - .env

5. Start project. Run the following command to start the project.
    > python3 manage.py runserver

Once the command executes, you should be able to see the page in the screenshot below at this url http://127.0.0.1:8000/:
