# import http.client
# import json
# from .models import Province,City

# def provinceChoiceField():
#     conn = http.client.HTTPSConnection("api.rajaongkir.com")

#     headers = {'key': "3921e2bb12875d82fe604ae0b153d62b" }

#     conn.request("GET", "/starter/province", headers=headers)

#     res = conn.getresponse()
#     data = res.read()

#     result = json.loads(data.decode('utf-8')) #Change the data type from byte to string to dictionary

#     # print(result)
#     # print(result['rajaongkir']['results'])
#     province_before = result['rajaongkir']['results']
#     province = []

#     #ADD PROVINCE TO DATABASE
#     for i in province_before:
#         print(i)
#         p = Province.objects.create(name=i['province'], identifier=i['province_id'])
#         p.save()

#     for i in province_before:
#         # province.append(i['province'])
#         tuple_value = i['province']
#         province.append(tuple([tuple_value,tuple_value]))

#     return province

# def checkCity():
#     conn = http.client.HTTPSConnection("api.rajaongkir.com")

#     headers = { 'key': "3921e2bb12875d82fe604ae0b153d62b" }

#     conn.request("GET", "/starter/city", headers=headers)

#     res = conn.getresponse()
#     data = res.read()

#     result = json.loads(data.decode('utf-8')) #Change the data type from byte to string to dictionary

#     # print(type(result))
#     print(result)
#     city_before = result['rajaongkir']['results']
#     print(city_before) # {'city_id': '464', 'province_id': '34', 'province': 'Sumatera Utara', 'type': 'Kabupaten', 'city_name': 'Tapanuli Tengah', 'postal_code': '22611'}

#     # ADD THE CITY
#     for i in city_before:
#         c = City.objects.create(name=i['city_name']+" ("+i['type']+")",province=Province.objects.get(name=i['province']), identifier=i['city_id'])
#         c.save()



