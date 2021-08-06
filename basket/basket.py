from decimal import Decimal

from checkout.models import DeliveryOptions
from django.conf import settings
from store.models import Animal


class Basket:
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, animal, qty):
        """
        Adding and updating the users basket session data
        """
        animal_id = str(animal.id)

        if animal_id in self.basket:
            self.basket[animal_id]["qty"] = qty
        else:
            self.basket[animal_id] = {"price": str(animal.regular_price), "qty": qty}

        self.save()

    def __iter__(self):
        """
        Collect the animal_id in the session data to query the database
        and return animals
        """
        animal_ids = self.basket.keys()
        animals = Animal.objects.filter(id__in=animal_ids)
        basket = self.basket.copy()

        for animal in animals:
            basket[str(animal.id)]["animal"] = animal

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item["qty"] for item in self.basket.values())

    def update(self, animal, qty):
        """
        Update values in session data
        """
        animal_id = str(animal)
        if animal_id in self.basket:
            self.basket[animal_id]["qty"] = qty
        self.save()

    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def get_total_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    def delete(self, animal):
        """
        Delete item from session data
        """
        animal_id = str(animal)

        if animal_id in self.basket:
            del self.basket[animal_id]
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        del self.session["address"]
        del self.session["purchase"]
        self.save()

    def save(self):
        self.session.modified = True
