import os

from django.core.management import BaseCommand

import pandas as pd

from src.empresas.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        base_path = "/home/lucas/Dev/recover-db/companies/"
        for company_file in os.listdir(base_path):
            df = pd.read_parquet(f"{base_path}{company_file}")
            df.drop_duplicates()

            inc_df = pd.DataFrame()
            bs_df = pd.DataFrame()
            cf_df = pd.DataFrame()

            inc_df["date"] = df["date"]
            bs_df["date"] = df["date"]
            cf_df["date"] = df["date"]

            inc_df["revenue"] = df["revenue"]
            inc_df["cost_of_revenue"] = df["costofrevenue"]
            inc_df["gross_profit"] = df["grossprofit"]
            inc_df["research_and_development_expenses"] = df["researchanddevelopmentexpenses"]
            inc_df["general_and_administrative_expenses"] = df["generalandadministrativeexpenses"]
            inc_df["selling_and_marketing_expenses"] = df["sellingandmarketingexpenses"]
            inc_df["selling_general_and_administrative_expenses"] = df["sellinggeneralandadministrativeexpenses"]
            inc_df["other_expenses"] = df["otherexpenses"]
            inc_df["operating_expenses"] = df["operatingexpenses"]
            inc_df["cost_and_expenses"] = df["costandexpenses"]
            inc_df["interest_expense"] = df["interestexpense"]
            inc_df["depreciation_and_amortization"] = df["depreciationandamortization_x"]
            inc_df["ebitda"] = df["ebitda"]
            inc_df["operating_income"] = df["operatingincome"]
            inc_df["total_other_income_expenses_net"] = df["totalotherincomeexpensesnet"]
            inc_df["income_before_tax"] = df["incomebeforetax"]
            inc_df["income_tax_expense"] = df["incometaxexpense"]
            inc_df["net_income"] = df["netincome_x"]
            inc_df["weighted_average_shs_out"] = df["weightedaverageshsout"]
            inc_df["weighted_average_shs_out_dil"] = df["weightedaverageshsoutdil"]

            bs_df["account_payables"] = df["accountpayables"]
            bs_df["accumulated_other_comprehensive_income_loss"] = df["accumulatedothercomprehensiveincomeloss"]
            bs_df["cash_and_cash_equivalents"] = df["cashandcashequivalents"]
            bs_df["cash_and_short_term_investments"] = df["cashandshortterminvestments"]
            bs_df["common_stock"] = df["commonstock"]
            bs_df["deferred_revenue"] = df["deferredrevenue"]
            bs_df["deferred_revenue_non_current"] = df["deferredrevenuenoncurrent"]
            bs_df["deferred_tax_liabilities_non_current"] = df["deferredtaxliabilitiesnoncurrent"]
            bs_df["goodwill"] = df["goodwill"]
            bs_df["goodwill_and_intangible_assets"] = df["goodwillandintangibleassets"]
            bs_df["intangible_assets"] = df["intangibleassets"]
            bs_df["inventory"] = df["inventory_x"]
            bs_df["long_term_debt"] = df["longtermdebt"]
            bs_df["long_term_investments"] = df["longterminvestments"]
            bs_df["net_debt"] = df["netdebt"]
            bs_df["net_receivables"] = df["netreceivables"]
            bs_df["other_assets"] = df["otherassets"]
            bs_df["other_current_assets"] = df["othercurrentassets"]
            bs_df["other_current_liabilities"] = df["othercurrentliabilities"]
            bs_df["other_liabilities"] = df["otherliabilities"]
            bs_df["other_non_current_assets"] = df["othernoncurrentassets"]
            bs_df["other_non_current_liabilities"] = df["othernoncurrentliabilities"]
            bs_df["othertotal_stockholders_equity"] = df["othertotalstockholdersequity"]
            bs_df["property_plant_equipment_net"] = df["propertyplantequipmentnet"]
            bs_df["retained_earnings"] = df["retainedearnings"]
            bs_df["short_term_debt"] = df["shorttermdebt"]
            bs_df["short_term_investments"] = df["shortterminvestments"]
            bs_df["tax_assets"] = df["taxassets"]
            bs_df["tax_payables"] = df["taxpayables"]
            bs_df["total_assets"] = df["totalassets"]
            bs_df["total_current_assets"] = df["totalcurrentassets"]
            bs_df["total_current_liabilities"] = df["totalcurrentliabilities"]
            bs_df["total_debt"] = df["totaldebt"]
            bs_df["total_investments"] = df["totalinvestments"]
            bs_df["total_liabilities"] = df["totalliabilities"]
            bs_df["total_liabilities_and_stockholders_equity"] = df["totalliabilitiesandstockholdersequity"]
            bs_df["total_non_current_assets"] = df["totalnoncurrentassets"]
            bs_df["total_non_current_liabilities"] = df["totalnoncurrentliabilities"]
            bs_df["total_stockholders_equity"] = df["totalstockholdersequity"]

            cf_df["accounts_payables"] = df["accountspayables"]
            cf_df["accounts_receivables"] = df["accountsreceivables"]
            cf_df["acquisitions_net"] = df["acquisitionsnet"]
            cf_df["capital_expenditure"] = df["capitalexpenditure"]
            cf_df["cash_at_beginning_of_period"] = df["cashatbeginningofperiod"]
            cf_df["cash_at_end_of_period"] = df["cashatendofperiod"]
            cf_df["change_in_working_capital"] = df["changeinworkingcapital"]
            cf_df["common_stock_issued"] = df["commonstockissued"]
            cf_df["common_stock_repurchased"] = df["commonstockrepurchased"]
            cf_df["debt_repayment"] = df["debtrepayment"]
            cf_df["deferred_income_tax"] = df["deferredincometax"]
            cf_df["depreciation_and_amortization"] = df["depreciationandamortization_x"]
            cf_df["dividends_paid"] = df["dividendspaid"]
            cf_df["effect_of_forex_changes_on_cash"] = df["effectofforexchangesoncash"]
            cf_df["free_cash_flow"] = df["freecashflow"]
            cf_df["inventory"] = df["inventory_y"]
            cf_df["investments_in_property_plant_and_equipment"] = df["investmentsinpropertyplantandequipment"]
            cf_df["net_cash_provided_by_operating_activities"] = df["netcashprovidedbyoperatingactivities"]
            cf_df["net_cash_used_for_investing_activites"] = df["netcashusedforinvestingactivites"]
            cf_df["net_cash_used_provided_by_financing_activities"] = df["netcashusedprovidedbyfinancingactivities"]
            cf_df["net_change_in_cash"] = df["netchangeincash"]
            cf_df["net_income"] = df["netincome_y"]
            cf_df["operating_cash_flow"] = df["operatingcashflow"]
            cf_df["other_financing_activites"] = df["otherfinancingactivites"]
            cf_df["other_investing_activites"] = df["otherinvestingactivites"]
            cf_df["other_non_cash_items"] = df["othernoncashitems"]
            cf_df["other_working_capital"] = df["otherworkingcapital"]
            cf_df["purchases_of_investments"] = df["purchasesofinvestments"]
            cf_df["sales_maturities_of_investments"] = df["salesmaturitiesofinvestments"]
            cf_df["stock_based_compensation"] = df["stockbasedcompensation"]

            inc_df = list(inc_df.T.to_dict().values())
            bs_df = list(bs_df.T.to_dict().values())
            cf_df = list(cf_df.T.to_dict().values())
            ticker = company_file.replace(".parquet", "")
            company = Company.objects.get(ticker=ticker)
            for statement in inc_df:
                date = statement.pop("date")
                company.incomestatementfinprep_set.filter(date=date).update(**statement)

            for statement in bs_df:
                date = statement.pop("date")
                company.balancesheetfinprep_set.filter(date=date).update(**statement)

            for statement in cf_df:
                date = statement.pop("date")
                company.cashflowstatementfinprep_set.filter(date=date).update(**statement)
