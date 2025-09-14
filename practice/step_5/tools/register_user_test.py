import requests

password="oYhOIblF7OyFVfRCslqiI+Cxs5x/B4+6Ti+ROSo3xPGVYuz+YxqajsshWD8cNP3Zl0alnlbaJoTnl6g5h5BQlMw/3JbvKbdYEJKIDEFrimPG9RvUuXuvD1fQeAqMLrF9MeO6syoxFn71ryplhZtWl7t/Uhe28W7EIfA0uvGrCI4zeUc52EYbWjwpnPHqrHDHD+EWs2ZZVP26kqYVXl9OD4yszO1OoFxSm1ZuEl1su0oumN0jzSpmUWyrvhy4iGxctnrhQeAH4Hb4NrV0pN8tenVK8N5e6dKAzI0KxNzilEUQVbCzCZbUxGABZT3acfjusvrrm8MNlYHYWodpyaP2xQ=="

url = "http://127.0.0.1:8000/api/user/v1/register"

body = {
    "header": {},
    "body": {
        "certificate_id": 1,
        "email": "charsyam@gmail.com",
        "password": password
    }
}

response = requests.post(url, json=body)
print(response.json())
