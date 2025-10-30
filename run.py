from app import create_app

app = create_app('development')

if __name__ == '__main__':
    print("=== AGRICULTURAL COST PREDICTOR STARTING ===")
    app.run(debug=True)