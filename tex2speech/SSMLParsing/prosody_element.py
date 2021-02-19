from SSMLParsing.ssml_element_node import SSMLElementNode
import xml.etree.ElementTree as ET

class ProsodyElement(SSMLElementNode):
    # Prosody Element Attribute Volume
    class Volume(SSMLElementNode):
        def __init__(self, volume = None):
            super().__init__()
            self.volumes = ['silent', '-6dB', '-5dB', '-4dB', '-3dB', '-2dB', '-1dB', '0dB', '-0dB', '+1dB', '+2dB', '+3dB', '+4dB', '+5dB', '+6dB']
            self.volumeIndex = {'silent': 0, '-6dB': 1, '-5dB': 2, '-4dB': 3, '-3dB': 4, '-2dB': 5, '-1dB': 6, '0dB': 7, '-0dB': 7, '+1dB': 8, '+2dB': 9, '+3dB': 10, '+4dB': 11, '+5dB': 12, '+6dB': 13}
            self._assignVolume(volume)

        def _assignVolume(self, value):
            if value in self.volumes:
                self.volume = volume
            else:
                if value == 'x-soft':
                    self.volume = '-6dB'
                elif value == 'soft':
                    self.volume = '-3dB'
                elif value == 'medium':
                    self.volume = '+0dB'
                elif value == 'loud':
                    self.volume = '+3dB'
                elif value == 'x-loud':
                    self.volume = '+6dB'

        def _mediumVolume(self, nestedVolume):
            mid = (self.volumeIndex[self.volume] + self.volumeIndex(nestedVolume))/2
            return self.volumes[mid]

    class Volume(SSMLElementNode):
        print("yo")
        def __init__(self, rate = None):
            super().__init__()

    class Volume(SSMLElementNode):
        print("yo")
        def __init__(self, pitch = None):
            super().__init__()

    class Volume(SSMLElementNode):
        print("yo")
        def __init__(self, duration = None):
            super().__init__()

    def _update(self):
        pass

    def _getXMLElement(self):
        pass

    def __str__(self):
        a = "ProsodyElement"
        if self.getHeadText() != "":
            a = '"' + self.getHeadText() + '"' + " " + a
        if self.getTailText() != "":
            a += " " + '"' + self.getTailText() + '"'
        return a

    __repr__ = __str__
