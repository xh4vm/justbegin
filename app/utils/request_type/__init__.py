from abc import ABCMeta, abstractmethod


class IRequestType:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self) -> dict:
        '''Получение параметров'''
    
