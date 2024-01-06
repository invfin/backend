import json
from datetime import datetime

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name) -> bool:
    return user.groups.filter(name=group_name).exists()


@register.filter(name="readable_date")
def readable_date(date: str | int) -> str:
    if isinstance(date, str):
        date = int(date)
    return datetime.utcfromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")


@register.filter(name="per_cent")
def percentagement(value: int | float) -> int | float:
    return value * 100


@register.simple_tag(name="utm")
def add_utms(
    content: str = "",
    term: str = "",
    medium: str = "webapp",
    source: str = "invfin",
    campaign: str = "website-links",
) -> str:
    utm_source = f"utm_source={source}"
    utm_medium = f"utm_medium={medium}"
    utm_campaign = f"utm_campaign={campaign}"
    utm_content = f"utm_content={content}"
    utm_term = f"utm_term={term}"
    return f"?{utm_source}&{utm_medium}&{utm_content}&{utm_campaign}&{utm_term}"


@register.simple_tag(name="clean_json")
def api_json_example(example):
    json.loads(example)
    return json.dumps(example, indent=4, sort_keys=True)


@register.simple_tag(name="pre_loading")
def render_pre_loading(link_params: str, extra, *args) -> str:
    link = reverse(link_params, args=args)
    return mark_safe(
        f"""<div hx-trigger="load" hx-target="this"
    hx-get='{link}?extra={extra}'>
    <div class="text-center">
        <div class="spinner-border" role="status"></div>
        Cargando...
    </div>
</div>
"""
    )


@register.simple_tag(name="open_modal")
def render_open_modal(link_params: str, text: str, class_attrs: str = "") -> str:
    link = reverse(link_params)
    return mark_safe(
        f'<button class="{class_attrs} dropdown-item"'
        f' hx-get="{link} "hx-target="#SharedModalDialog">{text}</button>'
    )
