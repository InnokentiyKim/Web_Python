import requests

# response = requests.post(" http://127.0.0.1:8080/api/v1/user",
#                          json={"name": "user_1", "password": "1234"}
#                          )
#
# print(response.status_code)
# print(response.json())
#
# response = requests.get(" http://127.0.0.1:8080/api/v1/user/1")
#
# print(response.status_code)
# print(response.json())
#
#
# response = requests.post(" http://127.0.0.1:8080/api/v1/advertisement",
#                          json={"title": "advertisement_1", "description": "My first advertisement",
#                                "price": 50.8, "author": 1}
#                          )
#
# print(response.status_code)
# print(response.json())

# response = requests.get(" http://127.0.0.1:8080/api/v1/advertisement/1")
#
# print(response.status_code)
# print(response.json())
#
# response = requests.patch(" http://127.0.0.1:8080/api/v1/advertisement/1",
#                          json={"description": "My first advertisement changed",
#                                "price": 100.3}
#                          )
#
# print(response.status_code)
# print(response.json())

response = requests.get(" http://127.0.0.1:8080/api/v1/advertisement",
                        params={
                            "price": 10.3,
                        })

print(response.status_code)
print(response.json())
