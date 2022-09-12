from .base import FULL_DOMAIN

WEB_ICON = "general/assets/img/favicon/favicon.ico"
WEB_MANIFEST = "/webmanifest.json"

TOP_MENU_LEFT = [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        # {"name": "Support", "url": "", "new_window": True},

        # model admin to link to (Permissions checked against model)
        # {"model": "users.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "users"},
    ]

TOP_MENU_RIGHT = [
        {"name": "Web", "url": FULL_DOMAIN, "new_window": True},
        {"name": "API", "url": f"{FULL_DOMAIN}/api/api-documentacion", "new_window": True},
        {"model": "users.user"}
    ]

SIDE_MENU = [
    {
        'label': 'Tasks',
        'icon': 'fas fa-tasks',
        'models': (
            {
                'model': 'django_celery_beat.PeriodicTask',
            },
        ),
    },
    {
        'label': 'Business',
        'icon': 'fas fa-briefcase',
        'models': (
            {
                'model': 'business.Customer',
                'label': "Customers",
            },
            {
                'model': 'business.Product',
                'label': "Products",
            },
            {
                'model': 'business.ProductComplementary',
                'label': "Products Complementary",
            },
        ),
    },
    {
        'label': 'Users',
        'icon': 'fas fa-user',
        'models': (
            {
                'model': 'users.user',
                'label': "Users",
            },
            {
                'model': 'seo.UserJourney',
                'label': "Journey",
            },
            {
                "model": "seo.UserCompanyVisited",
                "label": "Company visited"
            },
            {
                "model": "seo.UserPublicBlogVisited",
                "label": "Blog visited"
            },
            {
                "model": "seo.UserQuestionVisited",
                "label": "Question visited"
            },
            {
                "model": "seo.UserTermVisited",
                "label": "Term visited"
            },
        ),
    },
    {
        'label': 'Visiteurs',
        'icon': 'fas fa-user-secret',
        'models': (
            {
                'model': 'seo.Visiteur',
                'label': "Visiteurs",
            },
            {
                'model': 'seo.VisiteurJourney',
                'label': "Journey",
            },
            {
                "model": "seo.VisiteurCompanyVisited",
                "label": "Company visited"
            },
            {
                "model": "seo.VisiteurPublicBlogVisited",
                "label": "Blog visited"
            },
            {
                "model": "seo.VisiteurQuestionVisited",
                "label": "Question visited"
            },
            {
                "model": "seo.VisiteurTermVisited",
                "label": "Term visited"
            },
        ),
    },
    {
        'label': 'Empresas',
        'icon': 'fas fa-building',
        'models': (
            {
                'model': 'empresas.Company',
                'label': "Company",
            },
            {
                'model': 'empresas.CompanyStatementsProxy',
                'label': "Average & Ratios",
            },
            {
                'model': 'empresas.CompanyFinprepProxy',
                'label': "Finprep",
            },
            {
                'model': 'empresas.CompanyYahooQueryProxy',
                'label': "YahooQuery",
            },
            {
                'model': 'empresas.CompanyYFinanceProxy',
                'label': "YFinance",
            },
            {
                'model': 'empresas.CompanyFinnhubProxy',
                'label': "Finnhub",
            },
        ),
    },
    {
        'label': 'Company Relateds',
        'icon': 'fas fa-copy',
        'models': (
            {
                'model': 'empresas.ExchangeOrganisation',
                'label': "Exchanges",
            },
            {
                'model': 'empresas.InstitutionalOrganization',
                'label': "Institutions",
            },
            {
                'model': 'super_investors.Superinvestor',
                'label': "SuperInvestors",
            },
            {
                'model': 'general.Industry',
            },
            {
                'model': 'general.Sector',
            },
            {
                'model': 'general.Period',
            },
            {
                'model': 'empresas.CompanyUpdateLog',
                'label': "Company Logs",
            },
        ),
    },
    {
        'label': 'General',
        'icon': 'fas fa-globe',
        'models': (
            {
                'model': 'general.Category',
            },
            {
                'model': 'general.Tag',
            },
            {
                'model': 'general.Currency',
            },
            {
                'model': 'general.Country',
            },
        ),
    },
    {
        'label': 'API',
        'icon': 'fas fa-key',
        'models': (
            {
                'model': 'api.Key',
            },
            {
                'model': 'api.CompanyRequestAPI',
            },
            {
                'model': 'api.TermRequestAPI',
            },
            {
                'model': 'api.SuperinvestorRequestAPI',
            },
            {
                'model': 'api.EndpointsCategory',
            },
            {
                'model': 'api.Endpoint',
            },
        ),
    },
    {
        'label': 'Terms',
        'icon': 'fas fa-pen',
        'models': (
            {
                'model': 'escritos.Term',
                'label': "Terms",
            },
            {
                'model': 'escritos.TermCorrection',
                'label': "Corrections",
            },
        ),
    },
    {
        'label': 'Q&A',
        'icon': 'fas fa-question',
        'models': (
            {
                'model': 'preguntas_respuestas.Question',
                'label': "Questions",
            },
            {
                'model': 'preguntas_respuestas.Answer',
                'label': "Answers",
            },
        ),
    },
    {
        'label': 'Recsys',
        'icon': 'fas fa-globe',
        'models': (
            {
                'model': 'recsys.VisiteurCompanyRecommended',
            },
            {
                'model': 'recsys.UserCompanyRecommended',
            },
        ),
    },
    {
        'label': 'Raw company data',
        'icon': 'fas fa-file-excel',
        'models': (
            {"model": "empresas.IncomeStatement",},
            {"model": "empresas.BalanceSheet",},
            {"model": "empresas.CashflowStatement",},
            {"model": "empresas.RentabilityRatio",},
            {"model": "empresas.LiquidityRatio",},
            {"model": "empresas.MarginRatio",},
            {"model": "empresas.FreeCashFlowRatio",},
            {"model": "empresas.PerShareValue",},
            {"model": "empresas.NonGaap",},
            {"model": "empresas.OperationRiskRatio",},
            {"model": "empresas.EnterpriseValueRatio",},
            {"model": "empresas.CompanyGrowth",},
            {"model": "empresas.EficiencyRatio",},
            {"model": "empresas.PriceToRatio",},

            {"model": "empresas.IncomeStatementFinprep",},
            {"model": "empresas.BalanceSheetFinprep",},
            {"model": "empresas.CashflowStatementFinprep",},

            {"model": "empresas.IncomeStatementYahooQuery",},
            {"model": "empresas.BalanceSheetYahooQuery",},
            {"model": "empresas.CashflowStatementYahooQuery",},

            {"model": "empresas.IncomeStatementYFinance",},
            {"model": "empresas.BalanceSheetYFinance",},
            {"model": "empresas.CashflowStatementYFinance",},
        ),
    },
    {
        'label': 'Auth & Security',
        'icon': 'fas fa-shield-alt',
        'models': (
            {
                'model': 'auth.group',
                'label': "Groups",
                'icon': 'fas fa-shield-alt',
            },
            {
                'model': 'admin_honeypot.LoginAttempt',
                'label': "Honeypot",
            },
        ),
    },
]

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "InvFin Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "InvFin",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "InvFin",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": WEB_ICON,

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": WEB_ICON,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": WEB_ICON,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": WEB_ICON,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to InvFin",

    # Copyright on the footer
    "copyright": "InvFin",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "users.User",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": TOP_MENU_LEFT,

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": TOP_MENU_RIGHT,

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": False,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth"],

    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "books": [{
    #         "name": "Make Messages",
    #         "url": "make_messages",
    #         "icon": "fas fa-comments",
    #         "permissions": ["books.view_book"]
    #     }]
    # },

    "side_menu_models": SIDE_MENU,

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}

COLOR_PRIMARY = "primary"
COLOR_SECONDARY = "secondary"
COLOR_INFO = "info"
COLOR_WARNING = "warning"
COLOR_DANGER = "danger"
COLOR_SUCCESS = "success"

JAZZMIN_UI_TWEAKS = {
    "navbar": f'navbar-white navbar-light progress-bar-striped bg-{COLOR_WARNING}',
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_child_indent": True,
    "sidebar_nav_flat_style": True,
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "button_classes": {
        COLOR_PRIMARY: f"btn-{COLOR_PRIMARY}",
        COLOR_SECONDARY: f"btn-{COLOR_SECONDARY}",
        COLOR_INFO: f"btn-{COLOR_INFO}",
        COLOR_WARNING: f"btn-{COLOR_WARNING}",
        COLOR_DANGER: f"btn-{COLOR_DANGER}",
        COLOR_SUCCESS: f"btn-{COLOR_SUCCESS}"
    }
}
