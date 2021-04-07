from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(0,0)

    @task
    def redirect(self):
        self.client.get('/v1/shortener/r/aaaas6933b/', headers={'Authorization': 'Token 8b5d198dd50268ab6284e5c5d02cab6236aa75f7'})
