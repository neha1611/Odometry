from odometry.app import app
from odometry.settings import config

app.run_server(debug=config.debug, host = config.APP_HOST, port = config.APP_PORT)