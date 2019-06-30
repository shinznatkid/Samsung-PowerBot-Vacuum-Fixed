import requests


CLIENT_ID = 'xxxxxxxxxxxx'
CLIENT_SECRET = 'xxxxxxxxxxx'
REDIRECT_URI = 'https://example.com/some/where/'

def main():
    code = authorization()
    token = get_token(code)
    base_url = get_base_url(token)
    devices = get_devices(token, base_url)
    device_id = devices[0]['id']
    # power_on(device_id)
    # power_off(device_id)


def authorization():
    global CLIENT_ID
    url = 'https://graph.api.smartthings.com/oauth/authorize?response_type=code&client_id={}&scope=app&redirect_uri={}'.format(CLIENT_ID, REDIRECT_URI)
    print('open url below and get code')
    code = input('code: ').strip()
    return code

def get_token(code):
    global CLIENT_SECRET, CLIENT_SECRET, REDIRECT_URI
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post('https://graph.api.smartthings.com/oauth/token', data)
    response_json = response.json()
    return response_json['access_token']


def get_base_url(token):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    response = requests.get('https://graph.api.smartthings.com/api/smartapps/endpoints', headers=headers)
    base_url = response.json()[0]['uri']
    return base_url


def get_devices(token, base_url):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    # get states
    response = requests.get('{}/switches/states'.format(base_url), headers=headers)
    devices = response.json()
    return devices


def power_on(token, base_url, device_id):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    # set Switch on
    data = {
        'command': 'on',
    }
    response = requests.put('{}/switches/{}'.format(base_url, device_id), json=data, headers=headers)


def power_off(token, base_url, device_id):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    # set Switch on
    data = {
        'command': 'off',
    }
    response = requests.put('{}/switches/{}'.format(base_url, device_id), json=data, headers=headers)


main()
