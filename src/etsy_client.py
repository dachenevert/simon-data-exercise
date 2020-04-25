from sys import exit as sys_exit
from requests import get as requests_get

"""
    EtsyClient's concerns are "anything about the Etsy API", including
        pagination
        location of the Etsy API host
        path root of the Etsy API tree

    Its inputs are
        an Etsy API_KEY
        an API path

    Its outputs are
        all response values for a given API path e.g.  '/shops/'

    Limits and restrictions
        It only supports "GET" requests
        Error processing and reporting is naive and rudimentary
        It makes no attempt to recover from e.g. timeout failure or
            server-side throttling
        Performance is stone-age, nothing is done in parallel or batched
"""

class EtsyClient():
    def __init__(self, etsy_api_key):
        if etsy_api_key is None:
            print('ERROR: etsy_api_key not found')
            sys_exit(1)

        # shops with 1000 listings were taking 10s of seconds, so I capped
        # the max number of responses
        self.MAX_RESPONSES = 50
        self.params = {
            'api_key': etsy_api_key
        }
        pass

    def get_results(self, path):
        if not path.startswith('/'):
            raise Exception(f'malformed path "{path}"')
        url = f'https://openapi.etsy.com/v2{path}'
        all_results = []

        next_offset = 0
        while True:
            try:
                self.params['offset'] = next_offset
                resp = requests_get(url, params=self.params)
                if not resp.ok:
                    print(f'ERROR: request failed, path = {path}')
                    sys_exit(0)
            except Exception as ex:
                print(f'ERROR: exception type={type(ex)}, ex=>{ex}< in get_items()')
                sys_exit(0)

            resp_json = resp.json()
            pagination = resp_json['pagination']
            next_offset = pagination['next_offset']
            results_this_page = resp_json['results']
            all_results += results_this_page
            if len(all_results) >= self.MAX_RESPONSES:
                return all_results[0:self.MAX_RESPONSES]
            if next_offset is None:
                return all_results
