class pile:
    def __init__(self):
        self.data = []

    def pileUp(self, element) :
        self.data.append(element)

    def unstack(self):
        return self.data.pop()

    def isEmpty(self):
        return len(self.data)==0
        
    def hight(self):
        return len(self.data)

    def upperData(self):
        return self.data[-1]

    def pileUpAll(self, elements:list):
        for e in elements:
            self.pileUp(e)