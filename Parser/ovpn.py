import base64

class Ovpn:

    line_spliter = '\r\n'

    def __init__(self, input_str):
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
            ovpn_file = input_str.split(',')

        self.score = self.to_int(score)
        self.ping = self.to_int(ping)
        self.speed = self.to_int(speed)
        self.session_nums = self.to_int(session_nums)
        self.uptime = self.to_int(uptime)
        self.totoal_user = self.to_int(total_user)
        self.totoal_traffic = self.to_int(total_traffic)
        self.ovpn_file = str(base64.standard_b64decode(ovpn_file), 'utf-8')

        self.protocol = self.get_protocol()
        self.port = self.get_port()

        self.file_name = self.country_short + '_' + self.ip + '_' + self.protocol + '_' + str(self.port) + '.ovpn'

    def to_int(self, str):
        try:
            r = int(str)
        except ValueError:
            r = -1
        return r

    def get_protocol(self):
        return next(filter(lambda s: s.find('proto') == 0, self.ovpn_file.split(self.line_spliter))).split(' ')[1]

    def get_port(self):
        return self.to_int(next(filter(lambda s: s.find('remote') == 0, self.ovpn_file.split(self.line_spliter))).split(' ')[2])

    def save_file(self, path=None):
        import os
        with open(os.path.join(path, self.file_name), 'w') as ofile:
            num = ofile.write(self.ovpn_file)
            ofile.close()
        return num

