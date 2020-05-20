import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import APP
from database.models import db

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

        self.casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrXzZCV1ZMUFJLdi1LU1lDeVNJZSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTIwMjAuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzQ1OTQzZThmODZhMGJlYWMzNDhkOCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkwMDA0MTIwLCJleHAiOjE1OTAwNzYxMjAsImF6cCI6IkJvc3JqM09ZblFlbHhvMFBHZ1d6Z3R5R2lBbzY2UndoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.EM_hvk7J2oc3yBjguyOv9PKpSY8pumAIfB0oFFGrqpRKsLZRT-PkeGU-KNEgKBahS6Z15NpwuUpdj7Jt77ci22g_E8jYdPQZQrOxctD01IWDsPAZDFnVkqAxgFyx0uAJ55U5mHWgEc7i62KiyRfc0LEMOlciILHmENmgsQeLcYp_w21o1xPu8bpVlP0WWtq40Tzc6ON1GQA94cqGS0qyV6p0kCiHnziSBvEIB7chQ65zT6roAz90Q5ur7wzanoMuwyK-7JniQ3bGtRwFLHZoImOJ8Sq56Nr-iS-aTihIGW_cFgYB46K0FvnwGo_PhgPkWCi8IpOCKhCxVuOh6qQGpw'
        self.casting_director  = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrXzZCV1ZMUFJLdi1LU1lDeVNJZSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTIwMjAuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzQ0ODlmMGEzYjAzMGJmOTNjZWMwMiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkwMDAzNjc2LCJleHAiOjE1OTAwNzU2NzYsImF6cCI6IkJvc3JqM09ZblFlbHhvMFBHZ1d6Z3R5R2lBbzY2UndoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.dE7SP46pybUzO4bqRPOT32cioZbgVI2cQLVCQO9CxWoDpfcxpsyN9l0stmbVGzdKO4fU2lXzgIKoW2M1UKXtW8voAeRI7P47t0P3NGi3N0RVj5S6wNStUqrCvpodW_GTeKcY8L9Z9KnV1EXfz_27QfDhTzsYkk2FQmQ5Wzl1ESFYt_3OPoKm5uugvaSC4k_JDNXhVJHMKi4IYAIfirpLxfcax_uAMr2PTAw7eu236NqRPHBW35b8KXMVMc3edVc8Eg0O8cHa9q_xFEuaQiDRs4byWxSkq3nzIp94emSGtWpj9rkTwmsWD25k78BTSya6NnkmGeG8NTHz89efdCisyg'
        self.executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrXzZCV1ZMUFJLdi1LU1lDeVNJZSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTIwMjAuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzJlNDhkMGFkNGMzMGJmYzhmZGQ5NSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTg5OTkyMzE2LCJleHAiOjE1OTAwNjQzMTYsImF6cCI6IkJvc3JqM09ZblFlbHhvMFBHZ1d6Z3R5R2lBbzY2UndoIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Cn6tPsXvfEr2lj4uE73gYZ4SC4c3zwh0lLH7A7q1xEdeoGYTRQndPcbSp05yjqkfMpk5JYR3V5zsKC3gRqmY4cv7MOJSeKZFrnaoPVz7awyI2qLmkUl7hs-LVO7QCPOXKq-kI8XVsMYdMl_dI9WrnRQvKsZggq2sl15cvjRynbIfP5Vc3Ox0uOMQidHZeDCYnh8OUfdi577G-NSaHsOqFariemfB3pj5fbahtoooeK3X483x-XT2KeoRkCh1ytCaJV4bsbSBPj0nxAd9rQvpvcrZDd9v3Ng9RHV43nv_DnOv9ZZC_064ExgWc--cIhi-OfQABE0CAs25w6zz6fiDeQ'
        self.new_actor = {
              "name": "Marlon Brando",
              "role": "runner",
              "gender": "male",
              "movie_id": 1
              }
        self.new_movie = {
            "title": "Great title",
            "release_year": 2019
            }
        self.update_movie = {
            "title": "Dance Dance Dance",
            }   
        self.update_actor = {
            "role": "swimmer"
              }            
        # drop and create all tables
        db.drop_all()
        db.create_all() 

    def tearDown(self):
        pass

    """
    Test Cases
    """
    def test_get_all_actors_for_casting_assistant(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    def test_get_all_movies_for_casting_director(self):
        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)        
        
    def test_post_movie_for_executive_producer(self):
        res = self.client().post('/movies',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.executive_producer)
                                 }, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_post_actor_for_casting_director(self):
        res = self.client().post('/actors',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_director)
                                 }, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)    
        
    # def test_update_actor_for_casting_director(self):
        # res = self.client().patch('/actors/1',
                                 # headers={
                                     # "Authorization": "Bearer {}".format(
                                         # self.casting_director)
                                 # }, json=self.update_actor)
        # data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['success'], True)   
        
    # def test_update_movie_for_casting_director(self):
        # res = self.client().patch('/movies/1',
                                 # headers={
                                     # "Authorization": "Bearer {}".format(
                                         # self.casting_director)
                                 # }, json=self.update_movie)
        # data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['success'], True)                                           
                                 
        
    # def test_post_actor_for_casting_director(self):
        # res = self.client().post('/movies',
                                 # headers={
                                     # "Authorization": "Bearer {}".format(
                                         # self.casting_director)
                                 # }, json=self.new_movie)
        # data = json.loads(res.data)
        # self.assertEqual(res.status_code, 401)
        # self.assertEqual(data['success'], False)
        
if __name__ == "__main__":
    unittest.main()