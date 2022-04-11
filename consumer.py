"""
Ghitan Bogdan-Elvis-Dumitru
333CB
April 2022
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.name = kwargs["name"]

    def run(self):
        prints = ""
        for cart in self.carts:
            # Get a new shopping cart ID.
            cart_id = self.marketplace.new_cart()

            for operation in cart:
                # For every item, either add one to the cart or remove one.
                if operation["type"] == "add":
                    i = 0
                    while i < operation["quantity"]:
                        result = self.marketplace.add_to_cart(
                            cart_id, operation["product"])
                        # wait until product is available
                        if not result:
                            sleep(self.retry_wait_time)
                            continue
                        i += 1
                elif operation["type"] == "remove":
                    for _ in range(operation["quantity"]):
                        self.marketplace.remove_from_cart(
                            cart_id, operation["product"])

            products = self.marketplace.place_order(cart_id)

            for product in products:
                prints += f"{self.name} bought {product}\n"
        prints = prints[:-1]
        with self.marketplace.order_lock:
            print(prints)
