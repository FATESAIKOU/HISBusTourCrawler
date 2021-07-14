from abc import ABC, abstractmethod


class StorageInterface(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def downloadData(self, filename):
        pass

    @abstractmethod
    def uploadData(self, text, filename):
        pass
