from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import GenericAPIView

from apps.engagement_machine.tasks import send_email_engagement_task


class SendNewsletterView(GenericAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, *args, **kwargs):
        send_email_engagement_task.delay(self.kwargs["pk"])
        return Response(
            status=status.HTTP_202_ACCEPTED,
            headers={"HX-Trigger": "refreshNewsletterList"},
        )
