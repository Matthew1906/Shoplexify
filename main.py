from onlineShop import create_app
from os import environ

# Deployment
app = create_app()
port = int(environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
    