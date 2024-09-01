from unittest import TestCase

from requests import Session

import pytest

import random

import string

class TestAuth(TestCase):
    _base = "https://localhost:8000/api/v1"
    _headers = {
            "Content-Type": "application/json",
            "User-Agent": "Testing-platform"
        }
    _cert = ("../certs/cert.pem", "../certs/key.pem")
    _user = {}

    @classmethod
    def setUpClass(cls):
        cls._s = Session()

    @classmethod
    def url(cls, route):
        return cls._base + route
    
    @classmethod
    def gen_random(self):
        return "".join(random.choices(string.ascii_lowercase, k=15))
    
    @classmethod
    def gen_creds(self) -> dict:
        email = self.gen_random() + "@email.com"
        password = self.gen_random()
        return {
            "email": email,
            "password": password
        }

    @pytest.mark.order(1)
    def test_register_login(self):
        TestAuth._user = self.gen_creds()
        res = self._s.post(url=self.url("/auth/register"), json=self._user, headers=self._headers, verify=False)
        self.assertEqual(res.status_code, 200)
        email = res.json().get("data").get("email")
        self.assertEqual(self._user.get("email"), email)
        res = self._s.post(url=self.url("/auth/login"), json=self._user, headers=self._headers, verify=False)
        self.assertEqual(res.status_code, 200)

    @pytest.mark.order(2)
    def test_verify_token(self):
        token = self._s.cookies.get("auth")
        data = {"access_token": token}
        res = self._s.post(url=self.url("/auth/verify"), json=data, headers=self._headers, verify=False)
        self.assertEqual(res.status_code, 200)

    @pytest.mark.order(3)
    def test_get_info(self):
        res = self._s.get(url=self.url("/user/me"), headers=self._headers, verify=False)
        self.assertEqual(res.status_code, 200)
        email = res.json().get("data").get("email")
        self.assertEqual(email, TestAuth._user.get("email"))

    @pytest.mark.order(4)
    def test_logout(self):
        res = self._s.post(url=self.url("/auth/logout"), headers=self._headers, verify=False)
        self.assertEqual(res.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        cls._s.close()


    

