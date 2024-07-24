


class DD:
    
    def __init__(self, karyuku :int=0, reisou :int=0, luck :int=0, lv :int=0) -> None:
        self.__karyuku = karyuku
        self.__reisou = reisou
        self.__luck = luck
        self.__lv = lv
        
    @property
    def basic_attackpower(self):
        return self.