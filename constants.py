"""
Все запросы в URI-формате имеют следующий вид:

http(s)://<server>/<API_name>/<method block>/<method name>/?<get params>Где:

<server> — URI игрового сервера на соответствующем кластере
<API_name> — версия API
<method block> — название группы методов
<method name> — название метода
<get params> — параметры метода GET для запроса
"""
URL = 'https://api.worldoftanks.ru/wot/'
APPLICATION_ID = 'ae66c7931b72dfb5b148eb8960f83b28'
CLAN_INFO = 'clans/info/'
VEHICLE_INFO = 'account/tanks/'
VEHICLE = 'encyclopedia/vehicles/'
# https://api.worldoftanks.ru/wot/encyclopedia/vehicles/?application_id=ae66c7931b72dfb5b148eb8960f83b28&fields=name
