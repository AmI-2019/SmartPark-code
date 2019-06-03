import requests
import base64
import json
from functions import cam_init,getpicture
image_path = "esempio_1.jpg"
camera_path = "campic.jpg"
secret_key = "sk_ac131f0dc212d58f2ed6e288"
camera = cam_init()
pic = getpicture(camera,camera_path)
camera.release()
with open(camera_path,"rb") as image:
    image_b64 = base64.b64encode(image.read())
url = "https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=0&country=eu&secret_key=%s" % (secret_key)
request = requests.post(url, data=image_b64)
plate_data_str = json.dumps(request.json(),indent=2)
plate_data_dic = json.loads(plate_data_str)
plate_number = plate_data_dic["results"][0]["plate"]
print("La targa è: "+plate_number)