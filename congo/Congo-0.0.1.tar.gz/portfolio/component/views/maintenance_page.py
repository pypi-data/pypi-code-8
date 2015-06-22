"""
Maintenance Page
"""

from portfolio import Portfolio

def maintenance_page(template=None):
    """
    Create the Maintenance view
    Must be instantiated

    import maintenance_view
    MaintenanceView = maintenance_view()

    :param view_template: The directory containing the view pages
    :return:
    """
    if not template:
        template = "Portfolio/MaintenancePage/index.html"

    class Maintenance(Portfolio):
        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)

            if cls.get_config("MAINTENANCE_ON"):
                @app.before_request
                def on_maintenance():
                    return cls.render(layout=template), 503
    return Maintenance

MaintenanceV = maintenance_page()
