# Casting Agency
This project models a company's system that creates movies and manages and assigns actors to those movies. 

This final project encompasses everything taught throughout the Fullstack Web Developer Udacity Nanogree course. 
1) SQLAlchemy to conduct database queries
2) RESTful principles of API development
3) Structure endpoints to respond to (GET, PATCH, POST, DELETE) HTTP methods
4) Enable Role Based Authentication and roles-based access control (RBAC)



## Project Dependencies
This project requires python 3.7 or greater to be installed [python docs](https://wiki.python.org/moin/BeginnersGuide/Download)


### Local Environment
To start and Development the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=app && export FLASK_ENV=development && flask run
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)



* Documentation of API behavior and RBAC controls
