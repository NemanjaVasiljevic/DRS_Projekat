from EngineAPI import app, cc
from EngineAPI.routes import transaction_process
import os
from multiprocessing import Process

if __name__ == '__main__':
    p = Process(target=transaction_process, args=(cc,))
    p.start()
    port=int(os.environ.get('PORT',5000))
    app.run(debug=True,port=port,host='0.0.0.0')