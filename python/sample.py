from enum import Enum
from typing import Optional

import requests


# Sample client class built to make requests to the LTIaaS API
class LTIaaSClient:
    # Header templates
    LTIK_AUTHORIZATION_HEADER = 'LTIK-AUTH-V1 Token={ltik}, Additional=Bearer {api_key}'
    BEARER_AUTHORIZATION_HEADER = 'Bearer {api_key}'

    # LTIaaS Endpoint templates
    ID_TOKEN_ENDPOINT = '{base_url}/api/idtoken'
    MEMBERSHIPS_ENDPOINT = '{base_url}/api/memberships'

    # Request types
    class RequestMethod(Enum):
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'

    # Initializes the class and set the API Key
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key
        # Formatted endpoint URLs
        self.id_token_url = self.ID_TOKEN_ENDPOINT.format(base_url=base_url)
        self.memberships_url = self.MEMBERSHIPS_ENDPOINT.format(base_url=base_url)

    # Builds authorization header for requests that require the LTIk token
    def __build_ltik_authorization_header(self, ltik: str):
        return self.LTIK_AUTHORIZATION_HEADER.format(ltik=ltik, api_key=self.api_key)

    # Builds authorization header for requests that only require the API Key
    def __build_bearer_authorization_header(self):
        return self.BEARER_AUTHORIZATION_HEADER.format(api_key=self.api_key)

    # Helper method to make LTIaaS requests
    def make_request(self, method: RequestMethod, url: str, ltik: Optional[str] = None):
        # Decide which authorization header to use depending on whether or not the lti token was passed
        authorization_header = (self.__build_ltik_authorization_header(ltik)
                                if ltik else self.__build_bearer_authorization_header())
        response = requests.request(method=method.value, url=url, headers={'Authorization': authorization_header})
        return response.json()

    # Retrieve ID Token
    def get_id_token(self, ltik: str):
        return self.make_request(url=self.id_token_url, method=self.RequestMethod.GET, ltik=ltik)

    # Retrieve context memberships
    def get_memberships(self, ltik: str):
        return self.make_request(url=self.memberships_url, method=self.RequestMethod.GET, ltik=ltik)


# Everytime a new LTI launch takes place, LTIaaS will redirect the user to your application passing along a
# query parameters called "ltik". You can then retrieve this parameter and use it to call the client methods:
"""
ltiaas_client = LTIaaSClient(base_url='https://your.ltiaas.com', api_key='your_api_key')

# Inside a request handler
ltik = request.GET.get('ltik') # Retrieve ltik from query parameters
id_token = ltiaas_client.get_id_token(ltik=ltik) # Retrieve ID Token containing user, platform and launch information
"""
