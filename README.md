# Casting Agency
This project models a company's system that creates movies and manages and assigns actors to those movies. 

This final project encompasses everything taught throughout the Fullstack Web Developer Udacity Nanogree course. 
1) SQLAlchemy to conduct database queries
2) RESTful principles of API development
3) Structure endpoints to respond to (GET, PATCH, POST, DELETE) HTTP methods
4) Enable Role Based Authentication and roles-based access control (RBAC)



## Project Dependencies
This project requires python 3.7 or greater to be installed [python docs](https://wiki.python.org/moin/BeginnersGuide/Download)

Tech stack:
- SQLAlchemy to interact with the database
- Postman to evaluate API endpoints
- Heroku to host



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
For linux:
  ```
  $ export FLASK_APP=app && export FLASK_ENV=development && flask run
  ```
For windows:
  ```
  $ set FLASK_APP=app && set FLASK_ENV=development && flask run
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
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NDMwZDAwZDlmNzEwMDcwZWU2NGM3IiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTYxMDE2NzcsImV4cCI6MTYxNjE3MzY3NywiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.PvLB3ta5IaxBKtNtkVS_VH6tBhrwl6mmHndqIj5Ae4U_HrCNwkvu9SB7Qx98k6BuuHudMdW5X8vb8j-8vxgLfebvM0tGztCr2YFJ3qCtZ7zLlQgzxjtquIjobw7dAQuI3ZS3IAQd5shnvxNIKoS50ISYltxPt9f7kngi6l6oW7VLniMcJzi7wIUB2lo9d22OzwtCeONqM8eXFEPAY6Cgk9InGY1IECQikLHm_YIKRqiAw9GNnAjxJmO3xpDkBjGtwUzA-v7xzI8ELmbz7Yl7sybntdtnpuUbVkklTK5M37QOYllMkZxRzgCYaKC2zs-K48Krd8OfJxKs9R_HAyrwOQ
```
Casting director
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NzUzNWRiNDk4ZTIwMDZiOTQyNDNkIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTYwMzM5NDAsImV4cCI6MTYxNjEwNTk0MCwiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.iixr8lemlQk1_TdDBKGpcvgkR_yfFk_cXhMKAvUh8F3ImY4z0FaMDRuj0NRbJlWLFH2rr7czcjNY23_1bfxa2gNrPmCG-XRMwIjrw64OG7dE77vVkeHGZXSvaMh5bkWhVzD6gx1cwK8UwX8NICuBa11WeNWvXBeZE-QbM5mMVfqViGS_NLk1URW93WTsS_E7IXy_khGt_8dcWvdmsn-dhmvz24BBA3o02JFArA52M6xZa5uHwEaWaCexH6dGU-tJlQMVmrtMGxVKFoiRUHbilyCAxJbgcGVQdmWHehKCBWvrhcNCSP99HSy9Fy6xz2S0XljCCCojSyKQVkgjjKkzMQ
```
Executive producer
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NzUzOWNiYmJkODIwMDY4NjlmNDZjIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTYwMzM4MDcsImV4cCI6MTYxNjEwNTgwNywiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.hBycF039mk2pUe2kYv-kBB_EX3VnSRZpXDz42sjQysjVKIwht-p_5sVCoDs3EdhzB_rxoGX6Pj31frRW_GJKynDbwpzG-Jk2N4wG-UtkKL-uPsobB_75G2t8rZQoBzFav4Gzzob8LVkqhvXXtvGrR0cUE6ibgMiHjqX75xEr-gn73e8zninA3uPLfvPBTjJ_Eeyqdit4YiOJFS13xDpm7YoWf9PubIydcFhs-JmAMye_m-9u-LFF8HLei6G01viQTAJmvWau5TD0yWfahzobpT7TJS--20bqHoJ2SJRHZVKfxE-ptO97dogTTvuzBET_H1RE-kGKbEdh1nAYLpEvSQ
```


### Heroku Website hosted: https://rnagency.herokuapp.com/ 