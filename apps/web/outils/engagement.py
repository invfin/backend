class EngagementMachine:
    def send_website_email_engagement():
        for user in User.objects.all():
            last_email_engagement = WebsiteEmailTrack.objects.filter(
                sent_to=user,
                email_related__sent=True,
                email_related__type_related__slug__startswith=constants.CONTENT_FOR_ENGAGEMENT
                )
            if last_email_engagement.exists():
                # If an email for engagement has already been sent then we check when was the last time the user
                # visited the web
                if (
                    user.last_time_seen and
                    more_than_month(user.last_time_seen, last_email_engagement.date_to_send)
                    # If the user hasn't visited the web in the last month (29 days)

                ):
                    web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_LITTLE_ACTIVE
                elif (
                    not user.last_time_seen and
                    more_than_month(last_email_engagement.date_to_send)
                    # If the user has never visited the web and the last email was sent more then a month back
                ):
                    web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_NO_ACTIVE
            else:
                web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_FIRST_CALL

            email_to_send = WebsiteContentCreation.create_save_email(web_objective)
