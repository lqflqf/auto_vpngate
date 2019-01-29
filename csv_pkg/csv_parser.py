from csv_pkg.ovpn import Ovpn

class CSV_parser:
    path = None
    files = []

    def __init__(self):
        self.path = "http://www.vpngate.net/api/iphone/"
        self.open_remote()


    def open_remote(self):
        import urllib.request;
        with urllib.request.urlopen(self.path) as response:
            lines = response.read().decode("utf-8").split('\r\n')
        for ln in lines[2:-2]:
            self.files.append(Ovpn(ln))





