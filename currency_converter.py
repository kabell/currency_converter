#!/usr/bin/env python3
from urllib.parse import urlparse, urlunparse, urlencode
import argparse
import requests

APP_PORT = 8080

def parse_cli_args():
    
    """
    Parse cli arguments and return them as a dictionary
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", type=float, help="amount of currency to convert", required=True)
    parser.add_argument("--input_currency", help="input currency", required=True)
    parser.add_argument("--output_currency", help="output currency")
    args = parser.parse_args()
    values = vars(args)
    values = {v:values[v] for v in values if values[v] is not None}
    return values


if __name__ == '__main__':
    query = urlencode(parse_cli_args())
    r = requests.get('http://127.0.0.1:'+str(APP_PORT)+'/currency_converter?'+query)
    print(r.text)
