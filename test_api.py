from requests import get, post, delete


print(get('http://127.0.0.1:5000/api/users/1').json())
print(post('http://127.0.0.1:5000/api/users', json={'username': 'VASA_NASA', 'password': '123456'}).json())
print(delete('http://127.0.0.1:5000/api/users/1').json())
