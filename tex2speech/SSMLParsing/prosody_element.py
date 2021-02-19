from SSMLParsing.ssml_element_node import SSMLElementNode
import xml.etree.ElementTree as ET

# Prosody for Volume attribute
class ProsodyElementVolume(SSMLElementNode):
    def __init__(self, volume = None):
        super().__init__()
        self.volume = self._assignVolume(volume)

    def _assignVolume(self, value):
        temp = ""
        if value[1].isnumeric():
            tempVal = value[:-1]
            temp= int(tempVal)
        else:
            if value == 'x-soft':
                temp = -6
            elif value == 'soft':
                temp= -3
            elif value == 'medium':
                temp = 0
            elif value == 'loud':
                temp= 3
            elif value == 'x-loud':
                temp = 6
        return temp

    def _mediumVolume(self, nestedVolume):
        mid = (self.volume + self._assignVolume(nestedVolume))/2

        if str(mid[0]) == '-':
            return mid + "dB"
        else:
            return "+" + mid + "dB"

    def _getVolume(self):
        if str(self.volume[0]) == '-': 
            return self.volume + "dB"
        else:
            return "+" + self.volume + "dB"

# Prosody for Rate attribute
class ProsodyElementRate(SSMLElementNode):
    def __init__(self, rate = None):
        super().__init__()
        self.rate = self._assignRate(rate);

    def _assignRate(self, rate):
        temp = ""
        if rate[0].isnumeric():
            tempVal = rate[:-1]

            # Rate is between 20% and 200%
            if tempVal > 200:
                temp = 200;
            elif tempVal < 20:
                temp = 20;
            else:
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
        mid = (self.rate + self._assignRate(nestedRate))/2;
        return str(mid) + "%"

    def _getRate(self):
        return self.rate + "%"


# Prosody for Pitch attribute
class ProsodyElementPitch(SSMLElementNode):
    def __init__(self, pitch = None):
        super().__init__()
        self.pitch = self._assignPitch(pitch);

    def _assignPitch(self, pitch):
        temp = ""
        if pitch[1].isnumeric():
            tempVal = pitch[:-1]
            temp= int(tempVal)
        else:
            if pitch == 'x-low':
                temp = -20
            elif pitch == 'low':
                temp = -10
            elif pitch == 'medium':
                temp = 0
            elif pitch == 'high':
                temp = 10
            elif pitch == 'x-high':
                temp = 20
        return temp

    def _mediumPitch(self, nestedPitch):
        mid = (self.pitch + self._assignRate(nestedPitch))/2;

        if mid[0] == '-':
            return str(mid) + "%"
        else:
            return "+" + str(mid) + "%"

    def _getPitch(self):
        if self.pitch[0] == '-':
            return self.pitch + "%"
        else:
            return "+" + self.pitch + "%"

# Prosody for Duration attribute
class ProsodyElementDuration(SSMLElementNode):
    def __init__(self, duration = None):
        super().__init__()
        self.duration = self._assignDuration(duration);

    def _assignDuration(self, duration):
        temp = ""

        if duration.length - 3 >=0:
            if duration[duration.length - 3].isnumeric():
                temp = duration[:-2]
            else:
                temp = duration[:-1] * 1000
        else:
            temp = duration[:-1] * 1000

        return temp

    def _mediumPitch(self, nestedDuration):
        mid = (self.duration + self._assignRate(nestedDuration))/2;
        return str(mid) + "ms"

    def _getDuration(self):
        return self.duration + "ms"

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
