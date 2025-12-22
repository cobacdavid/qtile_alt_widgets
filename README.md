# My Qtile Widgets

## Widgets

 - [Github contrib. widget](#github-contribution-widget)
 - [Matrix](#matrix)
 - [Tixynet](#tixynet)
 - [Clock alt](#clock-alt)

## License

[GNU/GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Github Contribution Widget

Example image with a full year:
<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/ghcw.png?raw=true" width=50% />

Example image with 3 years (and a smaller `bar`):
<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/ghcw2.png?raw=true" width=50% />


### Install

The `Ghcw` widget is in the `ghcw.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).

You will need the  `aiohttp` library : `pip install aiohttp`.

You have to get a **token** from the official github site. It's an easy task (via *settings* and *developer settings* menus), I recommand to create a new token for just that widget purpose. You'll need a classic token and the `read:user` permission.

### Usage
For example, in your `config.py` :

```python
frow widgets import ghcw  # if you put ghcw.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    ghcw.Ghcw("YOUR GITHUB TOKEN", idgithub="torvalds"),
    ...
]
...
```

### Options

Unlike original Github diagram, **the week begins on Monday**.

Currently 6 options:

 - `colors`: a five RGB colors tab using `(0, 0, 0)` for black and `(1, 1, 1)` for white, thus `(.5, .5, .5)` is midgrey. Default is `None` as default config uses a `theme` default.
 - `empty_cell_color`: RGB color for 0 contrib. Useful to set according to qtile bar background. Default is `None` as default config uses a `theme` default.
 - `gap`: distance in pixel between two squares. Default is `None` (and recommanded), in this case `gap` is calculated.
 - `idgithub`: the Github username you want to access. Default is `'cobacdavid'`.
 - `nweeks`: number of weeks i.e. columns to display. Default is 52 (a full year).
 - `theme`: a predefined color palette to use. Default is `'gh'`, github usual palette.

If you use a predefined theme, `colors` option will be ignored but `empty_cell_color` will replace the first RGB color of the theme palette.


### Interaction

 - Left click on the widget opens the username github page.
 - Right click sends a notification on existing themes names.

## Matrix

The widget offers a 10x10 square pixels matrix. According to a value in [0-100] interval, the widgets lights up pixels.

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/matrix.png?raw=true" width=10% />

Pixels are chosen randomly. For example, with a battery charge: 100% lights up every pixel, while 50% lights up half of the pixels.

The value comes from a shell command or a Python function.

### Install

The `Matrix` widget is in the `matrix.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import matrix  # if you put matrix.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    matrix.Matrix(inmargin=0, cmd=r"cat /sys/class/power_supply/BAT0/capacity"),
    ...
]
...
```

### Options

 - `ìnmargin` (int): margin all around the square. Default is `2` (pixels) ;
 - `update_interval` (int): delay in seconds between two refreshs of the widget. Default is `300` (seconds=5 minutes) ;
 - `cmd` (str): shell command to execute to get the value. The command has to return a number between 0 and 100. Default is `r"echo $(( RANDOM % 101 ))"`. Note: The string resulting will be stripped if it contains unwanted blank spaces. So don't worry about extra spaces...
 - `execshell` (str): path to shell to be used. Default is `"/usr/bin/bash"`.
 - `pyfunc` (function): a Python function returning a number between 0 and 100. Default is `None`.

If `pyfunc` is not `None`, the shell command will be ignored.

### Interaction
No interaction.

## Tixynet

The widget offers a tixy experience (https://tixy.land/) associated with net UP or DOWN. Animation continues if UP else animation stops.

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/tixynet.gif?raw=true" width=30% />


### Install

The `Tixynet` widget is in the `tixynet.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import tixynet  # if you put tixynet.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    tixynet.Tixynet(iface="enp3s0"),
    ...
]
...
```

### Options

 - `iface` (str): network interface. Default is `"eth0"`.
 - `iface_interval` (int): delay in seconds between two net UP check. Default is `5`.
 - `colors` (list[str, str]): colors array, first element for positive color, second  d for negative. Default is `["ffffff", "ff0000"]`.
 - `force_step` (float): Forces fake time `t` step. Can be useful using great `update_interval` to get a slow animation. Default is `None`.
 - `ìnmargin` (int): margin all around the widget. Default is `2` (pixels) ;
 - `pyfunc` (function): a Python function returning a number between -1 and 1. Default is `"lambda t,i,x,y: math.sin(y/8+t)"`.
 - `update_interval` (int): delay in seconds between two refreshs of the widget. This controls the  `t` parameter.  Default is `1` (refresh every second).
 - `w` and `h` control number of cells, respectively in width and height. Default values are respectively `20` and `10`. 


### Interaction
No interaction.

## Clock alt

An alternative clock with 4 available layouts. 

<img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/clock_alt0.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/clock_alt1.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/clock_alt2.png?raw=true" width=10% /> <img src="https://github.com/cobacdavid/my_qtile_widgets/blob/main/clock_alt3.png?raw=true" width=10% />


### Install

The `Clock alt` widget is in the `clock_alt.py` standalone file.

Install it using a `git clone` command or just in copying the file in a `~/.config/qtile/widgets/` directory (and create in it a `__init__.py` empty file).


### Usage
For example, in your `config.py` :

```python
frow widgets import clock_alt  # if you put clock_alt.py in a `widgets` dir.
...
my_bar_widgets = [
    ...
    clock_alt.Clock_alt(),
    ...
]
...
```

### Options

 - `fmts` (list[str, str]): two usual time string formats. Default is `["%d/%m", "%H:%M"]`.
 - `gapy` (int): vertical space between the two displays in pixels, uisng state 0 or 1. Default is `2` pixels.
 - `state` (int): 0, 1, 2 or 3. Default is `0`.
    - `0`: 1st format above 2nd
    - `1`: 2nd format above 1st
    - `2`: 1st format only
    - `3`: 2nd format only

### Interaction

Left and right click change `state`.
