import requests

response = requests.post(" http://127.0.0.1:8000/api/v1/hello/world/30",
                         params={"some_key": "value"},
                         json={"name": "Athena", "age": 22}
                         )

print(response.status_code)
print(response.json())