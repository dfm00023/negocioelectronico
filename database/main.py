from utils.api import app

def main():
    app.run(debug=True, host='0.0.0.0', port=9876)

if __name__ == "__main__":
    main()