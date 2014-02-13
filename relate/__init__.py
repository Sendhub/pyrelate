"""
Python client for relate IQ

VERY EXPERIMENTAL
"""

import requests

class RelateAPI:
    API_PROTO = 'https'
    API_PORT = '443'
    API_HOST = 'api.relateiq.com'
    API_VERSION = 'v1'

    HTTP_POST = 'post'
    HTTP_GET = 'get'

    def __init__(self, api_token, list_id=None):
        self.API_TOKEN = api_token
        self.LIST_ID = list_id

    def _build_request_path(self, endpoint):
        path = "%s://%s/api/v%s/%s" % (
            self.API_PROTO,
            self.API_HOST,
            self.API_VERSION,
            endpoint)
        return path

    def add_relationship(self, data, list_id=None):
        """Add a relationship to the given list
        data format:
        {
            'firstName': "Matt",
            'email': "matt@sendwithus.com",
            'phone': '123-456-7890',
            'Status': 'New',
            'source': 'Landing'
        }

        expected response:
        {
            result: ["Created a contact", "Added a member"]
            success: true
        }
        """

        if not data:
            data = {}

        if not 'firstName' in data:
            raise Exception('firstName is a required parameter')

        if not 'email' in data:
            raise Exception('Email must be set')

        return self._api_request(self.HTTP_POST, 'addrelationship',
                list_id=list_id, data=data)

    def _api_request(self, http_method, endpoint, list_id=None, data=None):
        """Private method for api requests"""

        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

        if not list_id:
            list_id = self.LIST_ID

            if not list_id:
                raise Exception('List id must be set')

        path = self._build_request_path('entitylists')

        path = '%s/%s/%s' % (path, list_id, endpoint)

        if (http_method == self.HTTP_POST):
            r = requests.post(path, data=data, headers=headers,
                auth=('apitoken', self.API_TOKEN))

