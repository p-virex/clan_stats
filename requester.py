from pprint import pprint
import os
import requests
import pickle

from collections import OrderedDict

from constants import URL, CLAN_INFO, APPLICATION_ID, VEHICLE_INFO, VEHICLE


def start_vehicle_collect(clan_id):
    vehicle_collector = dict()
    json_vehicle_info = get_vehicle_info()
    request_clan_info = get_request(CLAN_INFO, {'application_id': APPLICATION_ID, 'clan_id': clan_id})
    members_info = request_clan_info['data']['1']['members']
    for member in members_info:
        account_id = member['account_id']
        request_member_info = get_request(VEHICLE_INFO, {'application_id': APPLICATION_ID, 'account_id': account_id})
        for vehicle_info in request_member_info['data'][str(account_id)]:
            vehicle_id = str(vehicle_info['tank_id'])
            if json_vehicle_info['data'].get(vehicle_id):
                name_vehicle = json_vehicle_info['data'][vehicle_id]['name']
                level = json_vehicle_info['data'][vehicle_id]['tier']
                nation = json_vehicle_info['data'][vehicle_id]['nation']
                type_v = json_vehicle_info['data'][vehicle_id]['type']
            else:
                name_vehicle, level, nation, type_v = vehicle_id, 0, 'not_known', 'not_known'
            wins, battles = vehicle_info['statistics']['wins'], vehicle_info['statistics']['battles']
            if vehicle_collector.get(name_vehicle):
                wins_v = vehicle_collector[name_vehicle]['wins'] + wins
                battles_v = vehicle_collector[name_vehicle]['battles'] + battles
                vehicle_collector[name_vehicle].update({'wins': wins_v, 'battles': battles_v})
            else:
                vehicle_collector.setdefault(name_vehicle, {}).update({'wins': wins,
                                                                       'battles': battles,
                                                                       'level': level,
                                                                       'nation': nation,
                                                                       'type': type_v})
            if json_vehicle_info.get(vehicle_id):
                vehicle_collector[name_vehicle].update(
                    {'level': json_vehicle_info[vehicle_id]['tier'], 'nation': json_vehicle_info[vehicle_id]['nation']})

    for veh_name, veh_info in vehicle_collector.items():
        vehicle_collector[veh_name].update({'p_win': round((veh_info['wins'] / veh_info['battles']) * 100, 3)})
    create_dump(vehicle_collector, 'picle')
    return vehicle_collector


def get_vehicle_info():
    if os.path.isfile('vehicle_info_picle'):
        vehicle_name_json = load_dump('vehicle_info_picle')
    else:
        vehicle_name_json = get_request(VEHICLE, {'fields': 'name, tier, nation, type', 'application_id': APPLICATION_ID})
        create_dump(vehicle_name_json, 'vehicle_info_picle')
        # {'data': {'9985': {'name': 'СУ-101', 'nation': 'ussr', 'tier': 8}}
    return vehicle_name_json


def get_request(method, params):
    return requests.get(URL + method, params=params).json()


def create_dump(name_object, name_pickle):
    with open(name_pickle, 'wb') as f:
        pickle.dump(name_object, f)


def load_dump(name_pickle):
    with open(name_pickle, 'rb') as f:
        return pickle.load(f)


def sorted_dict(dict_, key_sort):
    return OrderedDict(sorted(dict_.items(), key=lambda entry: (entry[1][key_sort], entry[1]['p_win']), reverse=True))


if __name__ == '__main__':
    # start_vehicle_collect(1)
    a = load_dump('picle')
    # pprint(sorted_dict(a, 'level'))
    count = 1
    for k, v in sorted_dict(a, 'battles').items():
        # if v['nation'] == 'germany':
        msg = '{}. {} > battles: {}, nation: {}, percent wins: {}, type: {}'
        print(msg.format(count, k, v['battles'], v['nation'], v['p_win'], v['type']))
        count += 1
