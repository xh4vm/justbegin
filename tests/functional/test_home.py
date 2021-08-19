import json
from tests.functional.base import BaseTestCase
from app.home.exceptions import HomeExceptions


# class HomeTestCase(BaseTestCase):

#     def test_index_success(self):

#         with self.app.test_client() as test_client:
#             response = test_client.get('/')
#             assert response.status_code == 302

#     def test_index_home_success(self):

#         with self.app.test_client() as test_client:
#             response = test_client.get('/home/')
#             assert response.status_code == 200
#             assert "путь до шаблона" in response.data.decode()
