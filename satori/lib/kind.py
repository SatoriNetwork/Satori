class HyperParameter:

    def __init__(
        self,
        name:str='n_estimators',
        value:'number'=3,
        limit:'number'=1,
        minimum:'number'=1,
        maximum:'number'=10,
        kind:'type'=int
    ):
        self.name = name
        self.value = value
        self.test = value
        self.limit = limit
        self.min = minimum
        self.max = maximum
        self.kind = kind