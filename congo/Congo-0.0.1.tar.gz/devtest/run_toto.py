"""
::Portfolio::

run_toto.py

To run the server
"""

from portfolio import Portfolio

# Import get_env for the system environment to retrieve the environment
from application import get_env

# Import the application's views
import application.toto.views

# The directory containing your views/portfolio/templates
app_dir = "application/toto"

# Get the environment: Development, Production. To help with config
app_env = get_env()

# The project config object
app_config = "application.config.%s" % app_env

# Portfolio.init returns Flask instance
app = Portfolio.init(__name__, directory=app_dir, config=app_config)

if __name__ == "__main__":
    app.run()
