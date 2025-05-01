from app import create_app
from app.routes import routes
from app.vehicle_security_routes import vehicle_security_routes
import os

app = create_app()

# Register existing routes
app.register_blueprint(routes)

# Register the vehicle security routes
app.register_blueprint(vehicle_security_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)