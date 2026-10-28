from app import create_app

app = create_app() #calls function and gets Flask app

if __name__ == "__main__":
    app.run(debug = True)
