from API import app
import os

if __name__ == '__main__':
    port=int(os.environ.get('PORT',5001))
    app.run(debug=True,port=port,host='0.0.0.0')