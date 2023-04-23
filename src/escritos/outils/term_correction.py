from typing import List, Optional

from django.utils import timezone

from src.notifications.constants import CORRECTION_APPROVED
from src.notifications.tasks import prepare_notification_task

from ..models import TermContent, TermCorrection


class TermCorrectionManagement:
    term_correction: TermCorrection
    term_content: TermContent

    def __init__(self, term_correction: TermCorrection):
        self.term_correction = term_correction
        self.term_content: TermContent = term_correction.term_content_related  # type: ignore

    def approve_correction(self, approved_by, fields: List[str]) -> None:
        self.update_correction_data_when_approved(approved_by, fields)
        prepare_notification_task.delay(self.term_correction.dict_for_task, CORRECTION_APPROVED)  # type: ignore
        return None

    def create_content(self):
        return (
            f"Enhorabuena, tu correción para <a href='{self.term_correction.shareable_link}' "
            f"target='_blank'>{self.term_correction.title}</a> ha sido aprovada."
            "<br></br>"
            "Desde el equipo de InvFin te damos las gracias por ayudar a mejorar el contenido para "
            "poder seguir ayudando al resto de la comunidad."
        )

    def update_correction_data_when_approved(self, approved_by, fields: List[str]) -> None:
        self.term_correction.is_approved = True
        self.term_correction.date_approved = timezone.now()
        self.term_correction.approved_by = approved_by
        self.replace_content_with_correction(fields)
        self.term_correction.save(update_fields=["is_approved", "date_approved", "approved_by"])
        return None

    def replace_content_with_correction(self, fields: List[str]) -> None:
        fields_to_update = list(filter(self.update_related_field, fields))
        self.term_content.save(update_fields=fields_to_update)
        return None

    def update_related_field(self, field: str) -> Optional[str]:
        original = getattr(self.term_content, field) if self.term_content else None
        correction = getattr(self.term_correction, field)
        if all([original, correction, original != correction]):
            setattr(self.term_content, field, correction)
            return field
        return None
