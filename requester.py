from pprint import pprint
import requests
import pickle

from collections import OrderedDict

from constants import URL, CLAN_INFO, APPLICATION_ID, VEHICLE_INFO, VEHICLE


def start_collect():
    vehicle_collector = dict()

    vehicle_name_json = requests.get(URL + VEHICLE, params={'application_id': APPLICATION_ID, 'fields': 'name'}).json()
    # {'data': {'1': {'name': 'Т-34'}}

    request_clan_info = requests.get(URL + CLAN_INFO, params={'application_id': APPLICATION_ID, 'clan_id': 1}).json()
    members_info = request_clan_info['data']['1']['members']

    for member in members_info:
        account_id = member['account_id']
        request_member_info = requests.get(URL + VEHICLE_INFO,
                                           params={'application_id': APPLICATION_ID, 'account_id': account_id}).json()
        for vehicle_info in request_member_info['data'][str(account_id)]:
            veh_id = vehicle_info['tank_id']
            if vehicle_name_json['data'].get(str(veh_id)):
                name_vehicle = vehicle_name_json['data'][str(veh_id)]['name']
            else:
                name_vehicle = veh_id
            wins, battles = vehicle_info['statistics']['wins'], vehicle_info['statistics']['battles']
            if vehicle_collector.get(name_vehicle):
                wins_v = vehicle_collector[name_vehicle]['wins'] + wins
                battles_v = vehicle_collector[name_vehicle]['battles'] + battles
                vehicle_collector[name_vehicle].update({'wins': wins_v, 'battles': battles_v})
            else:
                vehicle_collector.setdefault(name_vehicle, {}).update({'wins': wins, 'battles': battles})

    for veh_name, veh_info in vehicle_collector.items():
        vehicle_collector[veh_name].update({'p_win': round((veh_info['wins'] / veh_info['battles']) * 100, 3)})
    return vehicle_collector


def create_dump(vehicle_collector):
    with open('picle', 'wb') as f:
        pickle.dump(vehicle_collector, f)


def load_dump():
    with open('picle', 'rb') as f:
        return pickle.load(f)


def sorted_dict(dict_):
    return OrderedDict(sorted(dict_.items(), key=lambda entry: (entry[1]['p_win'], entry[1]['battles']), reverse=True))


if __name__ == '__main__':
    a = load_dump()
    b = load_dump()
    for name, info in b.items():
        if info['battles'] < 100:
            a.pop(name)
    pprint(sorted_dict(a))
