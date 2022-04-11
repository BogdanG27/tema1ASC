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
        # call thread init
        Thread.__init__(self)

        # initialize the data
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        # set the name for the thread consX, X = cons number
        self.name = kwargs["name"]

    def run(self):
        prints = ""
        # for every cart of the client
        for cart in self.carts:
            # register a new cart in the marketplace
            cart_id = self.marketplace.new_cart()

            # for every operation in the cart
            for operation in cart:
                # check if it is add or remove
                if operation["type"] == "add":
                    i = 0
                    # wait until the product in the required quantity is available
                    while i < operation["quantity"]:
                        # add that amount to the cart
                        result = self.marketplace.add_to_cart(
                            cart_id, operation["product"])
                        # do not go to the next product until the current one is available
                        if not result:
                            sleep(self.retry_wait_time)
                            continue
                        i += 1
                elif operation["type"] == "remove":
                    # delete that amount of products from the cart
                    for _ in range(operation["quantity"]):
                        self.marketplace.remove_from_cart(
                            cart_id, operation["product"])

            # place the order
            products = self.marketplace.place_order(cart_id)

            # saved string to print them all at once
            for product in products:
                prints += f"{self.name} bought {product}\n"
        prints = prints[:-1]
        # use a lock to sinchronize the prints to not cause print errors
        with self.marketplace.order_lock:
            print(prints)
