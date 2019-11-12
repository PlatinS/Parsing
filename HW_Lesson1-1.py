# 1. Посмотреть документацию к API GitHub, разобраться как вывести список
# репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json

import requests
import json

headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

link = "https://api.github.com/users/PlatinS/repos"
username = 'PlatinS'

req = requests.get(f'{link}', headers = headers)
#data = json.loads(req.text)
print('Код состояния ответа: ',req.status_code)

if req.ok:
    data = req.json()
    print('Репозитории пользователя PlatinS:')
    for i in range(len(data)):
        print("Имя: ", data[i]['name'],"\t URL: ", data[i]['url'])

file = open('out.json', 'w')
file.write(str(data))
file.close()
