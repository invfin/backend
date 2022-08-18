from model_bakery import baker

from apps.users.tests.factories import regular_user
from apps.screener.models import (
BasePrediction,
CompanyInformationBought,
FavoritesEtfsHistorial,
FavoritesEtfsList,
FavoritesStocksHistorial,
FavoritesStocksList,
UserCompanyObservation,
UserScreenerMediumPrediction,
UserScreenerSimplePrediction,
YahooScreener,
)


baker.make(BasePrediction)
baker.make(CompanyInformationBought)
baker.make(FavoritesEtfsHistorial)
baker.make(FavoritesEtfsList)
baker.make(FavoritesStocksHistorial)
baker.make(FavoritesStocksList)
baker.make(UserCompanyObservation)
baker.make(UserScreenerMediumPrediction)
baker.make(UserScreenerSimplePrediction)
baker.make(YahooScreener)