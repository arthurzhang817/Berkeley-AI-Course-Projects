# shopSmart.py
# ------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    "*** YOUR CODE HERE ***"
    bestShop = ('',9999999999999999)

    for shop in fruitShops:
      priceList = shop.fruitPrices
      curCost = shop.getPriceOfOrder(orderList)
      if curCost < bestShop[1]:
        bestShop = (shop, curCost)
    return bestShop[0]
    
if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  order1 = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print "For orders ", order1, ", the best shop is", shopSmart(order1, shops).getName()
  order2 = [('apples',3.0)]
  print "For orders: ", order2, ", the best shop is", shopSmart(order2, shops).getName()


