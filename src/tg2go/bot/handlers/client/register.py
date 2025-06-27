from aiogram import Dispatcher

from tg2go.bot.handlers.client.callbacks import category, good, hub, item, panel
from tg2go.bot.handlers.client.callbacks.cart import cart, items, remove
from tg2go.bot.handlers.client.commands import start_order, start_register


def RegisterClientHandlers(dp: Dispatcher) -> None:
    dp.include_routers(
        # order matters
        start_order.router,
        start_register.router,
        panel.router,
        hub.router,
        category.router,
        good.router,
        item.router,
        cart.router,
        items.router,
        remove.router,
    )
