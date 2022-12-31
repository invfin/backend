from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from src.empresas.models import Company
from src.seo.views import SEOFormView

from ..forms import (
    AddCategoriesForm,
    AddNewAssetForm,
    CashflowMoveForm,
    DefaultCurrencyForm,
    FinancialObjectifForm,
    PositionMovementForm,
)


class BaseFinancialFormView(LoginRequiredMixin, SEOFormView):
    no_index = True
    no_follow = True
    success_message = "Guardado correctamente"

    def successful_return(self):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return HttpResponse(status=204, headers={"HX-Trigger": "showMessageSuccess"})

    def form_valid(self, form):
        form.save(self.request)
        return self.successful_return()


class CurrencyInitial(BaseFinancialFormView):
    def get_initial(self):
        initial = super().get_initial()
        initial["currency"] = self.request.user.user_patrimoine.default_currency
        return initial


class AddDefaultCurrencyView(CurrencyInitial):
    template_name = "modals/default_currency.html"
    form_class = DefaultCurrencyForm


class AddCashflowMoveView(CurrencyInitial):
    template_name = "modals/cashflowmoves.html"
    form_class = CashflowMoveForm


class AddPositionMovementView(CurrencyInitial):
    template_name = "modals/asset_movement.html"
    form_class = PositionMovementForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AddCategoriesView(BaseFinancialFormView):
    template_name = "modals/categories.html"
    form_class = AddCategoriesForm


class AddFinancialObjectifView(BaseFinancialFormView):
    template_name = "modals/objectives.html"
    form_class = FinancialObjectifForm


class AddNewAssetView(CurrencyInitial):
    template_name = "modals/new_asset.html"
    form_class = AddNewAssetForm

    def form_valid(self, form):
        empresa_ticker = self.request.POST["stock"].split(" [")[1]
        ticker = empresa_ticker[:-1]
        empresa_busqueda = Company.objects.get(ticker=ticker)
        form.save(self.request, empresa_busqueda)
        return self.successful_return()
