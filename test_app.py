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
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
                             "VCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYU"
                             "F4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04Znh"
                             "jdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiY"
                             "XV0aDB8NjA0NDMwZDAwZDlmNzEwMDcwZWU2NG"
                             "M3IiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWF"
                             "nZW5jeS8iLCJpYXQiOjE2MTUzOTE4MDcsImV4"
                             "cCI6MTYxNTQ2MzgwNywiYXpwIjoiR2hyT282c3"
                             "FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJz"
                             "Y29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdld"
                             "DphY3RvcnMiLCJnZXQ6bW92aWVzIl19.FkKa-"
                             "W777q1q_bOT2EWfJc7md4IYrY1zduNxzFmjDV"
                             "UNU9Okwz1NOYhVOvhhibo8AyhuA0OzJywYzhA"
                             "SrMmvWh1fclo3vl1-38pX5SM-d1WVoU2FlEy9"
                             "nNx7lVwTmMxs7bR9LvqFt7BBrgJLxTuAbIAz"
                             "qxnYS399YZRZUFCQVJvXqEgTN2aZ4ctrWn8V"
                             "MRXJ0wW4sUz_tBMoSSAUHPE9cj-IlzOqorE-"
                             "riQ9qGJC8x3ks44e9LXXp650QvZ859EEIyxh"
                             "j5YvHV2BMj0_1AUcCl8qdD2n6jIzaaPbwyq"
                             "nzbAB3bb7gBBusO3hNI6Lyb4sytG_zihjEu"
                             "epdF-9oP0NQQ"
        }
        self.casting_director = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVC"
                             "IsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4Vi"
                             "J9.eyJpc3MiOiJodHRwczovL2Rli04ZnhjdGxlYy"
                             "51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NW"
                             "Y3NzUzNWRiNDkZTIwMDZiOTQyNDNkIiwiYXVkIjo"
                             "iaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXi"
                             "OjE2MTUwOTA1OTYsImV4cCI6MTYxNTA5Nzc5Niwi"
                             "YXpwIjoiR2hyT282c3FkU2paYtxMnB1QlB2d1Zac"
                             "mdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Np"
                             "b25zIjpbImRlGV0ZTphY3RvcnMiLCJnZXQ6YWN0"
                             "b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG"
                             "9cyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b"
                             "3JzIl19.OFnRS8gpESVH3MGzvbiy8uD2M9LebwGM"
                             "plJR2FzyZJArgI6AmJhHAlGdin1P9mJRRw3-CCA"
                             "sNAEcTpy_eTx_HM2ddKTAFCdlRUXiQJRE4yyZvgJ"
                             "Vn4NR0wdXn8VvAIDGiHKJEDxKqSi83NWOnHztkI"
                             "EbpbEJcseXW9bP0SS3W1SMxxerxgEewmvb1T0nU"
                             "dPgJTY5d9zd99a-ick6k65IlqMQH9wA2Ka49CRO"
                             "HgizgC7VJmuYHDype8whC6yLG6eonuAhNDfVo40"
                             "WbNX3HgDDumuXUeJJ3Z3aQ0PEkS0-lmL7XehpVv"
                             "-tpuTFv5ZhXdF0XHriaTYftMsKGGQ6w"
        }
        self.casting_producer = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtp"
                             "ZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOi"
                             "JodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb"
                             "20vIiwic3ViIjoiYXV0aDB8NWY3NzUzOWNiYmJkODIwMDY4"
                             "NjlmNDZjIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5"
                             "jeS8iLCJpYXQiOjE2MTUxNTY4MjEsImV4cCI6MTYxN"
                             "TIyODgyMSwiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d"
                             "1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25"
                             "zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92a"
                             "WVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRj"
                             "aDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG"
                             "9ycyIsInBvc3Q6bW92aWVzIl19.WZcKzjRwdQ-L-_UVWdy"
                             "xvlCIJ_NP0W9AA2CKFW6my4RUqY7d_IWcQCkY4LNXIuT5W"
                             "obTAqTTQ0j1znQ9D98CjaDMx2aFLh0v3Ts8bZFPwviMCa"
                             "gxwB1-jJ69pO7CBCwkzcvYk8g5tuWm2ZwxbgdHMafqg"
                             "Ao_vPszM42zbg6HbjPw_I8CeNy9T7q3qMS3jKaEnscd"
                             "QPDSx3iQwcnZk9xRyMuooP10P4k6XaHsXqO8oBtQs_Q2h"
                             "tDVK5D-s3gZSqrZXYtAw2falq88EhDtvK-IJHri35UVy-K"
                             "ZoIRYFISSH5CngFeHZqpP_03ZZ23IPBoI2lzTwYXdf4og"
                             "J9SCDHqvgA"
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
