class Ovpn:
    def __init__(self, str):
        self.host, \
            self.ip, \
            score, \
            ping, \
            speed, \
            self.country_long, \
            self.country_short, \
            session_nums, \
            uptime, \
            total_user, \
            total_traffic, \
            self.logtype, \
            self.operator, \
            self.message, \
            self.ovpn_file = str.split(',')

        self.score = self.to_int(score)
        self.ping = self.to_int(ping)
        self.speed = self.to_int(speed)
        self.session_nums = self.to_int(session_nums)
        self.uptime = self.to_int(uptime)
        self.totoal_user = self.to_int(total_user)
        self.totoal_traffic = self.to_int(total_traffic)

        self.protocol = self.get_protocol()
        self.port = self.get_port()

    def to_int(self, str):
        try:
            r = int(str)
        except ValueError:
            r = -1
        return r

    def get_protocol(self):
        return None

    def get_port(self):
        return None

    def save_file(self, path=None):
        import os
        import base64
        with open(os.path.join(path, self.ip + '.ovpn'), 'wb') as ofile:
            num = ofile.write(base64.standard_b64decode(self.ovpn_file))
            ofile.close()
        return num

