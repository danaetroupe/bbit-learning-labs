# Copyright 2024 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pika
import os

class mqConsumerInterface:
    def __init__(
        self, routing_key: str, exchange_name: str, queue_name: str
    ) -> None:
        # Save parameters to class variables
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        
        # Call setupRMQConnection
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        conParams = pika.URLParameters(os.environ[self.routing_key])
        self.connection = pika.BlockingConnection(parameters=conParams)

        # Establish Channel
        self.channel = self.connection.channel()
        
        # Create Queue if not already present
        if not self.queue:
            self.queue = self.channel.queue_declare(queue=self.queue_name)
        
        # Create the exchange if not already present
        if not self.exchange:
            self.exchange = self.channel.exchange_declare(self.exchange_name)

        # Bind Binding Key to Queue on the exchange
        self.channel.queue_bind(
            queue = self.queue_name,
            routing_key = self.routing_key,
            exchange = self.exchange_name
        )
    # Set-up Callback function for receiving messages
        self.channel.basic_consume(
            self.queue_name, self.on_message_callback, auto_ack=False
        )
    
    def on_message_callback(
        self, method_frame, header_frame, body
    ) -> None:
        # Acknowledge message
        self.channel.basic_ack(method_frame.delivery_tag, False)
        self.channel.basic_ack(header_frame.delivery_tag, False)
        
        #Print message (The message is contained in the body parameter variable)
        print(body)

    def startConsuming(self) -> None:
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        print('[*] Waiting for messages. To exit press CTRL+C')
        
        # Start consuming messages
        self.channel.start_consuming()
    
    def __del__(self) -> None:
        # Print "Closing RMQ connection on destruction"
        print('[*] Closing RMQ connection on destruction.')
        
        # Close Channel
        self.channel.close()
        
        # Close Connection
        self.connection.close()
