from SSMLParsing.ssml_element_node import SSMLElementNode
import xml.etree.ElementTree as ET

# Prosody for Volume attribute
class ProsodyElementVolume(SSMLElementNode):
    def __init__(self, volume = None):
        super().__init__()
        self.volumes = ['silent', '-6dB', '-5dB', '-4dB', '-3dB', '-2dB', '-1dB', '0dB', '-0dB', '+1dB', '+2dB', '+3dB', '+4dB', '+5dB', '+6dB']
        self.volumeIndex = {'silent': 0, '-6dB': 1, '-5dB': 2, '-4dB': 3, '-3dB': 4, '-2dB': 5, '-1dB': 6, '0dB': 7, '-0dB': 7, '+1dB': 8, '+2dB': 9, '+3dB': 10, '+4dB': 11, '+5dB': 12, '+6dB': 13}
        self.volume = self._assignVolume(volume)

    def _assignVolume(self, value):
        temp = ""
        if value in self.volumes:
            temp = value
        else:
            if value == 'x-soft':
                temp = '-6dB'
            elif value == 'soft':
                temp= '-3dB'
            elif value == 'medium':
                temp = '+0dB'
            elif value == 'loud':
                temp= '+3dB'
            elif value == 'x-loud':
                temp = '+6dB'
        return temp

    def _mediumVolume(self, nestedVolume):
        mid = (self.volumeIndex[self.volume] + self.volumeIndex(self._assignVolume(nestedVolume)))/2
        return self.volumes[mid]

    def _getVolume(self):
        return self.volume

# Prosody for Rate attribute
class ProsodyElementRate(SSMLElementNode):
    def __init__(self, rate = None):
        super().__init__()
        self.rate = self._assignRate(rate);

    def _assignRate(self, rate):
        temp = ""
        if rate[0].isnumeric():
            tempVal = rate[:-1]
            temp= int(tempVal)
        else:
            if rate == 'x-slow':
                temp = 60
            elif rate == 'slow':
                temp = 80
            elif rate == 'medium':
                temp = 100
            elif rate == 'fast':
                temp = 120
            elif rate == 'x-fast':
                temp = 140
        return temp

    def _mediumRate(self, nestedRate):
        mid = (self.volumeIndex[self.rate] + self._assignRate(nestedRate))/2;
        return str(mid) + "%"

    def _getVRate(self):
        return self.rate


# Prosody for Pitch attribute
class ProsodyElementPitch(SSMLElementNode):
    print("yo")
    def __init__(self, pitch = None):
        super().__init__()

# Prosody for Duration attribute
class ProsodyElementDuration(SSMLElementNode):
    print("yo")
    def __init__(self, duration = None):
        super().__init__()

    # def _update(self):
    #     pass

    # def _getXMLElement(self):
    #     pass

    # def __str__(self):
    #     a = "ProsodyElement"
    #     if self.getHeadText() != "":
    #         a = '"' + self.getHeadText() + '"' + " " + a
    #     if self.getTailText() != "":
    #         a += " " + '"' + self.getTailText() + '"'
    #     return a

    # __repr__ = __str__
