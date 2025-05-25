import boland_website

app = boland_website.create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)