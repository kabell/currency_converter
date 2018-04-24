
# Currency Converter

Converter between various currencies such as USD, EUR, GBP and much more. Supports both API and CLI interface.

## Requirements

 - Python 3.5

- cachetools==2.0.1
- Flask==0.12.2
- Flask-Jsonpify==1.5.0
- Flask-RESTful==0.3.6
- forex-python==0.3.3

## Deployment

When the python environment is prepared start the currency converter server
```
python server.py
```
By default the server port is __8080__ but you can change it in `server.py` to whatever you want. While the server is running both API and CLI is working.

## API
API is available by HTTP protocol on the specified port in `server.py`.

```
GET /currency_converter?amount=0.9&input_currency=GBP&output_currency=EUR HTTP/1.1
```

## CLI
CLI interface is provided by `currency_converter.py`. The script comunicates with the API, so running server is needed. Be sure that the port specified in `currency_converter.py` is the same as the `server.py`.

```
./currency_converter.py --amount 0.9 --input_currency GBP --output_currency EUR
```

## Output
Json output of both API and API is the same.
```
{
  "input": {
    "amount": 0.9,
    "currency": "GBP"
  },
  "output": {
    "EUR": 1.02897
  }
}

```

## Features
- you can use currency symbols ($, €, £, ... ) instead of currency codes
- if the output currency is not specified, the amount is converted to all available currencies
- if the requested currency code/symbol is not available, the error message is returned instead of standard json output
- uses http://fixer.io/ currency rates API by  `forex-python` package
- included caching for the exchange rates API calls - changable in server.py (CACHE_SIZE, CACHE_TIMEOUT)
