import math as _math

import colormaps as _cmaps

# import cairo as _cairo


def str2cairorgb(s):
    return tuple(int(s[2*i:2*i+2], 16) / 255 for i in range(3))


class Petal_pbar:
    def __init__(self, rmin, rmax, offset_rayon, angle_deg, angle_rond_deg):
        self.rmin = rmin
        self.rmax = rmax
        self.offset_rayon = offset_rayon
        self.angle_deg = angle_deg
        self.angle_rond_deg = angle_rond_deg

    def draw(self, ctx):
        if self.angle_rond_deg > self.angle_deg / 2:
            return
        if self.offset_rayon > (self.rmax - self.rmin) / 2:
            return
        #
        cosinus = _math.cos(_math.radians(self.angle_deg / 2))
        sinus = _math.sin(_math.radians(self.angle_deg / 2))
        pAngle = _math.radians(self.angle_deg/2 - self.angle_rond_deg)
        cpAngle = _math.cos(pAngle)
        spAngle = _math.sin(pAngle)
        #
        p1 = (self.rmin * cpAngle, self.rmin * spAngle)
        p2 = ((self.rmin + self.offset_rayon) * cosinus,
              (self.rmin + self.offset_rayon) * sinus)
        p3 = ((self.rmax - self.offset_rayon) * cosinus,
              (self.rmax - self.offset_rayon) * sinus)
        p4 = (self.rmax * cpAngle, self.rmax * spAngle)
        #
        tan = sinus / cosinus
        den = _math.sqrt(1 + tan**2)
        pcmin = (self.rmin / den,  self.rmin / den * tan)
        pcmax = (self.rmax / den,  self.rmax / den * tan)
        #
        alpha = 1
        beta = 1 - alpha
        barymin = (alpha*p2[0] + beta*pcmin[0], alpha*p2[1] + beta*pcmin[1])
        barymax = (alpha*p3[0] + beta*pcmax[0], alpha*p3[1] + beta*pcmax[1])
        #
        ctx.arc(0, 0, self.rmin, -pAngle, pAngle)
        ctx.curve_to(pcmin[0], pcmin[1],
                     barymin[0], barymin[1],
                     p2[0], p2[1])
        ctx.line_to(p3[0], p3[1])
        ctx.curve_to(barymax[0], barymax[1],
                     pcmax[0], pcmax[1],
                     p4[0], p4[1])
        ctx.arc_negative(0, 0, self.rmax, pAngle, -pAngle)
        ctx.curve_to(pcmax[0], -pcmax[1],
                     barymax[0], -barymax[1],
                     p3[0], -p3[1])
        ctx.line_to(p2[0], -p2[1])
        ctx.curve_to(barymin[0], -barymin[1],
                     pcmin[0], -pcmin[1],
                     p1[0], -p1[1])


class Flower_pbar:
    def __init__(self, value, max_value, min_value,
                 n_sectors, sector_angle,
                 start_angle, angle_incr, angle_offset,
                 in_radius, out_radius, inter_radius,
                 hex_foreground_color, hex_background_color,
                 colormap=None, colormap_rev=False):
        """
        sector_angle : angle du secteur visible (typiquement 90% de angle_incr)
        angle_incr : angle total du secteur, espacements compris
        """
        self.value = value
        self.max_value = max_value
        self.min_value = min_value
        self.n_sectors = n_sectors
        self.start_angle = start_angle
        self.angle_incr = angle_incr
        self.angle_offset = angle_offset
        self.in_radius = in_radius
        self.out_radius = out_radius
        self.inter_radius = inter_radius
        self.sector_angle = sector_angle
        self.pat_foreground_color = str2cairorgb(hex_foreground_color)
        self.pat_background_color = str2cairorgb(hex_background_color)
        self.colormap = colormap
        self.colormap_rev = colormap_rev
        #
        self.value_incr = (self.max_value - self.min_value) / self.n_sectors
        if self.colormap:
            self.cmp2col()

    def cmp2col(self):
        # ne pas utiliser la 1re couleur qui est utilisé pour le fond
        # quand on utilise un thème -> 1 couleur de plus
        col = getattr(_cmaps, self.colormap).discrete(self.n_sectors + 1)

        self.colors = [tuple(map(float, col(i)))[:-1]
                       for i in range(1, self.n_sectors + 1)]
        if self.colormap_rev:
            self.colors.reverse()

    def draw(self, ctx, draw_method):
        for i in range(self.n_sectors):
            angle = _math.radians(self.start_angle + i * self.angle_incr)
            if self.value >= (i + 1)*self.value_incr:
                # pétale active
                ctx.save()
                ctx.rotate(angle)
                Petal_pbar(self.in_radius, self.out_radius, self.inter_radius,
                           self.sector_angle, self.angle_offset).draw(ctx)
                if self.colormap:
                    ctx.set_source_rgb(*self.colors[i])
                else:
                    ctx.set_source_rgb(*self.pat_foreground_color)
                getattr(ctx, draw_method)()
                ctx.restore()
            else:
                ctx.save()
                ctx.rotate(angle)
                Petal_pbar(self.in_radius, self.out_radius, self.inter_radius,
                           self.sector_angle, self.angle_offset).draw(ctx)
                ctx.set_source_rgb(*self.pat_background_color)
                getattr(ctx, draw_method)()
                ctx.restore()
                if self.value > i * self.value_incr:
                    angle = _math.radians(self.start_angle + i * self.angle_incr)
                    ctx.save()
                    ctx.rotate(angle)
                    ecart_relatif = (self.value - i*self.value_incr) / self.value_incr
                    new_sector_angle = ecart_relatif * self.sector_angle
                    new_angle_offset = ecart_relatif * self.angle_offset
                    #
                    Petal_pbar(self.in_radius, self.out_radius, self.inter_radius,
                               new_sector_angle, new_angle_offset).draw(ctx)
                    if self.colormap:
                        ctx.set_source_rgb(*self.colors[i])
                    else:
                        ctx.set_source_rgb(*self.pat_foreground_color)
                    getattr(ctx, draw_method)()
                    ctx.restore()


if __name__ == "__main__":
    import cairo

    on = "ff0000"
    off = "ffff00"
    dim = 800
    #
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, dim, dim)
    ctx = cairo.Context(img)
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()
    ctx.set_source_rgb(1, 1, 1)
    ctx.save()
    ctx.translate(dim/2, dim/2)
    f = Petal_pbar(150, 200, 10, 40, 5)
    f.draw(ctx)
    ctx.fill()
    ctx.restore()
    img.write_to_png("test_petal_fpbar.png")
    #
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, dim, dim)
    ctx = cairo.Context(img)
    ctx.set_source_rgb(0.3, 0.3, 0.3)
    ctx.paint()
    ctx.set_source_rgb(1, 1, 1)
    ctx.save()
    ctx.translate(dim/2, dim/2)
    f = Flower_pbar(75, 100, 0,
                    10, 20,
                    18, -240 / 10, 3,
                    50, 300, 10,
                    on, off, "ice", True)
    f.draw(ctx, "fill")
    ctx.fill()
    ctx.restore()
    img.write_to_png("test_flower_fpbar.png")
    #
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, dim, dim)
    ctx = cairo.Context(img)
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()
    ctx.set_source_rgb(1, 1, 1)
    ctx.save()
    ctx.translate(dim/2, dim/2)
    f = Petal_pbar(150, 200, 10, 190, 5)
    f.draw(ctx)
    ctx.stroke()
    ctx.restore()
    img.write_to_png("test_petal_fpbar_issue.png")
