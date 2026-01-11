# click_coords.py

"""
Description: A script to add click position to widget (with ChatGPT)
Author: David COBAC
Date Created: January 11, 2026
Date Modified: January 11, 2026
Version: 1.0
Python Version: 3.13
Dependencies: aiohttp, colormaps
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/qtile_alt_widgets
"""

from libqtile.log_utils import logger
from libqtile.utils import send_notification


class Click_coords_mixin:
    """
    Mixin pour widgets Qtile fournissant les coordonnées
    locales (widget) lors d'un clic Button1.
    """

    def __init__(self, *args, **kwargs):
        self._click_handler = None
        super().__init__(*args, **kwargs)

    def set_click_handler(self, handler):
        """
        handler(x, y)
        """
        self._click_handler = handler

    def button_press(self, x, y, button):
        if button == 1 and self._click_handler:
            # x, y sont DÉJÀ relatifs au widget
            self._click_handler(x, y)
        # Important : laisser Qtile continuer la chaîne
        return super().button_press(x, y, button)
