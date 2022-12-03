from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from src.engagement_machine.tasks import send_email_engagement_task


class SendNewsletterView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request, pk, format=None):
        send_email_engagement_task.delay(pk)
        return Response(
            status=status.HTTP_202_ACCEPTED,
            headers={"HX-Trigger": "refreshNewsletterList"},
        )
