import area
import choice
import listener
import spots
import arrival
import threading


DBG: bool = True
# The port for the REST interface exposed by the UMS to the TDS
UM_TDport = 5000
# The port for the REST interface exposed by the TDS to the ACS
TD_ACport = 5001
# The port for the Website exposed to the TS
TD_TSport = 5002


if __name__ == '__main__':
    listenerThread = threading.Thread(target=listener.main)
    areaThread = threading.Thread(target=area.main, args=(TD_ACport,))
    choiceThread = threading.Thread(target=choice.main, args=(TD_TSport,))

    listener.DBG = spots.DBG = area.DBG = arrival.DBG = choice.DBG = DBG
    spots.initMap()
    arrival.UM_TDport = UM_TDport

    listenerThread.start()
    areaThread.start()
    choiceThread.start()

    listenerThread.join()
    areaThread.join()
    choiceThread.join()
