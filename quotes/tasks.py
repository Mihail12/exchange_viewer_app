import requests
from django.conf import settings

from exchange_viewer_app.celery import app
from quotes.models import Currency, ExchangeRate


@app.task(ignore_result=False)
def alphavantage_synchronizer():
    api_key = settings.ALPHA_VANTAGE_API_KEY
    url = (
        f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&'
        f'from_currency=BTC&to_currency=USD&apikey={api_key}'
    )
    r = requests.get(url).json()
    data = r['Realtime Currency Exchange Rate']
    from_currency, _ = Currency.objects.get_or_create(
        name=data['2. From_Currency Name'],
        code=data['1. From_Currency Code'],
    )
    to_currency, _ = Currency.objects.get_or_create(
        name=data['4. To_Currency Name'],
        code=data['3. To_Currency Code'],
    )
    ExchangeRate.objects.update_or_create(
        from_currency=from_currency,
        to_currency=to_currency,
        defaults={
            'value': data['5. Exchange Rate'],
        },
    )
    return f"The exchange rate of BTC/USD is {data['5. Exchange Rate']}"
