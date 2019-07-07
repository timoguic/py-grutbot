import random
import requests

from .config import RAPID_API_KEY

class Webcam:
    RAPID_WEBCAM_API = "https://webcamstravel.p.rapidapi.com/webcams/list/bbox="
    
    def __new__(self, lat, lon):
        # https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
        bbox_lat_ne = lat + .3
        bbox_lat_sw = lat - .3
        bbox_lon_ne = lon + .3
        bbox_lon_sw = lon - .3
        bbox = (bbox_lat_ne, bbox_lon_ne, bbox_lat_sw, bbox_lon_sw)

        headers = {
            "X-RapidAPI-Host": "webcamstravel.p.rapidapi.com",
            "X-RapidAPI-Key": RAPID_API_KEY,
          }

        params = {
            'lang': 'fr',
            'show': 'webcams:image,location',
        }
        
        r = requests.get(self.RAPID_WEBCAM_API + ','.join([str(v) for v in bbox]), headers=headers, params=params)
        resp = r.json()
        if 'result' not in resp.keys():
            return {'webcam_location': False, 'webcam_img': False}

        if int(resp['result']['total']) < 1:
            return False
        else:
            webcams = resp['result']['webcams']
            chosen_cam = random.choice(webcams)
            loc = chosen_cam['title']
            img = chosen_cam['image']['current']['preview']
            return {'webcam_location': loc, 'webcam_img': img}

