from flask import Flask
from routes.heartbeat import heartbeat_bp
from routes.wake_up import wake_up_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(heartbeat_bp)
app.register_blueprint(wake_up_bp)

if __name__ == '__main__':
    app.run()
