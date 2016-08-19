"""
mds3 - Our OPAL Application
"""
from opal.core import application

class Application(application.OpalApplication):
    flow_module   = 'mds3.flow'
    javascripts   = [
        'js/mds3/routes.js',
        'js/opal/controllers/discharge.js',
        # Uncomment this if you want to implement custom dynamic flows.
        # 'js/mds3/flow.js',
    ]