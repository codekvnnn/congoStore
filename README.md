# congoStore
Coding Dojo Group Project - eCommerce style site

Set up mySQL database, use mwb file or CongoStore.sql can be pasted into the mysql terminal to create the database with some test data I have been using.

Navigate to where you want to clone the repo in a terminal window.
Type : git clone https://github.com/mdejac/congoStore.git

This will pull the code from the repo and put in on your machine in a congoStore folder.
in congoStore folder type : git checkout -b MD_api_user_commit <-- make unique to you, and what you're going to work on
when you have finished your changes then type : git push origin MD_api_user_commit

backend/flask_app/config
	mysqlconnection.py - change user & password

Terminal window #1
congo/backend
	pipenv shell
	pipenv install
	python3 server.py
	

Terminal window #2
congo/frontend
	npm install
	npm run dev
