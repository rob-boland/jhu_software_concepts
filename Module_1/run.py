from flask import Flask

# Module imports
import pages

# Create Flask application and register blueprints
app = Flask(__name__)
app.register_blueprint(pages.bp)

if __name__ == "__main__":
    # Run locally in debug mode
    app.run(host="0.0.0.0", port=5000, debug=True)

#adding a comment for git