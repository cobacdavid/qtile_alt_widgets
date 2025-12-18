# clock_alt.py

"""
Description: yet another clock
Author: David COBAC
Date Created: December 16, 2025
Date Modified: December 17, 2025
Version: 1.0
Python Version: 3.13
Dependencies: 
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/my_qtile_widgets
"""
from datetime import datetime

from libqtile.log_utils import logger
from libqtile.utils import send_notification
from libqtile.widget import base


class Clock_alt(base._Widget):
    defaults = [
        ("top_fmt", "%d/%m", ""),
        ("bot_fmt", "%H:%M", ""),
        ("gapy", 2, ""),
        ("rev", False, ""),
        ("hide_bot", False, ""),
    ]
    
    def __init__(self, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        self._update()
        self.timeout_add(1, self._tick)

    def _tick(self):
        self._update()
        self.timeout_add(1, self._tick)

    def _update(self):
        if not self.rev:
            self.txt_ht = datetime.now().strftime(self.top_fmt)
            self.txt_bs = datetime.now().strftime(self.bot_fmt)
        else:
            self.txt_ht = datetime.now().strftime(self.bot_fmt)
            self.txt_bs = datetime.now().strftime(self.top_fmt)
        self.bar.draw()

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        #
        ctx = self.drawer.ctx
        ctx.select_font_face(self.font)
        ctx.set_font_size(self.fontsize)
        xb_ht, yb_ht, w_ht, h_ht, xa_ht, ya_ht \
            = ctx.text_extents(self.txt_ht)
        if not self.hide_bot:
            ctx.set_font_size(self.fontsize - 10)
            xb_bs, yb_bs, w_bs, h_bs, xa_bs, ya_bs \
                = ctx.text_extents(self.txt_bs)
        else:
            xb_bs = yb_bs = w_bs = h_bs = xa_bs = ya_bs = 0
        #
        ctx.set_source_rgb(0, 0, 0)
        occup_x = max(w_ht, w_bs) + 2*self.padding
        occup_y = h_ht + self.gapy + h_bs
        xd, yd = (occup_x - w_ht) / 2, (self.bar.height - occup_y) / 2 + h_ht
        xt, yt = (occup_x - w_bs) / 2, yd + self.gapy + h_bs
        ctx.move_to(xd, yd)
        ctx.set_font_size(self.fontsize)
        ctx.show_text(self.txt_ht)
        ctx.move_to(xt, yt)
        if not self.hide_bot:
            ctx.set_font_size(self.fontsize - 10)
            ctx.show_text(self.txt_bs)
        #
        self.length = round(occup_x)
        self.draw_at_default_position()
