import requests
import time
import csv
from numba import jit


def main():
    token = '*************************'

    params = {
        'access_token': token,
        'v': 5.131,
        'group_id': 'bmstu1830',
        'offset': 0
    }
    get_user_ids = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()
    counter = get_user_ids['response']

    people_counter = 1

    all_members = counter['count']
    text_file = open('names.csv', 'w')
    text_file.close()
    text_file = open('friends.csv', 'w')
    text_file.close()
    while all_members > 0 and params['offset'] < 7074000:
        time.sleep(1)
        get_user_ids = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()
        print(get_user_ids)
        print(params['offset'])
        m = get_user_ids['response']['items']
        s = ''
        for i in m:
            s += str(i)
            if i != m[-1]:
                s += ','

        get_user_info = requests.get('https://api.vk.com/method/users.get',
                                     params={'access_token': token, 'v': 5.131,
                                             'user_ids': s,
                                             'fields': 'first_name,last_name,country, sex, bdate, city',
                                             'lang': 'ru', }).json()

        for i in get_user_info['response']:
            if 'country' in i:
                country = i['country']['title']
            else:
                country = 'None'
            if 'city' in i:
                city = i['city']['title']
            else:
                city = 'None'
            with open('names.csv', 'a', encoding='utf-8', newline='') as text_file:
                writer = csv.writer(text_file)
                writer.writerow(
                    [people_counter, i['id'], i['first_name'], i['last_name'], country, city,
                     i['sex'], i.get('bdate', 'None')])

            get_user_friends = requests.get('https://api.vk.com/method/friends.get',
                                            params={'access_token': token, 'v': 5.131,
                                                    'user_id': i['id']}).json()

            if 'response' in get_user_friends and get_user_friends['response']['count'] > 0:
                friends = get_user_friends['response']['items']
            else:
                friends = '[]'
            with open('friends.csv', 'a', encoding='utf-8', newline='') as text_file:
                writer = csv.writer(text_file)
                writer.writerow([i['id'], friends])
            people_counter += 1
            all_members -= 1

        params['offset'] += len(get_user_ids['response']['items'])


main()
