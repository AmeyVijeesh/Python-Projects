import requests
import datetime
import socket


date = datetime.datetime.now()


def get_latest_no():
    url = "https://api.covid19api.com/summary"
    data = requests.get(url).json()
    return data


def get_live_data_country(country_code):
    country = country_code
    url = "https://api.covid19api.com/total/country/{}".format(country)
    try:
        data = requests.get(url).json()
        size_list = len(data)
        latest_data = int(size_list) - 1
        data_latest = data[latest_data]
    except:
        return None

    return data_latest


def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


def data_extract(dict):

    data_list = []
    for i, j in dict.items():
        data = {"Final": dict}
    for k, v in data.items():
        data_list.append(v["Confirmed"])
        data_list.append(v["Deaths"])
        data_list.append(v["Recovered"])
        data_list.append(v["Active"])
    return data_list
