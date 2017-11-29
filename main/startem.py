"""
Sets and starts the Flask Application using Blueprints

:return: Runnning Flask Application
"""

from flask import Flask
from tools.blueprints.page import page

# instantiating the Flas Application, with relative configuration enabled
app = Flask(__name__, instance_relative_config=True)

# Setting some configurations
app.config.from_object('config.settings')

# Calling the Main Page Blueprints
app.register_blueprint(page)

app.run()
