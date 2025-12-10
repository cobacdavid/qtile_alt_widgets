# ghcw.py

"""
Description: A Github contribution widget for Qtile
Author: David COBAC
Date Created: December 6, 2025
Date Modified: December 10, 2025
Version: 1.0
Python Version: 3.13
Dependencies: aiohttp, libqtile
License: GNU GPL Version 3
"""

import asyncio
import webbrowser
from datetime import datetime, timedelta

import aiohttp
from libqtile.widget import base


class Contrib_day:
    def __init__(self, x, y, dim, couleur):
        self.x = x
        self.y = y
        self.dim = dim
        self.couleur = couleur

    def draw(self, ctx):
        ctx.save()
        ctx.translate(self.x, self.y)
        ctx.rectangle(0, 0, self.dim - 1, self.dim - 1)
        ctx.set_source_rgb(*self.couleur)
        ctx.fill()
        ctx.restore()


class Ghcw(base._Widget):
    defaults = [
        ("idgithub", "cobacdavid", ""),
        ("gap", 1, ""),
        ("nweeks", 52, ""),
        ("colors",
         [(.1, .1, .1)] + [(0, .2*i, 0) for i in range(1, 6)],
         "")
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)
        # en faisant un fill on perd le pixel du stroke
        self.gap -= 1
        # tâche asynchrone pour récupérer les données en API
        self._tab_donnees = None
        asyncio.create_task(self.async_init())
        self.add_callbacks({"Button1": self.to_user_webpage})

    def to_user_webpage(self):
        url = f"https://github.com/{self.idgithub}"
        webbrowser.open(url)

    async def async_init(self):
        """Partie asynchrone de l'init."""
        data = await self.fetch_contribs()
        self._tab_donnees = data
        # dessine le widget et met à jour la barre
        self.draw()
        self.bar.draw()

    async def fetch_contribs(self):
        url = f"https://github-contributions.vercel.app/api/v1/{self.idgithub}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                res = await resp.json()

        today = datetime.today()

        i = 0
        while datetime.fromisoformat(res['contributions'][i]['date']) > today:
            i += 1

        tab_donnees = []
        for j in range(i, i + 7 * self.nweeks):
            d = res["contributions"][j]
            tab_donnees.append((d["date"], d["intensity"]))

        # prepend empty days to align week
        missing = 6 - today.weekday()
        for k in range(missing):
            tab_donnees.insert(
                0,
                ((today + timedelta(days=k+1)).isoformat()[:10], 0)
            )
        return tab_donnees[:7 * self.nweeks]

    def draw(self):
        if self._tab_donnees is None:
            # avant réception des données
            self.drawer.clear(self.background or self.bar.background)
            self.length = 0
            self.draw_at_default_position()
            return

        self.dim = (self.bar.height - 8 * self.gap) // 7
        lgth = self.nweeks * (self.dim + self.gap) + self.gap

        self.drawer.clear(self.background or self.bar.background)
        ctx = self.drawer.ctx
        ctx.scale(-1, -1)
        ctx.translate(-lgth, -self.bar.height)

        for col in range(self.nweeks):
            for lig in range(7):
                intensity = self._tab_donnees[col * 7 + lig][1]
                couleur = self.colors[min(5, int(intensity))]
                Contrib_day(
                    self.gap * (col + 1) + col * self.dim,
                    self.gap * (lig + 1) + lig * self.dim,
                    self.dim, couleur
                ).draw(ctx)

        self.length = lgth
        self.draw_at_default_position()
