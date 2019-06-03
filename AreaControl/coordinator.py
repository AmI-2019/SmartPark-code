import listener
import arrival


DBG = True
TD_ACport = 5001


"""
Sets parameters for the other modules
Launches listener.main()
"""
if __name__ == '__main__':
    listener.DBG = arrival.DBG = DBG
    arrival.TD_ACport = TD_ACport

    listener.main()
