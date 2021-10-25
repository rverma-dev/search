from enum import Enum

class BetType(Enum):
    CU = 'cu'
    GSI = 'gsi'

    def headers(self):
        switcher = {
            BetType.CU: ["bookId","gsiId","gsiName","cuNames"]
        }
        return switcher.get(self)
