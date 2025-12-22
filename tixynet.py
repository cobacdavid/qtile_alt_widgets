# tixynet.py

"""
Description: tixynet
Author: David COBAC
Date Created: December 19, 2025
Date Modified: December 22, 2025
Version: 1.0
Python Version: 3.13
Dependencies: 
License: GNU GPL Version 3
Repo: https://github.com/cobacdavid/my_qtile_widgets
"""

import math as _math
import socket as _socket

from libqtile.log_utils import logger
from libqtile.utils import send_notification
from libqtile.widget import base


def str2cairorgb(s):
    return tuple(int(s[2*i:2*i+2], 16) / 255 for i in range(3))


class Carre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._dim = None
        self._couleur = None

    @property
    def dim(self):
        return self._dim

    @dim.setter
    def dim(self, d):
        self._dim = d

    @property
    def couleur(self):
        return self._couleur

    @couleur.setter
    def couleur(self, c):
        self._couleur = str2cairorgb(c)

    def draw(self, ctx):
        ctx.save()
        ctx.translate(self.x - self.dim/2, self.y - self.dim/2)
        ctx.rectangle(0, 0, self.dim, self.dim)
        ctx.set_source_rgb(*self.couleur)
        ctx.fill()
        ctx.restore()


class Tixynet(base._Widget):
    defaults = [
        ("iface", "eth0", ""),
        ("iface_interval", 5, ""),
        ("inmargin", 2, ""),
        ("force_step", None, ""),
        ("pyfunc", lambda t, i, x, y: _math.sin(y/8+t), ""),
        ("update_interval", 1, ""),
        ("colors", ["ffffff", "ff0000"], ""),
        ("w", 20, ""),
        ("h", 10, "")
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)
        self.frame = 0
        self.etat = None

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        self.dimax = (self.bar.height - 2*self.inmargin) / self.h
        self.length = round(self.w * self.dimax
                            + 2*(self.inmargin + self.padding))
        self.myarray = [[Carre(col*self.dimax + self.dimax/2,
                               lig*self.dimax + self.dimax/2)
                         for col in range(self.w)]
                        for lig in range(self.h)]
        self.update_status()
        self._update()
        self.timeout_add(self.update_interval, self._tick)

    def _tick(self):
        self._update()
        self.timeout_add(self.update_interval, self._tick)

    def _update(self):
        if self.etat:
            if not self.force_step:
                self.frame += self.update_interval
            else:
                self.frame += self.force_step
        else:
            self.frame += 0
        self.bar.draw()

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        ctx = self.drawer.ctx
        ctx.translate(self.inmargin + self.padding, self.inmargin)
        n = self.w * self.h
        for i in range(n):
            x, y = i % self.w, i // self.w
            im = self.pyfunc(self.frame, i, x, y)
            self.myarray[y][x].couleur = self.colors[im < 0]
            self.myarray[y][x].dim = min(1, abs(im)) * self.dimax
            self.myarray[y][x].draw(ctx)
        self.draw_at_default_position()

    def update_status(self):
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        s.settimeout(1)

        try:
            s.setsockopt(_socket.SOL_SOCKET, 25, self.iface.encode())
            s.connect(("1.1.1.1", 443))
            self.etat = True
        except Exception:
            self.etat = False
        finally:
            s.close()

        self.timeout_add(self.iface_interval, self.update_status)
