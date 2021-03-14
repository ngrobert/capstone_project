"""
Casting agency tests
"""
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from app import create_app


# pylint: disable=too-many-instance-attributes, too-many-public-methods
class CastingAgencyTestCase(unittest.TestCase):
    """
    Casting agency test case
    """
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # mock database connection
        self.database_name = "castingagency"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # auth tokens for respective roles
        self.casting_assistant = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImt"
                             "pZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3Mi"
                             "OiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb"
                             "20vIiwic3ViIjoiYXV0aDB8NjA0NDMwZDAwZDlmNzEwMDc"
                             "wZWU2NGM3IiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFn"
                             "ZW5jeS8iLCJpYXQiOjE2MTU1MjE1NTIsImV4cCI6MTYxN"
                             "TU5MzU1MiwiYXpwIjoiR2hyT282c3FkU2paY2txMnB1Q"
                             "lB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3"
                             "Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl"
                             "19.YguobDkRrWR66UZXugJGnYJ70LsKC6LUzHrbPYLU"
                             "6Qgky576eVEJNpXQYwlX1VwynDZYLji8DrVAuTktoFYz"
                             "73tTX77ZYl4G5a1jMMpLEUwIoayBUpTIsUyAyl_DAv2S"
                             "55DHAbzpqjsG-Pp3GdMovPioux90KNEHCTiRrCwmCt1D"
                             "uN_7tM-FIrGWUIYB6iDdZ9d0iZpNnR3a3vNQaw1xf7ry"
                             "KIrkDifm6sA7JcYJlhJRhIj750QUrqsID4kh7XL4glsH"
                             "M7QGKSAkA0olitZ9qBlWqsKnRnWHiCcOB3J5ZQAW5lH"
                             "1fVq-QiLtRMYPwMDbAhrNZAF6bwkf20e2FTkUJQ"
        }
        self.casting_director = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImt"
                             "pZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3"
                             "MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC"
                             "5jb20vIiwic3ViIjoiYXV0aDB8NWY3NzUzNWRiNDk4ZT"
                             "IwMDZiOTQyNDNkIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW"
                             "5nLWFnZW5jeS8iLCJpYXQiOjE2MTU1MjA4NDcsImV4cC"
                             "I6MTYxNTU5Mjg0NywiYXpwIjoiR2hyT282c3FkU2paY2"
                             "txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsIn"
                             "Blcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZX"
                             "Q6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG"
                             "9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl"
                             "19.BuJAlW8J5WxAvQZB9a3ZNlgTpn0VVNiDBL9tW_Uae"
                             "6iNg9Qg87xTa10Yg93uhHi0VI_hjr4mGwmzoGyIK1oeb"
                             "UOCrZzKypXRQK6yfZDr4N8NdrBQo1jIV7aUNX1gZe96h"
                             "p8exnll0zEL-HvdpDYDd9Z5BqfbI80Kg8WBan2k5SRbq"
                             "vShc4WlzbstVP2LBgiQ2_A4EqR0yOP-ssJn8FVh7Dnqv"
                             "-4WYvWbiNk-yX2KFMeo1wCWdPP2AcwC-AhfwHspo5_ta"
                             "S8zdMUP3gsNAAzvmIjgXkiecD3S3J_uAqe6s_YetpO41"
                             "5kuYDbUNZ5beYWQ_5x98823iLoFAqw0I0kdWg"
        }
        self.casting_producer = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIs"
                             "ImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.ey"
                             "Jpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hd"
                             "XRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NzUzOWNi"
                             "YmJkODIwMDY4NjlmNDZjIiwiYXVkIjoiaHR0cHM6Ly9"
                             "jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTU3MDE3Nj"
                             "UsImV4cCI6MTYxNTc3Mzc2NSwiYXpwIjoiR2hyT282c"
                             "3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29w"
                             "ZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3R"
                             "vcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycy"
                             "IsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJw"
                             "YXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3"
                             "Q6bW92aWVzIl19.HDEqupExaB2l08pZNo9KVbRNHSX"
                             "STN1rw1HKJVfdgp9ENV7yOzvOnPDy5OJxi4Rc_E9AP"
                             "q47UcVtibRe_ZA7qiXGRn7Pfm2xmI-bj8P8Oa19C8j"
                             "zdZETZCJXdid7na8OgJ1zCVl58rIb2lYqn-Y9bZ2IX"
                             "274mig_pdO46pwzE11ApY0vmRr0l70_mHw4Pn77n-g"
                             "Ik11IpxzOaQt7xr9KwIMOXKgcHe1mbzy6vzqaJ4Qyc"
                             "8L3UiAXMS6H0slaVc0mijxxlxZ1okywCY7TjCePy4O"
                             "Yuq4CxyJs1M-MN2mjh5alcEDgH9-GVf7kj_QrBBu3-"
                             "0_Cumsa-0ULujUMBusRbQ"
        }

        self.new_actor = {
            "name": "Tom Hanks",
            "age": "21",
            "gender": "Male"
        }
        self.new_movie = {
            "title": "Forest Gump",
            "release_date": "1111-22-33",
        }

        # need to use functionality that interfaces with app
        # bind app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""

    # Tests for unauthorized user
    def test_no_access_get_actors(self):
        """
        Tests only role based access control users can view actors data
        """
        response = self.client().get('/actors', headers={
            "Authorization": "Bearer UNAUTHORIZED"
        })

        self.assertEqual(response.status_code, 401)

    def test_no_access_get_movies(self):
        """
        Tests only role based access control users can view actors data
        """
        response = self.client().get('/movies', headers={
            "Authorization": "Bearer UNAUTHORIZED"
        })

        self.assertEqual(response.status_code, 401)

    # Tests for casting assistant
    def test_assistant_get_actors(self):
        """
        Tests casting assistant can view actors data
        """
        response = self.client().get('/actors',
                                     headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_assistant_get_movies(self):
        """
        Tests casting assistant can view movies data
        """
        response = self.client().get('/movies',
                                     headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_assistant_post_actors(self):
        """
        Tests casting assistant cannot create actor
        """
        response = self.client().post('/actors',
                                      headers=self.casting_assistant,
                                      json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_post_movies(self):
        """
        Tests casting assistant cannot create movies
        """
        response = self.client().post('/movies',
                                      headers=self.casting_assistant,
                                      json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_patch_actors(self):
        """
        Tests casting assistant cannot update actor
        """
        response = self.client().patch('/actors/1',
                                       headers=self.casting_assistant,
                                       json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_patch_movies(self):
        """
        Tests casting assistant cannot update movies
        """
        response = self.client().patch('/movies/1',
                                       headers=self.casting_assistant,
                                       json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_delete_actors(self):
        """
        Tests casting assistant cannot delete actor
        """
        response = self.client().delete('/actors/1',
                                        headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_delete_movies(self):
        """
        Tests casting assistant cannot delete movies
        """
        response = self.client().delete('/movies/1',
                                        headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Tests for casting director
    def test_director_get_actors(self):
        """
        Tests casting director can view actors data
        """
        response = self.client().get('/actors',
                                     headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_director_get_movies(self):
        """
        Tests casting director can view movies data
        """
        response = self.client().get('/movies',
                                     headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_director_post_actors(self):
        """
        Tests casting director can create actor
        """
        total_actors_before = len(Actor.query.all())
        response = self.client().post('/actors',
                                      headers=self.casting_director,
                                      json=self.new_actor)
        data = json.loads(response.data)
        total_actors_after = total_actors_before + 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(total_actors_after, 1)

    def test_director_post_movies(self):
        """
        Tests casting director can create movies
        """
        response = self.client().post('/movies',
                                      headers=self.casting_director,
                                      json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_director_patch_actors(self):
        """
        Tests casting director can update actor
        """
        before_update = self.client().get('/actors',
                                          headers=self.casting_director)
        before_update = json.loads(before_update.data)["actors"][0]
        update_actor = {'name': before_update["name"] + "S"}
        response = self.client().patch('/actors/24',
                                       headers=self.casting_director,
                                       json=update_actor)
        data = json.loads(response.data)
        after_update = data["actors"][0]

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_director_patch_movies(self):
        """
        Tests casting director can update movies
        """
        before_update = self.client().get('/movies',
                                          headers=self.casting_director)
        before_update = json.loads(before_update.data)["movies"][0]
        update_movie = {'title': before_update["title"] + "S"}
        response = self.client().patch('/movies/10',
                                       headers=self.casting_director,
                                       json=update_movie)
        data = json.loads(response.data)
        after_update = data

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_director_delete_actors(self):
        """
        Tests casting director can delete actor
        """
        response = self.client().delete('/actors/25',
                                        headers=self.casting_director)
        data = json.loads(response.data)
        actor = Actor.query.filter(Actor.id == 25).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 25)
        self.assertEqual(actor, None)

    def test_director_delete_movies(self):
        """
        Tests casting director cannot delete movies
        """
        response = self.client().delete('/movies/1',
                                        headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Tests for casting producer
    def test_producer_get_actors(self):
        """
        Tests casting producer can view actors data
        """
        response = self.client().get('/actors',
                                     headers=self.casting_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_producer_get_movies(self):
        """
        Tests casting producer can view movies data
        """
        response = self.client().get('/movies',
                                     headers=self.casting_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_producer_post_actors(self):
        """
        Tests casting producer can create actor
        """
        total_actors_before = len(Actor.query.all())
        response = self.client().post('/actors',
                                      headers=self.casting_producer,
                                      json=self.new_actor)
        data = json.loads(response.data)
        total_actors_after = total_actors_before + 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(total_actors_after, 1)

    def test_producer_post_movies(self):
        """
        Tests casting producer can create movies
        """
        total_movies_before = len(Movie.query.all())
        response = self.client().post('/movies', headers=self.casting_producer,
                                      json=self.new_movie)
        data = json.loads(response.data)
        total_movies_after = total_movies_before + 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(total_movies_after, 1)

    def test_producer_patch_actors(self):
        """
        Tests casting producer can update actor
        """
        before_update = self.client().get('/actors',
                                          headers=self.casting_producer)
        before_update = json.loads(before_update.data)["actors"][0]
        update_actor = {'name': before_update["name"] + "S"}
        response = self.client().patch('/actors/24',
                                       headers=self.casting_producer,
                                       json=update_actor)
        data = json.loads(response.data)
        after_update = data["actors"][0]

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_producer_patch_movies(self):
        """
        Tests casting producer can update movies
        """
        before_update = self.client().get('/movies',
                                          headers=self.casting_producer)
        before_update = json.loads(before_update.data)["movies"][0]
        update_movie = {'title': before_update["title"] + "S"}
        response = self.client().patch('/movies/10',
                                       headers=self.casting_producer,
                                       json=update_movie)
        data = json.loads(response.data)
        after_update = data

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_producer_delete_actors(self):
        """
        Tests casting producer can delete actor
        """
        response = self.client().delete('/actors/25',
                                        headers=self.casting_producer)
        data = json.loads(response.data)
        actor = Actor.query.filter(Actor.id == 25).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 25)
        self.assertEqual(actor, None)

    def test_producer_delete_movies(self):
        """
        Tests casting producer cannot delete movies
        """
        response = self.client().delete('/movies/2',
                                        headers=self.casting_producer)
        data = json.loads(response.data)
        movie = Movie.query.filter(Movie.id == 25).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
        self.assertEqual(movie, None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
