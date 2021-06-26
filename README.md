# openLIMS

OpenLIMS is an open source Lab Information Management System. 
The basic idea behind OpenLIMS is to provide a system that works for anyone, without needing a dev team or expensive software. 

OpenLIMS was just born (June 2021), so any feedback is greatly appreciated! 

This software should be fully functional in its current state. 
However if you are looking to accomplish something else, please contact me and I will do my best to help!


Live demo at http://66.175.219.62/

admin login is admin@example.com pw is admin

feel free to play around, resets happen frequently


To give OpenLIMS a try:
1) clone this repo
2) setup a virtual python envoironment of your choice
3) pip install the requirements
4) run init_db.py to setup some demo data
5) run wsgi.py to test it out on your local machine

OpenLIMS is not quite ready for production use, however, if you would like to run it in production I recommend you switch to MySQL over SQLite in config.py.
For serving this application, Gunicorn is my favorite tool, but feel free to use whatever you'd like.

Again, if you need any help using this, please message me!