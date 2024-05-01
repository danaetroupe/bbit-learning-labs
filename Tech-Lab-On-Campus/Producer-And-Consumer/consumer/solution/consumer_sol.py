from consumer_interface import mqConsumerInterface

class mqConsumer(mqConsumerInterface):
    def _init_(self, routing_key: str, exchange_name: str, queue_name: str):
        mqConsumerInterface.__init__(self, routing_key, exchange_name, queue_name)