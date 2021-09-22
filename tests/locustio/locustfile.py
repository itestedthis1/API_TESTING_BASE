import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task(1)
    def hello_world(self):
        self.client.get("?token=jessica")

    @task(2)
    def view_jobs(self):
        for item_id in range(10): 
            self.client.get("jobs/?token=jessica", headers={'x-token' : 'fake-super-secret-token'})
            time.sleep(1)

    def on_start(self):
        self.client.get("?token=jessica")