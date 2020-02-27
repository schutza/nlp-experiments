from abc import ABC, abstractmethod

class DialogActDetector(ABC):
    
    @abstractmethod
    def detect(self, input, language):
        pass
