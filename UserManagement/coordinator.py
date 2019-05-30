import web
import REST
import threading


DBG: bool = True
# The port for the REST interface exposed by the UMS to the TDS
UM_TDport = 5000
# The port for the Website exposed by the UMS
UM_WEBport = 5003


if __name__ == '__main__':
    webThread = threading.Thread(target=web.main, args=(UM_WEBport,))
    RESTThread = threading.Thread(target=REST.main, args=(UM_TDport,))

    web.DBG = REST.DBG = DBG

    webThread.start()
    RESTThread.start()

    webThread.join()
    RESTThread.join()