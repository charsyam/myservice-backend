from locust import HttpUser, task, between, TaskSet 

 
class UserBehavior(TaskSet): 
    @task 
    def get_public_key(self): 
        self.client.get(f'/api/auth/v1/public-key') 

 
class LocustUser(HttpUser): 
    host = "http://127.0.0.1:8000" 
    tasks = [UserBehavior] 
    wait_time = between(1, 4) 
