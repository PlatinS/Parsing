# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json
import time

AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
VK_VERSION = '5.103'
URL_GROUPS_GET = 'https://api.vk.com/method/groups.get'
URL_GROUPS_BY_ID_GET = 'https://api.vk.com/method/groups.getById'

def parameters(user_id='', group_ids='', fields=''):
    parameters = {
        'User-Agent': AGENT,
        'access_token': TOKEN,
        'v': VK_VERSION,
        'user_id': 567958902,
        'group_ids': group_ids,
        'fields': fields
    }
    return parameters

def get_groups_info(list_groups):
    groups_list_with_str = []
    for group in list(list_groups):
        groups_list_with_str.append(str(group))
    time.sleep(1)
    groups_info = requests.get(URL_GROUPS_BY_ID_GET, parameters(group_ids=', '.join(groups_list_with_str)))
    groups_info = groups_info.json()

    groups_result_list = []
    for group in groups_info['response']:
        groups_result_list.append(dict(gid=group['id'], name=group['name']))

    return groups_result_list

def write_in_json_file(groups):
    with open('vk_out.json', 'w') as file:
        for group in groups:
            json.dump(group, file, indent=2, ensure_ascii=False)
    file.close()

def main():
    req = requests.get(URL_GROUPS_GET, parameters())

    print('Код состояния ответа: ',req.status_code)
    if req.ok:
        data = req.json()
        groups = data['response']['items']
        groups_info = get_groups_info(groups)

        for group in list(groups_info):
            print(f"Номер: {group['gid']} Имя группы: {group['name']}")

        write_in_json_file(groups_info)


if __name__ == '__main__':
    main()
