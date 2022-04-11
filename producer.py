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
        Thread.__init__(self, daemon=kwargs["daemon"])
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        producer_id = self.marketplace.register_producer()

        while True:
            for (product, quantity, production_time) in self.products:
                # Produce item:
                sleep(production_time)

                i = 0
                while i < quantity:
                    # Publish each item separately:
                    if not self.marketplace.publish(producer_id, product):
                        # Publishing failed, retry after a timeout:
                        sleep(self.republish_wait_time)
                        continue
                    i += 1
