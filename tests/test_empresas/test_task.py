from unittest import skip
from unittest.mock import patch

from django.core import mail
from django.test import TestCase

from bfet import DjangoTestingModel

from apps.empresas.models import Company
from apps.empresas.tasks import CompanyTask
from apps.empresas.outils.retrieve_data import RetrieveCompanyData


class TestCompanyTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.apple = DjangoTestingModel.create(
            Company,
            ticker="AAPL",
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "no"},
                "has_institutionals": {"time": "", "state": "no"},
                "has_first_financials_finnhub_info": {"time": "", "state": "yes"},
                "has_first_financials_yfinance_info": {"time": "", "state": "no"},
                "has_latest_financials_finprep_info": {"time": "", "state": "no"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "no"},
                "has_launch_fix_update": {"state": "no", "time": ""},
            },
        )
        cls.intc = DjangoTestingModel.create(
            Company,
            ticker="INTC",
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "yes"},
                "has_institutionals": {"time": "", "state": "yes"},
                "has_first_financials_finnhub_info": {"time": "", "state": "no"},
                "has_first_financials_yfinance_info": {"time": "", "state": "yes"},
                "has_latest_financials_finprep_info": {"time": "", "state": "yes"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "yes"},
                "has_launch_fix_update": {"state": "yes", "time": ""},
            },
        )
        cls.lvmh = DjangoTestingModel.create(
            Company,
            ticker="LVMH",
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "no"},
                "has_institutionals": {"time": "", "state": "no"},
                "has_first_financials_finnhub_info": {"time": "", "state": "yes"},
                "has_first_financials_yfinance_info": {"time": "", "state": "yes"},
                "has_latest_financials_finprep_info": {"time": "", "state": "no"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "yes"},
                "has_launch_fix_update": {"state": "yes", "time": ""},
            },
        )

    def test_retrieve_company(self):
        assert self.intc == CompanyTask("first_financials_finnhub_info", "key_stats").retrieve_company()
        assert self.apple == CompanyTask("first_financials_yahooquery_info", "key_stats").retrieve_company()
        assert CompanyTask("key_stats", "key_stats").retrieve_company() is None

    @patch("apps.empresas.outils.retrieve_data.RetrieveCompanyData.create_financials_finprep")
    @patch("apps.empresas.outils.retrieve_data.RetrieveCompanyData.create_financials_finnhub")
    @patch("apps.empresas.outils.retrieve_data.RetrieveCompanyData.create_key_stats_yahooquery")
    @patch("apps.empresas.outils.retrieve_data.RetrieveCompanyData.create_institutionals_yahooquery")
    @patch("apps.empresas.tasks.CompanyTask.yfinance_tasks")
    @patch("apps.empresas.tasks.CompanyTask.yahoo_query_tasks")
    def test_select_task(
        self,
        mock_yahoo_query_tasks,
        mock_yfinance_tasks,
        mock_create_institutionals_yahooquery,
        mock_create_key_stats_yahooquery,
        mock_create_financials_finnhub,
        mock_create_financials_finprep,
    ):
        tasks_map = {
            "financials_yfinance_info": mock_yfinance_tasks,
            "financials_yahooquery_info": mock_yahoo_query_tasks,
            "financials_finprep_info": mock_create_financials_finprep,
            "financials_finnhub_info": mock_create_financials_finnhub,
            "key_stats": mock_create_key_stats_yahooquery,
            "institutionals": mock_create_institutionals_yahooquery,
        }
        for key, value in tasks_map.items():
            with self.subTest(key):
                retrieve_data = RetrieveCompanyData(self.intc)
                CompanyTask("key_stats", key).select_task(retrieve_data)
                if "financials_yfinance_info" == key or "financials_yahooquery_info" == key:
                    assert value.called_with(retrieve_data)
                else:
                    value.assert_called_once()

    def test_send_ending_message(self):
        checking = "key_stats"
        CompanyTask(checking, "key_stats").send_ending_message()
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == f"No companies left to check for {checking}"
        assert mail.outbox[0].body == f"All companies have info for {checking}"
        assert mail.outbox[0].from_email == "InvFin - Automatic <EMAIL_DEFAULT@example.com>"
        assert mail.outbox[0].to == ["InvFin - Automatic <EMAIL_DEFAULT@example.com>"]

    @patch("apps.empresas.outils.retrieve_data.RetrieveCompanyData.create_financials_yahooquery")
    @patch("apps.empresas.outils.retrieve_data.RetrieveCompanyData.create_financials_yahooquery")
    def test_yahoo_query_tasks(self, mock_create_financials_yahooquery, mock_create_financials_yahooquery_2):
        retrieve_data = RetrieveCompanyData(self.intc)
        CompanyTask("key_stats", "key_stats").yahoo_query_tasks(retrieve_data)
        mock_create_financials_yahooquery.called_with("a")
        mock_create_financials_yahooquery_2.called_with("q")

    @patch("apps.empresas.outils.retrieve_data.RetrieveCompanyData.create_financials_yfinance")
    @patch("apps.empresas.outils.retrieve_data.RetrieveCompanyData.create_financials_yfinance")
    def test_yfinance_tasks(self, mock_create_financials_yfinance, mock_create_financials_yfinance_2):
        retrieve_data = RetrieveCompanyData(self.intc)
        CompanyTask("key_stats", "key_stats").yfinance_tasks(retrieve_data)
        mock_create_financials_yfinance.called_with("a")
        mock_create_financials_yfinance_2.called_with("q")

    @patch("apps.empresas.tasks.CompanyTask.select_task")
    def test_launch_task(self, mock_select_task):
        with self.subTest("called select task"):
            CompanyTask("first_financials_finnhub_info", "key_stats").launch_task()
            mock_select_task.assert_called_once()
        with self.subTest("not called select task"):
            checking = "key_stats"
            CompanyTask(checking, "key_stats").launch_task()
            assert len(mail.outbox) == 1
            assert mail.outbox[0].subject == f"No companies left to check for {checking}"
            assert mail.outbox[0].body == f"All companies have info for {checking}"
            assert mail.outbox[0].from_email == "InvFin - Automatic <EMAIL_DEFAULT@example.com>"
            assert mail.outbox[0].to == ["InvFin - Automatic <EMAIL_DEFAULT@example.com>"]


class TestTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.apple = DjangoTestingModel.create(
            Company,
            ticker="AAPL",
            checkings={
                "has_key_stats": {"time": "", "state": "no"},
                "has_meta_image": {"time": "", "state": "no"},
                "has_institutionals": {"time": "", "state": "no"},
                "has_first_financials_finnhub_info": {"time": "", "state": "no"},
                "has_first_financials_yfinance_info": {"time": "", "state": "no"},
                "has_latest_financials_finprep_info": {"time": "", "state": "no"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "no"},
                "has_launch_fix_update": {"state": "no", "time": ""},
            },
        )
        cls.int = DjangoTestingModel.create(
            Company,
            ticker="INTC",
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "yes"},
                "has_institutionals": {"time": "", "state": "yes"},
                "has_first_financials_finnhub_info": {"time": "", "state": "yes"},
                "has_first_financials_yfinance_info": {"time": "", "state": "yes"},
                "has_latest_financials_finprep_info": {"time": "", "state": "yes"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "yes"},
                "has_launch_fix_update": {"state": "yes", "time": ""},
            },
        )
        cls.lvmh = DjangoTestingModel.create(
            Company,
            ticker="LVMH",
            checkings={
                "has_key_stats": {"time": "", "state": "yes"},
                "has_meta_image": {"time": "", "state": "no"},
                "has_institutionals": {"time": "", "state": "no"},
                "has_first_financials_finnhub_info": {"time": "", "state": "no"},
                "has_first_financials_yfinance_info": {"time": "", "state": "yes"},
                "has_latest_financials_finprep_info": {"time": "", "state": "no"},
                "has_first_financials_yahooquery_info": {"time": "", "state": "no"},
                "has_launch_fix_update": {"state": "yes", "time": ""},
            },
        )

    @patch("apps.empresas.tasks.create_averages_task.delay")
    def test_create_averages_task(self, mock_create_averages_task):
        pass

    @patch("apps.empresas.tasks.create_ttm_task.delay")
    def test_create_ttm_task(self, mock_create_ttm_task):
        pass

    @patch("apps.empresas.tasks.arrange_quarters_task.delay")
    def test_arrange_quarters_task(self, mock_arrange_quarters_task):
        pass
