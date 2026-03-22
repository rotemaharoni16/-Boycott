import requests

res = requests.post("http://127.0.0.1:5000/register", json={
    "username": "dan",
    "interests": ["music", "games"]
})

print(res.json())