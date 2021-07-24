class Result:
    def __init__(self, json: dict):
        self.__dict__ = json
        for key in self.__dict__:
            if isinstance(self.__dict__[key], dict):
                self.__dict__[key] = Result(self.__dict__[key])
            if isinstance(self.__dict__[key], list):
                for i in range(len(self.__dict__[key])):
                    if isinstance(self.__dict__[key][i], dict):
                        self.__dict__[key][i] = Result(self.__dict__[key][i])

    def __repr__(self):
        return str(self.__dict__)
