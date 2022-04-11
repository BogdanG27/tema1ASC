"""
Ghitan Bogdan-Elvis-Dumitru
333CB
April 2022
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        # call thread.init with the daemon
        Thread.__init__(self, daemon=kwargs["daemon"])
        # initialize the attributes
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        # register a producer
        producer_id = self.marketplace.register_producer()

        # produce until all the consumers finish their orders
        while True:
            # for every product the producer has on it's list
            for (product, quantity, production_time) in self.products:
                # wait for production time
                sleep(production_time)

                # put it on the list
                i = 0
                while i < quantity:
                    if not self.marketplace.publish(producer_id, product):
                        sleep(self.republish_wait_time)
                        continue
                    i += 1
