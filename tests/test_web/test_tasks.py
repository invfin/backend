from unittest.mock import patch

from django.test import TestCase


class TestTask(TestCase):
    @patch("apps.web.tasks.send_periodically_email_engagement_task")
    def test_send_periodically_email_engagement_task(self, mock_update):
        with self.assertRaises(Destination.DoesNotExist):
            update_destination_metrics_task(destination_id=1234)
            mock_update.not_called()

        destination = DestinationFactory()
        update_destination_metrics_task(destination_id=destination.id)
        mock_update.called_with(destination)
