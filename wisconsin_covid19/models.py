class CovidData:
    def __init__(self, data):
        self.__dict__.update(data)

    def __repr__(self):
        return str(self.__dict__)