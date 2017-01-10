from client import *
from datetime import datetime


class ClientFriends(Client):
    today = datetime.toordinal(datetime.now())
    age_friends = {}

    def __init__(self, user_id):
        self.user_id = user_id
        self.payload = {'v': '5.57', 'fields': 'bdate', 'order': 'random', 'user_id': self.user_id}

    def get_friends(self):
        resp = self._get_data('friends.get', self.payload)

        resp_items = resp['response']['items']

        for item in resp_items:
            if 'bdate' in item:
                if len(item['bdate']) >= 8:
                    bdate = datetime.strptime(item['bdate'], '%d.%m.%Y')
                    bdate = datetime.toordinal(bdate)
                    age = int((self.today - bdate)//365.25)

                    self.age_friends[age] = '#' if self.age_friends.get(age) is None else self.age_friends[age] + '#'

                    # if self.age_friends.get(age) is None:
                    #     self.age_friends[age] = '#'
                    # else:
                    #     self.age_friends[age] += '#'
        return self.age_friends

    def print_friends(self):
        ages = self.get_friends()
        
        for i in range(max(ages.keys())+1):
            if ages.get(i) is None:
                continue
            else:
                print(i, ': ', ages.get(i))
