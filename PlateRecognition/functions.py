import cv2
def getpicture(camera,path):
    ret,frame = camera.read()
    cv2.imwrite(path,frame)
    return frame
def cam_init():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Webcam not found")

    return cam