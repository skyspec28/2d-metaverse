import unittest
import random
from selenium import webdriver
from django.test import TestCase
from django.http import HttpRequest
import requests


BACKEND_URL = 'http://localhost:8000/'
class AuthenticationTest(unittest.TestCase):

    def test_user_is_able_signup_once(self):
        username ="dave"+ str(random.randint(0 , 10))
        password = "123456"
        
        
        response = requests.post(f"{BACKEND_URL}/api/v1/signup" , data={
            'username': username,
            'password': password,
        })

        self.assertEqual(response.status_code, 201)
        
        response_duplicate = requests.post(f"{BACKEND_URL}/api/v1/signup", data={
            'username': username,
            'password': password,
            
        })

        self.assertEqual(response_duplicate.status_code ,409)

    def test_signup_request_fail_if_username_is_empty(self):
        username ="dave"+ str(random.randint(0 , 10))
        password = "123456"
        
        response = requests.post(f"{BACKEND_URL}/api/v1/signup", data={
            'password': password,
            
        })
        self.assertEqual(response.status_code ,400)

    def test_signin_succeced_if_usename_and_password_is_correct(self):
        username ="dave"+ str(random.randint(0 , 10))
        password = "123456"

        response_signup = requests.post(f"{BACKEND_URL}/api/v1/signup", data={
            'username': username,
            'password': password,
        })

        self.assertEqual(response_signup.status_code, 201)

        response_signin = requests.post(f"{BACKEND_URL}/api/v1/signin", data={
            'username': username,
            'password': password,
        })

        self.assertEqual(response_signin.status_code, 200)
        self.assertIn('token', response_signin.json())

    def test_signin_fails_if_username_and_password_is_incorrect(self):
        username = "dave" + str(random.randint(0, 10))
        password = "123456"

        # Test with an incorrect username
        response = requests.post(f"{BACKEND_URL}/api/v1/signin", data={
            'username': 'WRONG USERNAME',
            'password': password,
        })
        self.assertEqual(response.status_code, 401)  # Asserts that the status code is 401 (Unauthorized)

        # Test with an incorrect password
        response = requests.post(f"{BACKEND_URL}/api/v1/signin", data={
            'username': username,
            'password': 'WRONG PASSWORD',
        })
        self.assertEqual(response.status_code, 401)  # Asserts that the status code is 401 (Unauthorized)

class UserInformationEndpointTest(unittest.TestCase):
    token=""
    avatar_id =""


    def setUp(self):  #runs this first 
        self.username = "dave" + str(random.randint( 0, 10))
        self.password = "123456"

        response_signup = requests.post(f"{BACKEND_URL}/api/v1/signup", data={
            'username': self.username,
            'password': self.password,
        })
       

        response_signin = requests.post(f"{BACKEND_URL}/api/v1/signin", data={
            'username': self.username,
            'password': self.password,
        })
        self.token = response_signin.json()['token']

    def test_User_cant_update_their_metadata(self):
        # Attempt to update user metadata without authorization
        response = requests.post(f"{BACKEND_URL}/api/v1/user/metadata", data={
            "avatar_id": avatar_id
        })
        self.assertEqual(response.status_code, 403)  # Forbidden status code

        # Create an avatar with authorization
        avatar_response = requests.post(
            f"{BACKEND_URL}/api/v1/avatar",
            data={
                "image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRCRca3wAR4zjPPTzeIY9rSwbbqB6bB2hVkoTXN4eerXOIkJTG1GpZ9ZqSGYafQPToWy_JTcmV5RHXsAsWQC3tKnMlH_CsibsSZ5oJtbakq&usqp=CAE",
                "name": "test avatar"
            },
            headers={
                "Authorization": f"Bearer {self.token}"
            }
        )

        # Validate avatar creation response
        self.assertEqual(avatar_response.status_code, 201, "Avatar creation failed")
        
        # Extract avatar ID from the response
        avatar_data = avatar_response.json()  # Convert JSON response to Python dict
        avatar_id = avatar_data.get("avatar_id")
        self.assertIsNotNone(avatar_id, "Avatar ID is missing in the response")

class UserAvatarInfoormation(unittest.TestCase):
    token=""
    user_id=""

        
    def setUp(self):  #runs this first 
        self.username = "dave" + str(random.randint( 0, 10))# 
        self.password = "123456"

        response_signup = requests.post(f"{BACKEND_URL}/api/v1/signup", data={   #signup
            'username': self.username,
            'password': self.password,
        })
        user_id =response_signup.json().get("userId")
    

        response_signin = requests.post(f"{BACKEND_URL}/api/v1/signin", data={  #signin 
            'username': self.username,  
            'password': self.password,
        })
        self.token = response_signin.json()['token']  # gets a token

        avatar_response = requests.post(
            f"{BACKEND_URL}/api/v1/avatar",
            data={
                "image": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRCRca3wAR4zjPPTzeIY9rSwbbqB6bB2hVkoTXN4eerXOIkJTG1GpZ9ZqSGYafQPToWy_JTcmV5RHXsAsWQC3tKnMlH_CsibsSZ5oJtbakq&usqp=CAE",
                "name": "test avatar"
            },
            headers={
                "Authorization": f"Bearer {self.token}"
            }
        )
        
        avatar_data = avatar_response.json()  # Convert JSON response to Python dict
        avatar_id = avatar_data.get("avatar_id")


        

if __name__ == "__main__":
    unittest.main()