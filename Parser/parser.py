class Parser:
    file_path = None
    file = None
    filter = None

    def __init__(self):
        self.file_path = "http://www.vpngate.net/api/iphone/"


    def open_remote(self):
        import urllib.request;
        with urllib.request.urlopen(self.file_path) as response:
            self.file = response.read().decode("utf-8")
        print(self.file)


    def open_local(self, file_path):
        import csv;
        with open(file_path, newline='') as csvfile:
            self.file = csv.reader(csvfile)

rf = Parser()
rf.open_remote()
