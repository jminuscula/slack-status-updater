
import json
import requests
import urllib.parse

from slackclient import SlackClient


SLACK_OAUTH_ACCESS_URL = 'https://slack.com/api/oauth.access'
SLACK_OAUTH_AUTHORIZE_URL = 'https://slack.com/oauth/authorize'
SLACK_OAUTH_SCOPES = (
    'users.profile:read',
    'users.profile:write',
)


class SlackStatusClient:
    """
    Wraps the slackclient library to provide a high level interface to the API.
    """

    def __init__(self, slack_token):
        self.client = SlackClient(slack_token)

    def get_status(self):
        return self.client.api_call(
            'users.profile.get',
        )

    def set_status(self, text=None, emoji=None, expiration=None):
        status_expiration = 0
        if expiration:
            status_expiration = expiration.timestmap()

        return self.client.api_call(
            'users.profile.set',
            profile=json.dumps({
                'status_text': text or '',
                'status_emoji': emoji or '',
                'status_expiration': status_expiration,
            })
        )

    def clear_status(self):
        return self.set_status()


def get_oauth_token(slack_config):
    params = {
        'client_id': slack_config['client_id'],
        'scope': ','.join(SCOPES),
        'redirect_uri': 'https://www.httpbin.org/get',
    }

    query = urllib.parse.urlencode(params)
    print('Please authorize the app via this url')
    print(f'> {SLACK_OAUTH_AUTHORIZE_URL}?{query}')

    print('\nPlease enter the provided code')
    code = input('Code: ')

    params.update({'client_secret': slack_config['client_secret'], 'code': code})
    oauth_req = requests.get(SLACK_OAUTH_ACCESS_URL, params=params)
    oauth_data = oauth_req.json()

    return oauth_data.get('access_token')
