from flask import Flask
from admin_module import routes

app = Flask(__name__)
routes.register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
