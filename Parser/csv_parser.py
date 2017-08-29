from Parser.ovpn import Ovpn

class CSV_parser:
    path = None
    file = None
    filter = None

    def __init__(self):
        self.path = "http://www.vpngate.net/api/iphone/"


    def open_remote(self):
        import urllib.request;
        with urllib.request.urlopen(self.path) as response:
            lines = response.read().decode("utf-8").split('\r\n')
        ofiles = []
        for i in lines[2:-2]:
            ofiles.append(i)
        return ofiles


# csv = CSV_parser()
# files = csv.open_remote()
# print(len(files))

