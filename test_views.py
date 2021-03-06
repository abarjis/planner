"""User View tests."""

# run these tests like:
#
# FLASK_ENV=production python -m unittest test_views.py

import os
from unittest import TestCase

from models import db, connect_db, User, Recipe, Category

os.environ['DATABASE_URL'] = "postgresql:///planner-test"

from app import app, CURR_USER_KEY

db.drop_all()
db.create_all()


app.config['WTF_CSRF_ENABLED'] = False

class ViewsTestCase(TestCase):
    """Test views."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.register(username="testuser",
                                    password="password",
                                    name="testuser",
                                    email="test@email.com")
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.register("test3", "password", "testname3", "email3@email.com")
        self.u1_id = 778
        self.u1.id = self.u1_id
        self.u2 = User.register("test4", "password", "testname4", "email4@email.com")
        self.u2_id = 884
        self.u2.id = self.u2_id
        self.u3 = User.register("test5", "password", "testname5", "email5@email.com")
        self.u3_id = 890
        self.u3.id = self.u3_id

        r = Recipe(title="test recipe", summary="test summary", recipe_id="3")
        self.r_id = r.id

        db.session.add_all([self.u1, self.u2, r])
        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp



    def test_profile(self):
        """ Test user profile """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            resp = c.get(f"/users/{self.u1_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username:', html)

    def test_register_page(self):
        """ Test register """
        with self.client as c:
            resp = c.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('</form>', html)


    def test_login_form(self):
        """Test user login"""
        with self.client as c:
            resp = c.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username', html)
            self.assertIn('</form>', html)


    def test_logout_user(self):
        """ Test user logout """
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.u2_id
            resp = c.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.u2_id, s)
            self.assertIn('You have successfully logged out.', html)


    def test_search_recipes(self):
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            resp = c.get(f"/users/{self.u1_id}/search?q=pasta")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Recipes search', html)

    def test_recipes(self):
        """ Test view recipes """
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.u3_id
            resp = c.get(f"/users/{self.u3_id}/recipes")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Recipes You Saved:', html)


    def test_view_recipe(self):


        r = Recipe(title="test recipe", summary="test summary", recipe_id="3", user_id=self.testuser_id)
        
        db.session.add(r)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            r = Recipe.query.get(3)

            resp = c.get(f"/users/{self.testuser_id}/recipes/{self.r_id}")
            html = resp.get_data(as_text=True)

            self.assertNotEqual(resp.status_code, 200)
            self.assertIn('title', html )

    def test_categories(self):
        """ Test view categories"""
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.u3_id
            resp = c.get(f"/users/{self.u3_id}/categories")
            html = resp.get_data(as_text=True)
           
            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Food Categories:', html)


    def test_generate(self):
        """ Test generate plan """
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.u1_id
            resp = c.get(f"/users/{self.u1_id}/generate")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('</h2>', html)


    def test_view_plan(self):
        """ Test view plan """
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.u1_id
            resp = c.get(f"/users/{self.u1_id}/view_plan")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('</h5>', html)


    def test_save_plan(self):
        """ Test save plan """
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.u1_id
            resp = c.get(f"/users/{self.u1_id}/details/save")
            html = resp.get_data(as_text=True)
            
            self.assertNotEqual(resp.status_code, 200)
            self.assertIn('title', html)


    def test_plan_details(self):
        """ Test plan details"""
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.u1_id
            resp = c.get(f"/users/{self.u1_id}/details")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 400)
            self.assertIn('title', html)

   
    def test_shopping_cart(self):
        """ Test Shopping cart"""
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.u1_id
            resp = c.get(f"/users/{self.u1_id}/shopping-list")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('item', html)