from app import app

if __name__ == '__main__':
    # For a self-contained desktop app feel, running on 127.0.0.1 is typical.
    # Port 5000 is standard for Flask development.
    # debug=False is important for a "production" bundled app.
    app.run(host='127.0.0.1', port=5000, debug=False)
