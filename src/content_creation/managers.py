import random
from typing import Dict, List, Type

from django.db.models import Manager


class DefaultContentManager(Manager):
    def random_content(self, filter: Dict):
        list_content = list(self.filter(**filter))
        return random.choice(list_content) if list_content else None


class TitlesManager(Manager):
    def random_title(self, filter: Dict):
        list_titles = list(self.filter(**filter))
        return random.choice(list_titles) if list_titles else None


class EmojisManager(Manager):
    def random_emojis(self, num):
        list_emojis = list(self.all())
        return random.choices(list_emojis, k=num) if list_emojis else list_emojis


class HashtagsManager(Manager):
    def random_hashtags(self, platform):
        return list(self.filter(platform=platform))
