


from django.db import transaction

from django.shortcuts import get_object_or_404

from portfolios.models import Position, Transaction


class InsufficientQuantityError(Exception):
    pass


def calculate_average_price( current_quantity, current_average_price, new_quantity, new_price):
    """
    Calculate the new average price after a buy transaction.

    :param current_quantity: The current quantity of the asset in the position.
    :param current_average_price: The current average price of the asset in the position.
    :param new_quantity: The quantity of the asset being bought.
    :param new_price: The price at which the asset is being bought.
    :return: The new average price after the transaction.
    """
    if current_quantity + new_quantity == 0:
        return 0  # Avoid division by zero
    total_cost = (current_average_price * current_quantity) + (new_price * new_quantity)
    return total_cost / (current_quantity + new_quantity)

@transaction.atomic
def buy_positions(portfolio, asset, quantity, price, idempotency_key):
    """
    Handle the logic for buying positions in a portfolio.

    :param portfolio: The portfolio in which the asset is being bought.
    :param asset: The asset being bought.
    :param quantity: The quantity of the asset being bought.
    :param price: The price at which the asset is being bought.
    """
    
    position, created = Position.objects.select_for_update().get_or_create(
        portfolio=portfolio,
        asset=asset,
        defaults={"quantity": quantity, "average_price": price},
    )
    if not created:
        # Update the existing position
        new_average_price = calculate_average_price(
            position.quantity, position.average_price, quantity, price
        )
        position.quantity += quantity
        position.average_price = new_average_price
        position.save()
        
    purchase = Transaction.objects.create(
        asset=asset,
        type='buy',
        portfolio=portfolio,
        quantity=quantity,
        price=price,
        idempotency_key=idempotency_key
    )
    return purchase



@transaction.atomic
def sell_positions(portfolio, asset, quantity, price, idempotency_key):
    """
    Handle the logic for selling positions in a portfolio.

    :param portfolio: The portfolio from which the asset is being sold.
    :param asset: The asset being sold.
    :param quantity: The quantity of the asset being sold.
    :param price: The price at which the asset is being sold.
    """
    
    position = get_object_or_404(Position.objects.select_for_update(), 
                            portfolio=portfolio,
                            asset=asset,
                        )
    
    if quantity > position.quantity:
        raise InsufficientQuantityError("Selling quantity cannot exceed current position quantity.")
    
    position.quantity -= quantity
    if position.quantity == 0:
        position.delete()
    else:
        position.save()
    
    sale = Transaction.objects.create(
        asset=asset,
        type='sell',
        portfolio=portfolio,
        quantity=quantity,
        price=price,
        idempotency_key=idempotency_key
    )
    
    return sale