import logging
from dataclasses import dataclass


@dataclass
class BotState:
    active = True

    def Activate(self) -> None:
        self.active = True
        logging.info("Bot activated for clients")

    def Deactivate(self) -> None:
        self.active = False
        logging.info("Bot deactivated for clients")


bot_state = BotState()
