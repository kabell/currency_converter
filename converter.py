from forex_python.converter import CurrencyRates, RatesNotAvailableError
from cachetools import TTLCache

class Converter(CurrencyRates):

    
    def __init__(self, ttl=20.0, maxsize=256):
        super().__init__()
        self.cache = TTLCache(ttl=ttl, maxsize=maxsize)
   
    
    def get_cached_rates(self, input_currency):
        
        """
        Method for caching exchange rates from forex library
        It returns all possible exchange rates for the given currency
        """

        if self.cache.get(input_currency) is not None:
            return self.cache.get(input_currency)

        try:
            ret =  self.get_rates(input_currency)
            ret[input_currency] = 1.0
        except RatesNotAvailableError as e:
            ret = {}

        self.cache[input_currency] =  ret
        return ret


    def convert(self, amount, input_currency, output_currency):

        """ 
        Method for converting amount of input currency to output currency.
        If the output currency is None then it will output the amount in all possible currencies
        """
        
        rates = self.get_cached_rates(input_currency)
        if output_currency is not None:
            rates = {output_currency:rates[output_currency]}

        rates = {r:rates[r]*amount for r in rates}
        return rates

