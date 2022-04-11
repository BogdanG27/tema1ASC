"""
Ghitan Bogdan-Elvis-Dumitru
333CB
April 2022
"""

from threading import Lock
import logging
from logging.handlers import RotatingFileHandler
import unittest


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        # dictionaires to keep data for producers and consumers"
        self.producers_products = {}
        self.consumers_carts = {}
        self.all_products = {}

        # used to generate ids for producers and consumers carts
        self.current_producer_id = 0
        self.current_cart_id = 0

        # locks
        self.producer_lock = Lock()
        self.cart_lock = Lock()
        self.order_lock = Lock()

        # setting up the locks
        logging.basicConfig(filename="marketplace.log", level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')

        self.logger = logging.getLogger()
        handler = RotatingFileHandler(
            "marketplace.log", maxBytes=0, backupCount=10)
        formatter = logging.Formatter(
            "[%(asctime)s] -  %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        handler.doRollover()
        self.logger.addHandler(handler)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        # we need a lock because incrementing is not thread-safe
        with self.producer_lock:
            # assign an id for every producer registered
            producer_id = self.current_producer_id
            self.current_producer_id += 1
            # assign a list of products for every producer
            self.producers_products[producer_id] = []
            # log the registered producer
            self.logger.info(f"Registered producer, id: {producer_id}")
            return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # add the product to the list
        self.producers_products[producer_id].append(product)
        # log the added product
        self.logger.info(
            f"Producer {producer_id} published {product.__str__()}")

        self.all_products[product] = producer_id
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        # we also need a lock because we increment
        with self.cart_lock:
            cart_id = self.current_cart_id
            self.current_cart_id += 1
            self.consumers_carts[cart_id] = []
            self.logger.info(f"Created new cart, id: {cart_id}")
            return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for id_producer in range(0, self.current_producer_id):
            if product in self.producers_products[id_producer]:
                self.consumers_carts[cart_id].append(product)
                self.producers_products[id_producer].remove(product)
                self.logger.info(
                    f"Added new product to the cart {cart_id}: {product.__str__()}")
                self.logger.info(
                    f"Removed product from producer {id_producer}: {product.__str__()}")

                return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        if product in self.consumers_carts[cart_id]:
            producer_id = self.all_products[product]

            self.producers_products[producer_id].append(product)
            self.consumers_carts[cart_id].remove(product)
            self.logger.info(
                f"Removed product {product.__str__()} from cart {cart_id}")
            self.logger.info(
                f"Added product {product.__str__()} back to producer {producer_id} stock")

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.logger.info(
            f"Order placed {self.consumers_carts[cart_id]} from cart {cart_id}")
        return self.consumers_carts[cart_id]


class TestMarketplace(unittest.TestCase):
    """
    Class for testing all the functionalities of the marketplace class
    """

    def setUp(self):
        """
        Set-up method, initializes the marketplace
        """
        self.marketplace = Marketplace(10)

    def test_register_product(self):
        rang = range(200)
        for i in rang:
            self.assertEqual(
                self.marketplace.register_producer(), i, "Not the expected id")

    def test_publish(self):
        producer_id = self.marketplace.register_producer()
        prod1 = {
            "product_type": "Coffee",
            "name": "Indonezia",
            "acidity": 5.05,
            "roast_level": "MEDIUM",
            "price": 1
        }.__str__()

        prod2 = {
            "product_type": "Tea",
            "name": "Wild Cherry",
            "type": "Black",
            "price": 5
        }.__str__()
        expected_list = [prod1, prod2]
        self.marketplace.publish(producer_id, prod1)
        self.marketplace.publish(producer_id, prod2)

        self.assertEqual(
            self.marketplace.producers_products[producer_id], expected_list,
            "Not the expected products")

    def test_new_cart(self):
        r = range(200)
        for i in r:
            self.assertEqual(
                self.marketplace.new_cart(), i, "Not the expected id")

    def test_add_to_cart(self):
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        prod1 = {
            "product_type": "Coffee",
            "name": "Indonezia",
            "acidity": 5.05,
            "roast_level": "MEDIUM",
            "price": 1
        }.__str__()

        prod2 = {
            "product_type": "Tea",
            "name": "Wild Cherry",
            "type": "Black",
            "price": 5
        }.__str__()

        self.marketplace.publish(producer_id, prod1)
        self.marketplace.publish(producer_id, prod2)

        self.marketplace.add_to_cart(cart_id=cart_id, product=prod1)

        # check for adding to cart
        self.assertEqual(self.marketplace.consumers_carts[cart_id], [
                         prod1], "Not the expected cart content")

        # check for removing from producer
        self.assertEqual(self.marketplace.producers_products[producer_id], [
                         prod2], "Not the expected cart content")

    def test_remove_from_cart(self):
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        prod1 = {
            "product_type": "Coffee",
            "name": "Indonezia",
            "acidity": 5.05,
            "roast_level": "MEDIUM",
            "price": 1
        }.__str__()

        prod2 = {
            "product_type": "Tea",
            "name": "Wild Cherry",
            "type": "Black",
            "price": 5
        }.__str__()

        self.marketplace.publish(producer_id, prod1)
        self.marketplace.publish(producer_id, prod2)

        self.marketplace.add_to_cart(cart_id=cart_id, product=prod1)

        self.marketplace.remove_from_cart(cart_id=cart_id, product=prod1)

        self.assertEqual(self.marketplace.consumers_carts[cart_id], [
        ], "Not the expected cart content")

        # check for removing from producer
        self.assertEqual(self.marketplace.producers_products[producer_id], [prod2,
                         prod1], "Not the expected cart content")

    def test_place_order(self):
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        prod1 = {
            "product_type": "Coffee",
            "name": "Indonezia",
            "acidity": 5.05,
            "roast_level": "MEDIUM",
            "price": 1
        }.__str__()

        prod2 = {
            "product_type": "Tea",
            "name": "Wild Cherry",
            "type": "Black",
            "price": 5
        }.__str__()

        self.marketplace.publish(producer_id, prod1)
        self.marketplace.publish(producer_id, prod2)

        self.marketplace.add_to_cart(cart_id=cart_id, product=prod1)
        cart = self.marketplace.consumers_carts[cart_id]
        order = self.marketplace.place_order(cart_id=cart_id)

        self.assertEqual(cart, order, "Not the expected order")
