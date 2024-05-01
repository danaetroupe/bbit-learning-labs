from consumer_interface import mqConsumerInterface

class mqConsumer(mqConsumerInterface):
    def _init_(self, name):
        self.name = name
        mqConsumerInterface.setupRMQConnection(self)