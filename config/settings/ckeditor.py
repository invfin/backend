# CKEditor
# ------------------------------------------------------------------------------
# CKEDITOR_BASEPATH = STATIC_ROOT+"/ckeditor/ckeditor/"

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Full",
        "toolbar_Full": [
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
            {
                "name": "editing",
                "items": [
                    "Find",
                    "Replace",
                    "-",
                    "SelectAll",
                    "-",
                    "SpellChecker",
                    "Scayt",
                ],
            },
            {
                "name": "basics",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "NumberedList",
                    "BulletedList",
                    "Link",
                    "Unlink",
                    "Anchor",
                    "Table",
                ],
            },
            {
                "name": "tools",
                "items": [
                    "Maximize",
                ],
            },
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Source",
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
    },
    "simple": {
        "toolbar": [
            {"name": "insert", "items": ["Smiley"]},
            {"name": "styles", "items": ["Styles"]},
            {"name": "colors", "items": ["Colors"]},
            {"name": "links", "items": ["Link", "Unlink"]},
            {"name": "basicstyles", "items": ["Bold", "Italic", "Strike", "-", "RemoveFormat"]},
        ],
        "width": "full",
    },
    "writter": {
        "toolbar": [
            {"name": "clipboard", "items": ["Undo", "Redo"]},
            {"name": "styles", "items": ["Styles", "Format"]},
            {"name": "basicstyles", "items": ["Bold", "Italic", "Strike", "-", "RemoveFormat"]},
            {
                "name": "paragraph",
                "items": ["NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Blockquote"],
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
                "styles": {"padding": "5px 10px", "background": "#eee", "border": "1px solid #ccc"},
            },
            {
                "name": "Compact table",
                "element": "table",
                "attributes": {"cellpadding": "5", "cellspacing": "0", "border": "1", "bordercolor": "#ccc"},
                "styles": {"border-collapse": "collapse"},
            },
            {
                "name": "Borderless Table",
                "element": "table",
                "styles": {"border-style": "hidden", "background-color": "#E6E6FA"},
            },
            {"name": "Square Bulleted List", "element": "ul", "styles": {"list-style-type": "square"}},
            {
                "name": "Illustration",
                "type": "widget",
                "widget": "image",
                "attributes": {"class": "image-illustration"},
            },
            {"name": "240p", "type": "widget", "widget": "embedSemantic", "attributes": {"class": "embed-240p"}},
            {"name": "360p", "type": "widget", "widget": "embedSemantic", "attributes": {"class": "embed-360p"}},
            {"name": "480p", "type": "widget", "widget": "embedSemantic", "attributes": {"class": "embed-480p"}},
            {"name": "720p", "type": "widget", "widget": "embedSemantic", "attributes": {"class": "embed-720p"}},
            {"name": "1080p", "type": "widget", "widget": "embedSemantic", "attributes": {"class": "embed-1080p"}},
        ],
    },
}
