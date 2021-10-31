from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quotes.models import ExchangeRate
from quotes.tasks import alphavantage_synchronizer


class QuotesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        btc_usd = (
            ExchangeRate.objects.filter(from_currency__code='BTC', to_currency__code='USD')
            .select_related('from_currency', 'to_currency')
            .first()
        )
        if not btc_usd:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(
            f'The exchange rate of {btc_usd.from_currency.code}/{btc_usd.to_currency.code} ' f'is {btc_usd.value}',
        )

    def post(self, request, *args, **kwargs):
        return Response(alphavantage_synchronizer())
