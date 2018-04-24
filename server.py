from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jsonpify import jsonify
from converter import Converter
import json
import os

app = Flask(__name__)
api = Api(app)

CACHE_TIMEOUT = 20.0
CACHE_SIZE = 512
APP_PORT = 8080

converter = Converter(ttl = CACHE_TIMEOUT, maxsize = CACHE_SIZE)

class CurrencyConverter(Resource):

    def __init__(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/data/currencies.json') as f:

            #load all currencies from json
            self._data = json.loads(f.read())
            self.currencies = { d['cc'] for d in self._data}
            self.symbols = {d['symbol']:d['cc'] for d in self._data}

            #make single-valued world symbols
            self.symbols['£'] = 'GBP'
            self.symbols['$'] = 'USD'
            self.symbols['¥'] = 'CNY'


    def code_from_symbol(self, symbol):
        """
        If the symbol is one of the supported currencies symbols then this
        method converts it into the currency code
        """

        if symbol is None:
            return None
        if symbol in self.currencies:
            return symbol

        #if the symbol is neither a currency code nor symbol raise an exception
        if symbol not in self.symbols:
            raise Exception("Currency not supported !")

        return self.symbols[symbol]


    def parse_url_args(self):

        """
        Parse arguments from url
        """

        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float, required=True)
        parser.add_argument('input_currency', type=str, required=True)
        parser.add_argument('output_currency', type=str)
        return parser.parse_args()

    def get(self):

        """
        Takes input values as get parameters and outputs json with converted currency
        If there is no exchange rate available it will return error message.
        """

        try:
            kwargs = self.parse_url_args()
            kwargs['input_currency'] = self.code_from_symbol(kwargs['input_currency'])
            kwargs['output_currency'] = self.code_from_symbol(kwargs['output_currency'])

            ret = {
                "input":{
                    "amount":kwargs.get('amount'),
                    "currency":kwargs.get('input_currency'),
                },
            }
            ret["output"] = converter.convert(**kwargs)

        except Exception as e:
            ret = "No exchange rates found for the given currencies or currency not supported !"

        return jsonify(ret)

api.add_resource(CurrencyConverter, '/currency_converter')

if __name__ == '__main__':
     app.run(port=APP_PORT)
