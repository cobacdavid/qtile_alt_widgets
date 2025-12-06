# ghcw.py

"""
Description: A Github contribution widget for Qtile
Author: David COBAC
Date Created: December 6, 2025
Date Modified: June 10, 2023
Version: 1.0
Python Version: 3.13
Dependencies: libqtile
License: GNU GPL Version 3
"""

from datetime import datetime, timedelta

import requests
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
        ctx.rectangle(0, 0, self.dim-1, self.dim-1)
        ctx.set_source_rgb(*self.couleur)
        ctx.fill()
        ctx.restore()


class Ghcw(base._Widget):

    defaults = [("idgithub", "cobacdavid", ""),
                ("nweeks", 20, ""),
                ("colors",
                 [(.1, .1, .1)] + [(0, .2*i, 0) for i in range(1, 6)],
                 "")]

    def __init__(self, **config):
        base._Widget.__init__(self, length=0, **config)
        self.add_defaults(self.defaults)
        self._tab_donnees = self.tab_donnees(self.idgithub, self.nweeks)

    def draw(self):
        # calcul de la dimension des carrés en fonction de la
        # hauteur de la barre. À faire : laisser l'utilisateur
        # gérer l'espace entre deuxc carrés
        self.espace = 1
        self.dim = (self.bar.height - 8) // 7
        lgth = self.nweeks * (self.dim + self.espace) + self.espace
        self.drawer.clear(self.background or self.bar.background)
        ctx = self.drawer.ctx
        # on reste cohérent avec la version originale
        ctx.scale(-1, -1)
        ctx.translate(-lgth, -self.bar.height)
        #
        for col in range(self.nweeks):
            for lig in range(7):
                intensity = self._tab_donnees[col * 7 + lig][1]
                couleur = self.colors[min(5, int(intensity))]
                Contrib_day(self.espace * (col + 1) + col * self.dim,
                            self.espace * (lig + 1) + lig * self.dim,
                            self.dim, couleur).draw(ctx)
                # on réajuste le widget en longueur
        self.length = lgth
        self.draw_at_default_position()

    @staticmethod
    def tab_donnees(idgithub, nweeks):
        url = f"https://github-contributions.vercel.app/api/v1/{idgithub}"
        res = requests.get(url)
        today = datetime.today()
        # on attend d'arriver à la date du jour
        i = 0
        while (datetime.fromisoformat(res.json()['contributions'][i]['date'])
               > today):
            i += 1
            # on ajoute autant de jours que demandé par nweeks
        tab_donnees = []
        for j in range(i, i + 7 * nweeks):
            dico_jour = res.json()["contributions"][j]
            date = dico_jour['date']
            intensity = dico_jour['intensity']
            tab_donnees.append((date, intensity))
            # on ajoute les jours suivants de notre semaine
        a_ajouter = 6 - today.weekday()
        for i in range(a_ajouter):
            tab_donnees.insert(0, ((today
                                    + timedelta(days=i+1)).isoformat()[:10], 0))
            # on supprime les jours précédents en trop (vu qu'on en a ajoutés)
        return tab_donnees[:7*nweeks]
