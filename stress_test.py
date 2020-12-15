from locust import HttpUser, between, task

class MyWebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    @task
    def load_main(self):
        self.client.post("/", {"sentence": "test sentence", "form_type":"analysis_sentence", "topN":"3"})