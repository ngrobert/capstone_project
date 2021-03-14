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


### API endpoints
```
- GET /actors
    - Fetches list of actors
    - Request argument: none
    - Returns success and list of actors
{
	"actors": [{
			"age": 21,
			"gender": "Male",
			"id": 1,
			"name": "Brad Pitt"
		}
	],
	"success": true
}

- GET /movies
    - Fetches list of movies
    - Request argument: none
    - Returns success and list of movies
{
	"movies": [{
			"id": 1,
			"title": "Forest Gump",
			"release_date": "2011-01-01"
		}
	],
	"success": true
}

- POST /actors
    - Adds actor to the database
    - Request arguments: name, age, and gender
{
    "age": 22,
    "gender": "Female",
    "id": 2,
    "name": "Jennifer Aniston"
}
    - Returns success and list of actors including what is passed in the request
{
	"actors": [{
			"age": 21,
			"gender": "Male",
			"id": 1,
			"name": "Brad Pitt"
		},
		{
			"age": 22,
			"gender": "Female",
			"id": 2,
			"name": "Jennifer Aniston"
		}
	],
	"success": true
}

- POST /movies
    - Adds movie to the database
    - Request arguments: title and release date
{
    "id": 2,
    "title": "Fight Club",
    "release_date": "2021-02-02"
}
    - Returns success and list of movies including what is passed in the request
{
	"movies": [{
			"id": 1,
			"title": "Forest Gump",
			"release_date": "2011-01-01"
		},
		{
			"id": 2,
			"title": "Fight Club",
			"release_date": "2021-02-02"
		}
	],
	"success": true
}

- PATCH /actors/<int:id>
    - Updates information of actor id specified
    - Request argument: any name, age, and/or gender combination
{
    "age": 121,
    "gender": "Female",
    "id": 1
}
    - Returns success and actor object with updated values from request
{
	"actors": [{
			"age": 121,
			"gender": "Female",
			"id": 1,
			"name": "Brad Pitt"
		}
	],
	"success": true
}

- PATCH /movies/<int:id>
    - Updates information of movie id specified
    - Request argument: any title and/or release_date combination
{
    "id": 2,
    "title": "Foo Bar"
}
    - Returns success and movie object with updated values from request
{
	"movies": [
		{
			"id": 2,
			"title": "Foo Bar",
			"release_date": "2021-02-02"
		}
	],
	"success": true
}

- DELETE /actors/<int:id>
    - Removes specified actor from database
    - Request argument: none
    - Returns success and deleted actor id
{
  "delete": 1,
  "success": true
}

- DELETE /movies/<int:id>
    - Removes specified movie from database
    - Request argument: none
    - Returns success and deleted movie id
{
  "delete": 1,
  "success": true
}
```
    

    
### Role Based Access Controls
```
    * Casting Assistant has the following permissions:
        - GET /actors
        - GET /movies
    * Casting Director has the following permissions:
        - GET /actors
        - GET /movies
        - POST /actors
        - PATCH /actors
        - PATCH /movies
        - DELETE /actors
    * Executive Producer has the following permissions:
        - GET /actors
        - GET /movies
        - POST /actors
        - POST /movies
        - PATCH /actors
        - PATCH /movies
        - DELETE /actors
        - DELETE /movies
```
        
        
### Authentication (bearer tokens)
Casting assistant
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NDMwZDAwZDlmNzEwMDcwZWU2NGM3IiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTU1MjE1NTIsImV4cCI6MTYxNTU5MzU1MiwiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.YguobDkRrWR66UZXugJGnYJ70LsKC6LUzHrbPYLU6Qgky576eVEJNpXQYwlX1VwynDZYLji8DrVAuTktoFYz73tTX77ZYl4G5a1jMMpLEUwIoayBUpTIsUyAyl_DAv2S55DHAbzpqjsG-Pp3GdMovPioux90KNEHCTiRrCwmCt1DuN_7tM-FIrGWUIYB6iDdZ9d0iZpNnR3a3vNQaw1xf7ryKIrkDifm6sA7JcYJlhJRhIj750QUrqsID4kh7XL4glsHM7QGKSAkA0olitZ9qBlWqsKnRnWHiCcOB3J5ZQAW5lH1fVq-QiLtRMYPwMDbAhrNZAF6bwkf20e2FTkUJQ
```
Casting director
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NzUzNWRiNDk4ZTIwMDZiOTQyNDNkIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTU1MjA4NDcsImV4cCI6MTYxNTU5Mjg0NywiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.BuJAlW8J5WxAvQZB9a3ZNlgTpn0VVNiDBL9tW_Uae6iNg9Qg87xTa10Yg93uhHi0VI_hjr4mGwmzoGyIK1oebUOCrZzKypXRQK6yfZDr4N8NdrBQo1jIV7aUNX1gZe96hp8exnll0zEL-HvdpDYDd9Z5BqfbI80Kg8WBan2k5SRbqvShc4WlzbstVP2LBgiQ2_A4EqR0yOP-ssJn8FVh7Dnqv-4WYvWbiNk-yX2KFMeo1wCWdPP2AcwC-AhfwHspo5_taS8zdMUP3gsNAAzvmIjgXkiecD3S3J_uAqe6s_YetpO415kuYDbUNZ5beYWQ_5x98823iLoFAqw0I0kdWg
```
Executive producer
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NzUzOWNiYmJkODIwMDY4NjlmNDZjIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTU3MDE3NjUsImV4cCI6MTYxNTc3Mzc2NSwiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.HDEqupExaB2l08pZNo9KVbRNHSXSTN1rw1HKJVfdgp9ENV7yOzvOnPDy5OJxi4Rc_E9APq47UcVtibRe_ZA7qiXGRn7Pfm2xmI-bj8P8Oa19C8jzdZETZCJXdid7na8OgJ1zCVl58rIb2lYqn-Y9bZ2IX274mig_pdO46pwzE11ApY0vmRr0l70_mHw4Pn77n-gIk11IpxzOaQt7xr9KwIMOXKgcHe1mbzy6vzqaJ4Qyc8L3UiAXMS6H0slaVc0mijxxlxZ1okywCY7TjCePy4OYuq4CxyJs1M-MN2mjh5alcEDgH9-GVf7kj_QrBBu3-0_Cumsa-0ULujUMBusRbQ
```
