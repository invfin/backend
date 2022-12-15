class EmailExtension:
    @property
    def email_serialized(self):
        return {
            "subject": self.title,
            "content": self.content,
            "call_to_action": self.call_to_action,
            "call_to_action_url": self.call_to_action_url,
            **self.dict_for_task,
        }

    @property
    def opening_rate(self):
        all_emails = self.email_related.all().count()
        all_opened = self.email_related.filter(opened=True).count()
        rate = all_emails / all_opened if all_opened != 0 else 0
        return round(rate, 2)
