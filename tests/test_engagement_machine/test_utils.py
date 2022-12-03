from datetime import datetime, timedelta


from src.engagement_machine.utils import more_than_month


class TestUtils:
    def test_more_than_month(self):
        now_less_ten = datetime.now() - timedelta(10)
        assert more_than_month(now_less_ten) is False

        now_less_twenty = datetime.now() - timedelta(20)
        assert more_than_month(now_less_twenty) is False

        now_less_thirty = datetime.now() - timedelta(40)
        assert more_than_month(now_less_thirty) is True
