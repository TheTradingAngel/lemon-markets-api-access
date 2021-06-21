import json
import requests
from typing import *
from lemon_markets.models import *
from lemon_markets.account import Account
from lemon_markets.config import DEFAULT_PAPER_REST_API_URL


class Client:

    def __init__(self, account: Account, endpoint: str = None):
        self._account = account
        self._endpoint = endpoint or DEFAULT_PAPER_REST_API_URL

    def list_instruments(self, query: str = None, type_: InstrumentType = None) -> List[Instrument]:
        params = {}
        if query is not None:
            params['query'] = query
        if type_ is not None:
            params['type'] = type_.value

        data_rows = self._request_paged('instruments/', params=params)
        return [Instrument.from_response(data) for data in data_rows]

    def get_instrument(self, isin: str) -> Instrument:
        data = self._request('instruments/'+isin+'/')
        return Instrument.from_response(data)

    def _request_paged(self, endpoint, params=None) -> List[dict]:
        if params is None:
            params = {}

        # Keep requesting until there are no more pages
        offset = None
        count = None
        results = []
        while True:
            page_params = params.copy()
            if offset is not None:
                page_params['offset'] = offset
            data = self._request(endpoint, params=page_params)

            if count is None:
                count = data['count']

            results += data['results']

            if data['next'] is None or len(results) >= count:
                break

        return results

    def _request(self, endpoint, method='GET', data=None, params=None):
        method = method.lower()
        url = self._endpoint+endpoint
        headers = self._account.authorization

        if method == 'get':
            response = requests.get(url=url, params=params, headers=headers)
        elif method == 'post':
            response = requests.post(url=url, data=data, headers=headers)
        elif method == 'patch':
            response = requests.patch(url=url, data=data, params=params, headers=headers)
        elif method == 'delete':
            response = requests.delete(url=url, params=params, headers=headers)
        else:
            raise ValueError('Unknown method: %r' % method)

        response.raise_for_status()

        data = json.loads(response.content)
        return data
