"""
::Portfolio::

run_boom.py

To run the server
"""

from portfolio import Portfolio

# Import get_env for the system environment to retrieve the environment
from application import get_env

# Import the application's views
import application.boom.views

# The directory containing your views/portfolio/templates
app_dir = "application/boom"

# Get the environment: Development, Production. To help with config
app_env = get_env()

# The project config object
app_config = "application.config.%s" % app_env

# Portfolio.init returns Flask instance
app = Portfolio.init(__name__, directory=app_dir, config=app_config)

if __name__ == "__main__":
    app.run()
