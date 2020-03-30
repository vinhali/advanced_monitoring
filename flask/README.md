## Other method

    if __name__ == "__main__":
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
 

## CURL GET

    curl -v http://127.0.0.1:5000/getMemory
    
 or
 
    curl -v http://192.168.1.254:5000/getMemory

## Default flask

      export FLASK_ENV=development
