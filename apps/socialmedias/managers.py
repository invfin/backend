import random
from typing import Dict, List

from django.db.models import Manager


class DefaultContentManager(Manager):
    def random_content(self, filter: Dict):
        return random.choice(list(self.filter(**filter)))


class TitlesManager(Manager):
    def random_title(self, filter: Dict):
        return random.choice(list(self.filter(**filter)))


class EmojisManager(Manager):
    def random_emojis(self, num) -> List:
        return random.choices(list(self.all()), k=num)


class HashtagsManager(Manager):
    def random_hashtags(self, platform) -> List:
        return list(self.filter(platform=platform))
