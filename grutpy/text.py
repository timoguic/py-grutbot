from .utils import Parser, Search
from .utils.weather import Weather


class CliApp:
    def run(self):
        while True:
            val = input("Phrase?\n")
            if val == "q":
                break
            parsed = Parser(val)
            if not parsed:
                print("Cannot parse", val)
            else:
                print(val, "=>", parsed)
                search = Search(parsed).process()
                lat = search["coords"][0]
                lon = search["coords"][1]
                weather = Weather(lat=lat, lon=lon)
                print(weather)
                print(search["coords"], "-", search["wiki_extract"][0:50])


app = CliApp()
