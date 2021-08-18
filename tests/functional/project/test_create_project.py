from tests.functional.base import BaseTestCase


class ProjectCreateTestCase(BaseTestCase):

    def test_create_project_check_auth_fail(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/projects/')
            assert response.status_code == 401

    '''
    def test_create_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/projects/', data={
                'title': 'test project title',
                'description': 'test project description',
                'website': 'testproject.com',
            })

            assert response.status_code == 200
    '''
