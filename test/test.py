import unittest
import requests

class TestCase(unittest.TestCase):
    def test_root_server(self):
        response = requests.get('http://api.koooleposhti.ir/api/v1/')
        self.assertEqual('<h1 style="text-align: center;">Flask webserver working properly</h1>', response.text)
        self.assertEqual(200, response.status_code)

    def test_sign_up(self):
        signup_content = {
            "githubId" : "mayazdi",
            "beheshtiEmail" : "amin.yazdi@atrovan.co",
            "password" : "passwordeamn",
            "firstName" : "Amin",
            "lastName" : "Yazdi"
        }
        response = requests.post('http://api.koooleposhti.ir/api/v1/auth/signup', json=signup_content)

        self.assertTrue(409 == response.status_code or 201 == response.status_code)
        self.assertTrue({"error": "user already exists"} == response.json() or 'id' in response.json())
    
    def test_terms(self):
        response = requests.get('http://api.koooleposhti.ir/api/v1/terms')

        self.assertTrue(200 == response.status_code)
        self.assertTrue('lastModified' in response.json() and 'content' in response.json())


if __name__ == '__main__':
    unittest.main()