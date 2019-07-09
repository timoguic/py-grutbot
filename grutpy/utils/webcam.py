import random
import requests

from .config import RAPID_API_KEY


class Webcam:
    RAPID_WEBCAM_API = "https://webcamstravel.p.rapidapi.com/webcams/list/bbox="

    def __new__(self, coords):
        if type(coords) == tuple and len(coords) == 2:
            lat = coords[0]
            lon = coords[1]

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            raise AttributeError("Please call with tuple(lat, lon) containing floats.")

        return self._get_data(lat, lon)

    @classmethod
    def _get_data(cls, lat, lon):
        # https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
        bbox_lat_ne = lat + 0.3
        bbox_lat_sw = lat - 0.3
        bbox_lon_ne = lon + 0.3
        bbox_lon_sw = lon - 0.3
        bbox = (bbox_lat_ne, bbox_lon_ne, bbox_lat_sw, bbox_lon_sw)

        headers = {
            "X-RapidAPI-Host": "webcamstravel.p.rapidapi.com",
            "X-RapidAPI-Key": RAPID_API_KEY,
        }

        params = {"lang": "fr", "show": "webcams:image,location"}

        r = requests.get(
            cls.RAPID_WEBCAM_API + ",".join([str(v) for v in bbox]),
            headers=headers,
            params=params,
        )
        resp = r.json()
        if "result" not in resp.keys():
            return False

        if int(resp["result"]["total"]) < 1:
            return False
        else:
            webcams = resp["result"]["webcams"]
            chosen_cam = random.choice(webcams)
            loc = chosen_cam["title"]
            img = chosen_cam["image"]["current"]["preview"]
            return {"location": loc, "img": img}
