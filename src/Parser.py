import re


class Parser:

    def __init__(self, data, d):
        self.nodes = {}
        self.diseq = []
        self.eq = []
        self.parse_data(data, d)

    def parse(self, data):
        return