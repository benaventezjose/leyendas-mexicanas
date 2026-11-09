#!/usr/bin/env python3
"""Writes every illustration of 'Don Juan Manuel' to art/*.svg (render with render_svg.js)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from djm_art3 import *  # noqa
from djm_art import portrait, noble, persp_street

A = os.path.join(HERE, "art"); os.makedirs(A, exist_ok=True)
only = set(sys.argv[1:])


def put(name, *parts):
    if only and name not in only: return
    open(os.path.join(A, name + ".svg"), "w", encoding="utf-8").write(svg(*parts))


def fg_arch():
    return ('<path d="M0,0 L2400,0 L2400,1350 L0,1350 Z M260,1350 L260,620 A940,700 0 0 1 2140,620 L2140,1350 Z" fill="#020203" fill-rule="evenodd"/>'
            f'<path d="M260,1350 L260,620 A940,700 0 0 1 2140,620 L2140,1350" stroke="{MOONRIM}" stroke-width="6" fill="none" opacity="0.3"/>')


def fg_bars():
    s = '<path d="M0,0 L2400,0 L2400,1350 L0,1350 Z M300,140 L2100,140 L2100,1210 L300,1210 Z" fill="#030304" fill-rule="evenodd"/>'
    for k in range(9):
        s += f'<rect x="{360 + k * 205}" y="140" width="26" height="1070" fill="#050506"/>'
    s += '<rect x="300" y="640" width="1800" height="24" fill="#050506"/>'
    return s


# ---------------------------------------------------------------- backgrounds (opaque)
put("street_night", persp_street(3, "night"))
put("street_b", persp_street(8, "night", portal=False, vx=760, moon_x=1300))
put("street_dawn", persp_street(3, "dawn"))
put("street_c", persp_street(12, "night", portal=False, vx=1640, moon_x=760))
put("street_modern", persp_street(3, "modern", niche=False))
put("portal_night", portal_close("night"))
put("portal_dawn", portal_close("dawn", ajar=False))
put("house_night", house_facade(True))
put("belltower", belltower_low())
put("clock", clock_close())
put("city", city_aerial())
put("canal", canal_night())
put("plaza", plaza_mayor())
put("gallows_night", gallows_scene("night", with_rope=False))
put("gallows_dawn", gallows_scene("dawn", with_rope=False))
put("bedroom", bedroom())
put("study", study())
put("patio", patio())
put("stairs", stairs())
put("balcony", balcony_close())
put("convent", convent())
put("confession", confession())
put("docs", docs())
put("viceroy", viceroy_cameo())
put("zaguan", zaguan_pov())
put("lantern_fallen", lantern_fallen())
put("candle_bg", candle_close())
put("plaque", plaque_modern())
put("djm_portrait", portrait())
put("djm_portrait_ember", portrait(eyes="ember", red=True))
put("djm_portrait_cold", portrait(cold=True, lantern=False, hat_glow=False))
put("devil_face", devil_face())
put("eyes_dark", eyes_dark())
put("wife_portrait", wife_portrait())
put("coffin", coffin_face())
put("rosary", rosary_hands())
# ---------------------------------------------------------------- layers (transparent)
put("l_djm", noble(1200, 1300, 1150))
put("l_djm_dagger", noble(1200, 1300, 1150, dagger=True))
put("l_nephew", noble(1200, 1300, 1050, young=True, flip=True, doublet="#4a1612", plume="#d8c8a0", cape_col="#1c2a44", lantern_tilt=8))
put("l_passer", noble(1200, 1300, 1050, hat_plume=False, flip=True, young=True, cape_col="#2a2a30", doublet="#2a2418"))
put("l_devil", devil_full())
put("l_wife_small", wife_window(1500, 720, 380))
put("l_wife_big", wife_window(1480, 1140, 880))
put("l_kneel", djm_kneel(760, 1270, 600))
put("l_hanged", hanged(1150, 392, 470))
put("l_noose", noose(1150, 390, 1.05))
put("l_procession", procession())
put("l_ronda", ronda())
put("l_dagger", dagger())
put("l_shadow", shadow_man())
put("l_clouds", clouds(21, 300, 8, "#141c28", "#8aa4c4", 0.75))
put("l_flame", candle_flame(1200, 594, 150))
put("l_arch", fg_arch())
put("l_pov_lantern", pov_lantern())
put("ship_wall", ship_wall())
put("l_bars", fg_bars())
print("svg written")
