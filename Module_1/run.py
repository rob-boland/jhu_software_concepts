import boland_website


if __name__ == "__main__":
    # Create Flask app, run with localhost:5000 address.
    app = boland_website.create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)