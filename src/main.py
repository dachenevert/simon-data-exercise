#!/usr/bin/env python3
from os import environ as os_environ
from sys import exit as sys_exit

from argparse import ArgumentParser

from etsy_client import EtsyClient
from secret_sauce import SecretSauce

"""
Usage:
    $ export ETSY_API_KEY='hunter2hunterhunter2'
    $ which python3
        /usr/local/bin/python3
    $ which env
        /usr/bin/env
    $ ./main.py
        DakotaIrish: 'for fans', 'role dungeons', 'fans critical', 'critical role', 'dungeons dragons'
        ...
        nerdylittlestitcher: 'cross', 'download representative', 'stitch', 'cross stitch', 'stitch pattern'

Design:
    the head of the code is all in 'main.py'. It depends on these classes

        EtsyClient: gets data from Etsy

        SecretSauce: heuristic logic aka 'secret sauce'. everything from 'raw data' to 'dictionary of answers'

There are additional comments in the class files

"""
def main():
    args = get_arguments()
    etsy_client = EtsyClient(args.api_key)
    secret_sauce = SecretSauce()

    items_by_shop = {}
    for shop in get_shops():
        etsy_api_path = f'/shops/{shop}/listings/active'
        items_by_shop[shop] = etsy_client.get_results(etsy_api_path)

    meaningful_terms = secret_sauce.get_most_meaningful_terms(items_by_shop)
    report_terms(meaningful_terms)

def report_terms(terms):
    for shop_id, terms in terms.items():
        formatted_terms = '\', \''.join(terms)
        print(f'{shop_id}: \'{formatted_terms}\'')

def get_shops():
    # per the spec "2. Spend a few minutes browsing Etsy, and identify a set
    # of 10 different shops on the site."
    #
    # I chose these, based on "had 'nerd' in the name" + "most recent"
    #
    return [
        'DakotaIrish',
        'InspiredByNerd',
        'MyNerdNursery',
        'NerdTrove',
        'Nerdlystuff',
        'NerdyThingsArt',
        'OddNerdVintage',
        'RobinsNerdSupplies',
        'TheNaturalNerd',
        'nerdylittlestitcher'
    ]


def get_arguments():
    parser = ArgumentParser(description='view itews in Etsy shops.')
    parser.add_argument(
        '--api_key',
        help='Etsy API Key',
        default=os_environ.get('ETSY_API_KEY')
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
