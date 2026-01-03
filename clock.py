# clock.py

"""
Description: alternative clock
Author: David COBAC
Date Created: December 16, 2025
Date Modified: December 23, 2025
Version: 1.2
Python Version: 3.13
Dependencies:
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/qtile_alt_widgets

TODO:
- suppress rev and hide_bot attributes (for I now use state)
"""
from datetime import datetime

from libqtile.log_utils import logger
from libqtile.utils import send_notification
from libqtile.widget import base


def str2cairorgb(s):
    return tuple(int(s[2*i:2*i+2], 16) / 255 for i in range(3))


class Clock(base._Widget):
    defaults = [
        ("fmts", ["%d/%m", "%H:%M"], "display formats"),
        ("fontsizes", None, "adjust manually font sizes"),
        ("gapy", 2, "vertical space (in pixels) between displays"),
        ("state", 0, "display state: 0, 1, 2 or 3"),
        ("text_colors", ["000000", "000000"], "")
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)
        self.fmt1, self.fmt2 = self.fmts
        self.add_callbacks({"Button1": self.inc_state,
                            "Button3": self.dec_state})

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        if self.fontsizes is not None:
            self.fsizes = self.fontsizes
        else:
            self.fsizes = [self.fontsize, self.fontsize * .5]
        self._update()
        self.timeout_add(1, self._tick)

    def inc_state(self):
        self.state = (self.state + 1) % 4
        self._update()
        self.bar.draw()

    def dec_state(self):
        self.state = (self.state - 1) % 4
        self._update()
        self.bar.draw()

    def _tick(self):
        self._update()
        self._timer = self.timeout_add(1, self._tick)

    def _update(self):
        self.rev = self.state & 1
        self.hide_bot = self.state >> 1

        if not self.rev:
            self.txt_ht = datetime.now().strftime(self.fmt1)
            self.txt_bs = datetime.now().strftime(self.fmt2)
        else:
            self.txt_ht = datetime.now().strftime(self.fmt2)
            self.txt_bs = datetime.now().strftime(self.fmt1)
        self.draw()

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        #
        ctx = self.drawer.ctx
        ctx.select_font_face(self.font)
        ctx.set_font_size(self.fsizes[0])
        xb_ht, yb_ht, w_ht, h_ht, xa_ht, ya_ht \
            = ctx.text_extents(self.txt_ht)
        # yb_ht + h_ht = pixels en bas de la ligne
        if not self.hide_bot:
            ctx.set_font_size(self.fsizes[1])
            xb_bs, yb_bs, w_bs, h_bs, xa_bs, ya_bs \
                = ctx.text_extents(self.txt_bs)
        else:
            xb_bs = yb_bs = w_bs = h_bs = xa_bs = ya_bs = 0
        #
        ctx.set_source_rgb(*str2cairorgb(self.text_colors[0]))
        occup_x = max(w_ht, w_bs) + 2*self.padding
        occup_y = (h_ht + (yb_ht + h_ht)) + self.gapy + (h_bs + (yb_bs + h_bs))
        xd, yd = (occup_x - w_ht) / 2, (self.bar.height - occup_y) / 2 + h_ht
        xt, yt = (occup_x - w_bs) / 2, yd + (yb_ht + h_ht) + self.gapy + h_bs
        ctx.move_to(xd, yd)
        ctx.set_font_size(self.fsizes[0])
        ctx.show_text(self.txt_ht)
        ctx.move_to(xt, yt)
        if not self.hide_bot:
            ctx.set_source_rgb(*str2cairorgb(self.text_colors[1]))
            ctx.set_font_size(self.fsizes[1])
            ctx.show_text(self.txt_bs)
        #
        self.length = round(occup_x)
        self.draw_at_default_position()

    def finalize(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None
        base._Widget.finalize(self)
