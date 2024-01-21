import json
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
import firebase_creds_render
from firebase_admin import db

ref = db.reference("/")

def fetch_json(url, num):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
        if script_tag:
            script_content = script_tag.contents[0]
        push_json(script_content, num)

def convert_utc_to_ist(utc_datetime_str):
    utc_datetime = datetime.strptime(utc_datetime_str, "%Y-%m-%dT%H:%M:%S%z")

    utc_timezone = pytz.timezone('UTC')

    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_datetime = utc_datetime.astimezone(ist_timezone)

    ist_datetime_str = ist_datetime.strftime("%Y-%m-%dT%H:%M:%S%z")

    return ist_datetime_str

def push_json(script_content, num):
    data = json.loads(script_content)
    enc_data = {}
    socials = ['linkedin', 'twitter', 'facebook', 'instagram', 'medium', 'telegram', 'slack', 'discord']
    times = ['reg_starts_at', 'reg_ends_at', 'starts_at', 'ends_at']
    enc_data['name'] = data['props']['pageProps']['hackathon']['name']
    try:
        enc_data['location'] = data['props']['pageProps']['hackathon']['city'] + ', ' + data['props']['pageProps']['hackathon']['country']
    except TypeError:
        pass
    enc_data['reg_starts_at'] = convert_utc_to_ist(data['props']['pageProps']['hackathon']['settings']['reg_starts_at'])
    enc_data['reg_ends_at'] = convert_utc_to_ist(data['props']['pageProps']['hackathon']['settings']['reg_ends_at'])
    enc_data['starts_at'] = convert_utc_to_ist(data['props']['pageProps']['hackathon']['starts_at'])
    enc_data['ends_at'] = convert_utc_to_ist(data['props']['pageProps']['hackathon']['ends_at'])
    enc_data['is_online'] = data['props']['pageProps']['hackathon']['is_online']
    enc_data['tracks'] = data['props']['pageProps']['hackathon']['tracks']
    enc_data['email'] = data['props']['pageProps']['hackathon']['settings']['contact_email']
    enc_data['site'] = data['props']['pageProps']['hackathon']['settings']['site']
    enc_data['socials'] = {}
    for i in socials:
        if data['props']['pageProps']['hackathon']['settings'][i] != None:
            enc_data['socials'][i] = data['props']['pageProps']['hackathon']['settings'][i]
    enc_data['is_hybrid'] = data['props']['pageProps']['hackathon']['settings']['is_hybrid']
    enc_data['team_size'] = str(data['props']['pageProps']['hackathon']['team_min']) + '-' + str(data['props']['pageProps']['hackathon']['team_max'])
    prizes = []
    for i in data['props']['pageProps']['hackathon']['prizes']:
        arr_i = []
        arr_i.append(i['name'])
        if i['amount'] == 0:
            arr_i.append(i['desc'])
        else:
            arr_i.append('$' + str(i['amount']))

        arr_i.append(i['quantity'])
        try:
            arr_i.append(i['sponsors'][0]['sponsor']['name'])
        except IndexError:
            pass
        prizes.append(arr_i)
    enc_data['prizes'] = prizes

    ref = db.reference(f"/{num}")
    ref.set(enc_data)
