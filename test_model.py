"""User model tests."""

# run these tests like:
#
# python -m unittest test_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError

from models import db, User, Category, Recipe


os.environ['DATABASE_URL'] = "postgresql:///planner-test"


from app import app


db.create_all()

class UserModelTestCase(TestCase):
    """Test views for recipes."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.register("test1", "password", "testname1", "email1@email.com")
        uid1 = 1111
        u1.id = uid1

        u2 = User.register("test2", "password", "testname2", "email2@email.com")
        uid2 = 2222
        u2.id = uid2

        r = Recipe(title="recipe_test", summary="summary_test", recipe_id="5")

        db.session.add_all([u1, u2, r])
        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)


        self.r = r
        self.r_id = r.id


        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def testUserModel(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            password="HASHED_PASSWORD",
            name="testname",
            email="test@email.com"
            )

        db.session.add(u)
        db.session.commit()

        # User should have no recipes & no categories
        self.assertEqual(len(u.recipes), 0)
        self.assertEqual(len(u.categories), 0)



    ####
    #
    # Signup Tests
    #
    ####
    def test_valid_signup(self):
        u_test = User.register("testtesttest", "password", "testname", "testtest@email.com")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertNotEqual(u_test.password, "password")
        self.assertEqual(u_test.name, "testname")
        self.assertEqual(u_test.email, "testtest@email.com")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))


    def test_invalid_email_signup(self):
        invalid = User.register("testtest", "password", "testname1", None)
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.register("testtest", "", "testname1", "email@email.com")
    
    ####
    #
    # Authentication Tests
    #
    ####
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))



    def testRecipeModel(self):
        """ Does basic model work? """
        r = self.r
        self.assertEqual(r.id, self.r_id)
        self.assertIsInstance(r, Recipe)
        self.assertEqual(r.title, "recipe_test")
        self.assertEqual(r.summary, "summary_test")


    def testUserRecipes(self):
        u1 = self.u1
        r = self.r

        self.assertNotIn(r, u1.recipes)
        u1.recipes.append(r)
        db.session.commit()

        self.assertIn(r, u1.recipes)


    def test_add_recipe(self):
        """ test add a new recipe """

        u1 = self.u1
        rcp = Recipe(title='newRecipe', summary="newSummary", recipe_id="1010")
        self.u1.recipes.append(rcp)
        db.session.commit()

        self.assertEqual(len(u1.recipes), 1)
        self.assertIn(rcp, u1.recipes)
        self.assertEqual(u1.recipes[0].title, rcp.title)
        self.assertEqual(u1.recipes[0].summary, rcp.summary)