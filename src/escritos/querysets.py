from src.general.managers import BaseQuerySet


class TermCorrectionQuerySet(BaseQuerySet):
    def get_contributors(self, term):
        return (
            self.filter(
                term_content_related__term_related=term,
                is_approved=True,
            )
            .order_by("corrected_by_id")
            .distinct("corrected_by")
            .only("corrected_by")

        )
