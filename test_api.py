from requests import get, post, delete


print(post('http://127.0.0.1:5000/api/chats', json={'name': 'pupu', 'users_id': '1 2', 'is_private': True}))
p = post('http://127.0.0.1:5000/api/chats/messages/1', json={'content': 'skibidi', 'sender_id': 1,
                                                             'picture': None, 'coordinates': None})
print(p.status_code, p.json())
p = post('http://127.0.0.1:5000/api/chats/messages/1', json={'content': 'skibidi2', 'sender_id': 1})
print(p.status_code, p.json())
print(get('http://127.0.0.1:5000/api/chats/messages/1').json())
print(delete('http://127.0.0.1:5000/api/messages/1').json())

# print(post('http://127.0.0.1:5000/api/chats', json={'name': 'pupu1', 'users_id': '1 2', 'is_private': True}))
# print(post('http://127.0.0.1:5000/api/chats', json={'name': 'pupupu', 'users_id': '1 2', 'is_private': False}))
# print(post('http://127.0.0.1:5000/api/chats', json={'name': 'pupupu1', 'users_id': '1 2', 'is_private': False}))
print(get('http://127.0.0.1:5000/api/chats').json())
print(post('http://127.0.0.1:5000/api/users', json={'username': 'lol', 'password': '123456'}).json())
print(get('http://127.0.0.1:5000/api/users/1').json())
print(delete('http://127.0.0.1:5000/api/users/1').json())
