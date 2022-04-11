# tema1ASC
Ghitan Bogdan-Elvis-Dumitru, 333CB

--------------------------------------------------------------------------
Opinion

Actually ok homework, quite easy to implement, few concurrency problems to
consider and fix. I think it was useful, getting to understand how threads
work in python

I consider my implementation to be decent, I think it could've been done
with a little more caution, but I'm pleased with the result/

--------------------------------------------------------------------------
Implementation

The implementation is based on the skel we received, containing 4 main
classes:
  -> Consumer
  -> Producer
  -> Product
  -> Marketplace

--------------------------------------------------------------------------
Product class:
Already implemented in skel, no need to make changes. I honestly don't see
the point of it, as it is not used anywhere, not even in test.py.

--------------------------------------------------------------------------
Producer class:
Used to manufacture products for the consumers.
Every product has a production time and every producer has a republish time.
Products are pushed constantly to the list.

--------------------------------------------------------------------------
Consumer class:
Used to add products to their carts and place orders.
Their products are added to the carts as long as they are available from the
producer. If not available, they have to wait until a new product of that
kind is introduced for sale.
The consumers can also remove products from their carts, then the products
removed are added back for sale for the consumer.

--------------------------------------------------------------------------
Marketplace class:
Is actually a middleman that assists all the operations made by producers
and consumers. It facilitates the whole process. Producers can be
registered and can publish their products, consumers can create new carts,
can add products to their carts, remove products from their carts and place
orders.

--------------------------------------------------------------------------
The unittesting class is used to test all the methods from marketplace
class.

--------------------------------------------------------------------------
Concurrency and problems:
There were few concurrencies that needed to be synchronized, such as
registering a new producer or a cart, where an id was needed and using an
incrementation is not thread safe, so a lock was required.
Also, I used a lock when printing the results, as stdout is a shared
resource, so many threads could print at the same time.

I also encountered a deadlock at test no. 10, some consumers were trying
to add an unavailable product to the cart and the producers could not
republish it because the limit was registered. So I removed the limit
for the amount of products that could be on the list at a certain time
