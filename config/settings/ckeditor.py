# CKEditor
# ------------------------------------------------------------------------------
# CKEDITOR_BASEPATH = STATIC_ROOT+"/ckeditor/ckeditor/"

CKEDITOR_UPLOAD_PATH = "uploads/"


DEFAULT_EDITOR = {
    "toolbar": "Full",
    "toolbar_Full": [
        {
            "name": "document",
            "items": ["Source", "-", "Save", "NewPage", "Preview", "Print", "-", "Templates"],
        },
        {
            "name": "clipboard",
            "items": [
                "Cut",
                "Copy",
                "Paste",
                "PasteText",
                "PasteFromWord",
                "-",
                "Undo",
                "Redo",
            ],
        },
        {"name": "editing", "items": ["Find", "Replace", "-", "SelectAll"]},
        {
            "name": "forms",
            "items": [
                "Form",
                "Checkbox",
                "Radio",
                "TextField",
                "Textarea",
                "Select",
                "Button",
                "ImageButton",
                "HiddenField",
            ],
        },
        "/",
        {
            "name": "basicstyles",
            "items": [
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "Subscript",
                "Superscript",
                "-",
                "RemoveFormat",
            ],
        },
        {
            "name": "paragraph",
            "items": [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "Blockquote",
                "CreateDiv",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
                "-",
                "BidiLtr",
                "BidiRtl",
                "Language",
            ],
        },
        {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
        {
            "name": "insert",
            "items": [
                "Image",
                "Flash",
                "Table",
                "HorizontalRule",
                "Smiley",
                "SpecialChar",
                "PageBreak",
                "Iframe",
            ],
        },
        "/",
        {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
        {"name": "colors", "items": ["TextColor", "BGColor"]},
        {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
        {"name": "about", "items": ["About"]},
        "/",  # put this to force next toolbar on new line
        {
            "name": "yourcustomtools",
            "items": [
                # put the name of your editor.ui.addButton here
                "Preview",
                "Maximize",
            ],
        },
    ],
    "startupFocus": False,
    "pasteFromWordPromptCleanup": True,
    "pasteFromWordRemoveFontStyles": True,
    "disableNativeSpellChecker": False,
    "extraPlugins": "scayt",
    "scayt_autoStartup": True,
    "removePlugins": "elementspath",
    "resize_enabled": False,
    "forcePasteAsPlainText": True,
    "ignoreEmptyParagraph": True,
    "removeFormatAttributes": True,
    "allowedContent": True,
    "width": "full",
}
SIMPLE_EDITOR = {
    "toolbar": [
        {"name": "insert", "items": ["Smiley"]},
        {"name": "styles", "items": ["Styles"]},
        {"name": "colors", "items": ["Colors"]},
        {"name": "links", "items": ["Link", "Unlink"]},
        {"name": "basicstyles", "items": ["Bold", "Italic", "Strike", "-", "RemoveFormat"]},
    ],
    "width": "full",
}
WRITER_EDITOR = {
    "toolbar": [
        {"name": "clipboard", "items": ["Undo", "Redo"]},
        {"name": "styles", "items": ["Styles", "Format"]},
        {"name": "basicstyles", "items": ["Bold", "Italic", "Strike", "-", "RemoveFormat"]},
        {
            "name": "paragraph",
            "items": [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "Blockquote",
            ],
        },
        {"name": "links", "items": ["Link", "Unlink"]},
        {"name": "insert", "items": ["Image", "EmbedSemantic", "Table"]},
        {"name": "tools", "items": ["Maximize"]},
        {"name": "editing", "items": ["Scayt"]},
    ],
    "width": "full",
    "extraPlugins": "autoembed,embedsemantic,image2,uploadimage",
    "removePlugins": "image",
    "bodyClass": "article-editor",
    "format_tags": "p;h1;h2;h3;pre",
    "removeDialogTabs": "image:advanced;link:advanced",
    "stylesSet": [
        {"name": "Marker", "element": "span", "attributes": {"class": "marker"}},
        {"name": "Cited Work", "element": "cite"},
        {"name": "Inline Quotation", "element": "q"},
        {
            "name": "Special Container",
            "element": "div",
            "styles": {
                "padding": "5px 10px",
                "background": "#eee",
                "border": "1px solid #ccc",
            },
        },
        {
            "name": "Compact table",
            "element": "table",
            "attributes": {
                "cellpadding": "5",
                "cellspacing": "0",
                "border": "1",
                "bordercolor": "#ccc",
            },
            "styles": {"border-collapse": "collapse"},
        },
        {
            "name": "Borderless Table",
            "element": "table",
            "styles": {"border-style": "hidden", "background-color": "#E6E6FA"},
        },
        {
            "name": "Square Bulleted List",
            "element": "ul",
            "styles": {"list-style-type": "square"},
        },
        {
            "name": "Illustration",
            "type": "widget",
            "widget": "image",
            "attributes": {"class": "image-illustration"},
        },
        {
            "name": "240p",
            "type": "widget",
            "widget": "embedSemantic",
            "attributes": {"class": "embed-240p"},
        },
        {
            "name": "360p",
            "type": "widget",
            "widget": "embedSemantic",
            "attributes": {"class": "embed-360p"},
        },
        {
            "name": "480p",
            "type": "widget",
            "widget": "embedSemantic",
            "attributes": {"class": "embed-480p"},
        },
        {
            "name": "720p",
            "type": "widget",
            "widget": "embedSemantic",
            "attributes": {"class": "embed-720p"},
        },
        {
            "name": "1080p",
            "type": "widget",
            "widget": "embedSemantic",
            "attributes": {"class": "embed-1080p"},
        },
    ],
}

CKEDITOR_CONFIGS = {
    "default": DEFAULT_EDITOR,
    "simple": SIMPLE_EDITOR,
    "writer": WRITER_EDITOR,
}
