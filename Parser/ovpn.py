class Ovpn:
    def __init__(self, str):

        self.host, \
            self.ip, \
            self.score, \
            self.ping, \
            self.speed, \
            self.country_long, \
            self.country_short, \
            self.session_nums, \
            self.uptime, \
            self.total_user, \
            self.total_traffic, \
            self.logtype, \
            self.operator, \
            self.message, \
            self.ovpn_file = str.split(',')
