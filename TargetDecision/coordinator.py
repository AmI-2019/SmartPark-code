import listener, area, spots, choice, threading


if __name__ == '__main__':
    listenerThread = threading.Thread(target=listener.main)
    areaThread = threading.Thread(target=area.main)
    choiceThread = threading.Thread(target=choice.main)

    spots.initMap()
    listenerThread.start()
    areaThread.start()
    choiceThread.start()

    listenerThread.join()
    areaThread.join()
    choiceThread.join()