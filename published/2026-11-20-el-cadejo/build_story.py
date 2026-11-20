#!/usr/bin/env python3
"""Builds story.json and script.md for 'El Cadejo (Chiapas). Edit BEATS here, then run.
After tts.py has run, re-run this: shots longer than ~9.5 s are split automatically with a second camera move."""
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__))


def L(src, **kw):
    d = {"src": f"art/{src}.png"}; d.update(kw); return d


def S(bg, *layers, cam=None, fx=None, text=None, tr=None, tl=None, w=None, grade=None, out=None, dur=None, vig=None):
    sc = {"layers": [L(bg)] + list(layers)}
    if cam: sc["cam"] = {"from": list(cam[0]), "to": list(cam[1]), "ease": cam[2] if len(cam) > 2 else "inout"}
    if fx: sc["fx"] = fx
    if text: sc["text"] = text
    if tr: sc["transition"] = tr
    if tl: sc["transition_len"] = tl
    if w: sc["weight"] = w
    if dur: sc["dur"] = dur
    if grade: sc["grade"] = grade
    if out: sc["out"] = "fade"; sc["out_len"] = out
    if vig: sc["vignette"] = vig
    return sc


def T(s, style, a=0.3, b=None, pos=None):
    d = {"str": s, "style": style, "at": [a, b if b else a + 4.0]}
    if not pos and style in ("quote", "big") and not s.startswith("PRÓXIMO"): pos = "bottom"
    if pos: d["pos"] = pos
    return d


def X(name, at=0.0, gain=-6, at_scene=None, pan=None, **args):
    d = {"name": name, "at": at, "gain": gain}
    if at_scene is not None: d["scene"] = at_scene
    if pan is not None: d["pan"] = pan
    if args: d["args"] = args
    return d


FOG = {"type": "fog", "strength": 0.35}
FOGL = {"type": "fog", "strength": 0.45, "low": True}
FL = {"type": "flicker", "amp": 0.08}
def SH(a, b, amp=7): return {"type": "shake", "amp": amp, "at": [a, b]}
def PU(bpm=70, amp=0.1): return {"type": "pulse", "bpm": bpm, "amp": amp}

N = 0
FOGLAY = L("l_fog", blend="screen", opacity=[0, 0.8], anim=[{"type": "drift", "dx": -0.06, "ease": "linear"}])
FIRE = L("l_fire_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.15, "speed": 1.8}])
WHITE = L("l_white", depth=1.12, anim=[{"type": "drift", "dx": 0.05, "ease": "linear"}, {"type": "float", "amp": 0.002, "period": 0.8}])
WHITEG = L("l_white", depth=1.12, blend="normal", opacity=[0, 1.0], fade_in=1.8, anim=[{"type": "float", "amp": 0.002, "period": 3}])
WGLOW = L("l_white_glow", blend="screen", anim=[{"type": "pulse", "amp": 0.04, "period": 4, "pivot": [0.5, 0.75]}])
BLACK = L("l_black", depth=1.12, anim=[{"type": "scale", "from": 1.0, "to": 1.06, "pivot": [0.5, 0.85], "ease": "in"}])
BLACKG = L("l_black", depth=1.12, opacity=[0, 1.0], fade_in=2.0, anim=[{"type": "scale", "from": 1.0, "to": 1.05, "pivot": [0.5, 0.85]}])
EYES = L("l_eyes", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 1.2}])
WALK = L("l_tomas_walk", depth=1.1, anim=[{"type": "drift", "dx": 0.04, "ease": "linear"}, {"type": "float", "amp": 0.002, "period": 0.9}])
SMOKE = L("l_smoke", blend="screen", opacity=[0, 0.85], fade_in=1.5, anim=[{"type": "drift", "dx": 0.02, "dy": -0.05, "ease": "linear"}])

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)


ABU = dict(voice="ef_dora", speed=0.76)
TOM = dict(voice="em_santa", speed=0.86)
CAD = dict(voice="em_santa", speed=0.7, fx="eco")
NIGHT = ["night", {"name": "wind", "gain": -9}]
CRICK = ["crickets", {"name": "wind", "gain": -10}]

# ======================================================================== COLD OPEN
B("Camino real de Comitán, en los Altos de Chiapas. Medianoche.",
  S("road_night", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.25), "in"), fx=["dust"], tr="fade", tl=1.2,
    text=[T("Camino real de Comitán, Chiapas|medianoche", "date", 0.6, 4.5)]),
  pre=0.6, music="dread", amb=NIGHT, sfx=[X("owl", 1.0, -16)])
B("Imagina que vas caminando solo, de regreso a tu pueblo. La luna se esconde detrás de las nubes. Solo se oyen tus pasos sobre la tierra.",
  S("road_night2", WALK, cam=((0.45, 0.55, 1.1), (0.55, 0.55, 1.3), "linear"), fx=[FOGL]),
  sfx=[X("footsteps", 0.5, -12, dur=7)])
B("Y entonces escuchas otros pasos detrás de ti. Pero no suenan como pasos de persona. Suenan duros. Pequeños. Como pezuñas de cabra… sobre la piedra.",
  S("hooves", cam=((0.5, 0.55, 1.1), (0.5, 0.6, 1.45), "in"), fx=[FOGL, PU(70, 0.06)], grade="cold"),
  music="tension", sfx=[X("hooves", 2.5, -10, dur=6, distance=0.4, bpm=60), X("heartbeat", 0.5, -12, dur=8, bpm=80)])
B("Te das la vuelta. Y a diez pasos, en medio del camino, hay un perro negro, grande como un becerro, con dos brasas rojas en lugar de ojos.",
  S("road_fog", BLACKG, cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.35), "in"), fx=[FOGL], grade="night"),
  S("black_eyes", tr="flash", tl=0.12, dur=1.5, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.55)), fx=[SH(0, 0.6, 9)]),
  pause=0.6, sfx=[X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("EL CADEJO|el perro que te sigue de noche", "title", 0.6, 6.4)]),
  pause=5.2, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Y a tu lado, pegado a tu pierna, sin que sepas desde cuándo… hay otro perro. Blanco. Que no te quita los ojos de encima.",
  S("white_close", WGLOW, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=["dust"], grade="moon"))
B("Uno de los dos te quiere llevar. El otro te quiere llevar a casa. El problema es que, en la oscuridad… a veces no sabes cuál es cuál.",
  S("moon_two", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOG], grade="night"),
  sfx=[X("howl", 1.5, -12)])
B("Lo que encontraron en el puente a la mañana siguiente nadie lo ha podido explicar. Y lo que el muchacho confesó antes de morir… lo vas a saber al final.",
  S("bridge", FOGLAY, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.35), "in"), fx=[FOG], grade="night"))

# ======================================================================== I
B("Cuentan que esto le pasó a Tomás, un muchacho de diecinueve años que tocaba la marimba en un pueblo cerca de Comitán, allá por los años cuarenta.",
  S("fiesta", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["embers"], tr="fade", tl=1.0, grade="warm",
    text=[T("CAPÍTULO I|El camino viejo", "chapter", 0.6, 5.0)]),
  S("tomas_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust"], tr="xfade", tl=0.8),
  music="calm", amb=["crickets", {"name": "fire", "gain": -12}])
B("Tomás tocaba en todas las fiestas. Bodas, novenarios, fiestas de santos. Y siempre volvía tarde, caminando, por el camino viejo que cruza el monte entre los pinos.",
  S("marimba", FIRE, cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.3), "linear"), fx=["embers"], grade="warm"),
  S("road_night", cam=((0.3, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=[FOGL], tr="xfade", tl=0.8))
B("Su abuela, doña Chabela, lo esperaba despierta junto al fogón. Y cada noche, antes de que saliera, le decía lo mismo.",
  S("kitchen", FIRE, cam=((0.45, 0.5, 1.05), (0.55, 0.5, 1.25), "in"), fx=["embers", FL], grade="candle"))
B("Mijo, si de regreso te sale un perro en el camino, no le hables, no le tires piedras y no corras. Y fíjate bien de qué color es.",
  S("abuela", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=[FL], grade="candle",
    text=[T("Fíjate bien de qué color es.|doña Chabela", "quote", 3.5, 8.0)]), **ABU)
B("Tomás se reía. Le decía que ya estaba grande para cuentos de perros. Pero la abuela no se reía. Nunca se reía cuando hablaba del Cadejo.",
  S("tomas_smile", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.25), "in"), fx=["dust"], grade="candle"),
  S("abuela", cam=((0.5, 0.4, 1.3), (0.5, 0.4, 1.5), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6))
B("Porque en el sur de México y en toda Centroamérica, desde Chiapas hasta Costa Rica, los viejos cuentan que de noche, por los caminos, andan dos perros que no son perros.",
  S("map", cam=((0.45, 0.5, 1.05), (0.4, 0.55, 1.3), "in"), fx=["dust"], grade="sepia"),
  music="mystery")
B("Los arrieros lo conocían bien. Los que llevaban café y mercancía por las veredas de la sierra, de pueblo en pueblo, decían que más de una vez un perro blanco les había salido al camino. Que los acompañaba un buen trecho… y luego, sin más, desaparecía.",
  S("arrieros", WGLOW, cam=((0.35, 0.55, 1.05), (0.6, 0.55, 1.2), "linear"), fx=[FOGL, "dust"], grade="moon"),
  sfx=[X("hooves", 0.5, -16, dur=8, distance=0.8)])
B("Uno es blanco. Dicen que lo mandó Dios para cuidar a los que andan solos de noche. A los arrieros, a los caminantes… y a los borrachos que no encuentran el camino a casa.",
  S("white_full", WGLOW, cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], grade="moon",
    text=[T("EL BLANCO|cuida", "big", 1.0, 4.5)]),
  S("drunk", WGLOW, cam=((0.4, 0.55, 1.1), (0.55, 0.55, 1.25), "linear"), fx=[FOGL], tr="xfade", tl=0.8))
B("El otro es negro. Tiene los ojos rojos como carbones, a veces arrastra una cadena, y dicen que huele a azufre. A ese, cuentan, lo mandó el Diablo.",
  S("black_full", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL, PU(60, 0.06)], grade="night",
    text=[T("EL NEGRO|lleva", "big", 1.0, 4.5)]),
  S("chain", cam=((0.4, 0.6, 1.2), (0.6, 0.6, 1.35), "linear"), fx=[FOGL], tr="xfade", tl=0.6, grade="blood"),
  music="dread", sfx=[X("chains", 0.5, -10, at_scene=1)])
B("Y los dos, dicen, buscan a la misma persona.",
  S("moon_two", cam=((0.5, 0.45, 1.2), (0.5, 0.5, 1.05), "out"), fx=[FOG], grade="night"), pause=0.9)

# ======================================================================== II
B("Aquella noche de octubre, la fiesta terminó pasada la medianoche. Tomás guardó las baquetas, se despidió de los músicos y tomó el camino viejo. Solo.",
  S("fiesta", cam=((0.6, 0.5, 1.2), (0.45, 0.5, 1.05), "out"), fx=["embers"], tr="fade", tl=1.0, grade="warm",
    text=[T("CAPÍTULO II|El perro blanco", "chapter", 0.6, 5.0)]),
  S("road_night2", WALK, cam=((0.4, 0.55, 1.1), (0.55, 0.55, 1.25), "linear"), fx=[FOGL], tr="xfade", tl=0.8),
  music="calm", amb=CRICK)
B("Le habían ofrecido quedarse. Le habían ofrecido una lámpara. Dijo que no. Que conocía el camino de memoria.",
  S("tomas_portrait", cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.4), "in"), fx=[FOG], grade="moon"))
B("Al día siguiente tenía que ayudar a su tío en la milpa. Así que caminó. Silbando los sones que había tocado esa noche, con el morral de las baquetas apretado contra el pecho. A lo lejos, de vez en cuando, ladraba el perro de algún rancho.",
  S("milpa", cam=((0.3, 0.55, 1.05), (0.6, 0.55, 1.2), "linear"), fx=[FOGL], grade="night"),
  sfx=[X("howl", 6.0, -22)])
B("Los primeros kilómetros fueron tranquilos. Grillos. El viento en los pinos. El olor de la tierra mojada por la lluvia de la tarde.",
  S("pines_bg", FOGLAY, cam=((0.3, 0.5, 1.1), (0.7, 0.5, 1.15), "linear"), fx=[FOGL], grade="night"),
  sfx=[X("footsteps", 0.3, -14, dur=8)])
B("Hasta que, al llegar a la cruz de madera que marca la mitad del camino, los grillos se callaron. Todos. Al mismo tiempo.",
  S("cross_road", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.3), "in"), fx=[FOGL], grade="night"),
  amb=["wind"], music="tension")
B("Tomás se detuvo. Y fue entonces cuando lo vio.",
  S("tomas_fear", cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.45), "in"), fx=[PU(80, 0.06)], grade="moon"),
  sfx=[X("heartbeat", 0.0, -12, dur=5, bpm=90)])
B("Sentado junto a la cruz, quieto como una estatua, había un perro blanco. Muy blanco. Tanto, que parecía brillar con una luz que no venía de ningún lado.",
  S("cross_road", WHITEG, WGLOW, cam=((0.5, 0.6, 1.2), (0.5, 0.6, 1.45), "in"), fx=[FOGL], grade="moon"),
  sfx=[X("whoosh", 0.5, -12)])
B("No ladró. No gruñó. Solo se levantó despacio… y se puso a caminar a su lado.",
  S("white_close", WGLOW, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.5), "in"), fx=["dust"], grade="moon"),
  S("road_walk_two", cam=((0.4, 0.55, 1.1), (0.55, 0.55, 1.25), "linear"), fx=[FOGL], tr="xfade", tl=0.6))
B("Tomás pensó en espantarlo. Pero recordó la voz de su abuela. No le hables. No le tires piedras. No corras. Y siguió caminando.",
  S("abuela", cam=((0.5, 0.4, 1.4), (0.5, 0.4, 1.55), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.5),
  S("road_walk_two", cam=((0.6, 0.6, 1.4), (0.5, 0.6, 1.55), "linear"), fx=[FOGL], tr="xfade", tl=0.5),
  sfx=[X("whisper", 0.5, -18, dur=3)])
B("El perro caminaba exactamente a su paso. Si Tomás se detenía, el perro se detenía. Si apuraba el paso, el perro también. Y nunca, ni una sola vez, dejaba de mirar hacia atrás.",
  S("road_walk_two", cam=((0.45, 0.55, 1.1), (0.6, 0.55, 1.2), "linear"), fx=[FOGL]),
  S("white_look", WGLOW, cam=((0.5, 0.5, 1.15), (0.5, 0.48, 1.35), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.6),
  sfx=[X("footsteps", 0.0, -14, dur=10)])
B("Como si estuviera vigilando algo. Algo que venía detrás de ellos.",
  S("road_fog", EYES, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.5), "in"), fx=[FOGL], grade="night"),
  sfx=[X("riser", 0.0, -12, dur=4)], pause=0.8)
B("Si te gustan estas historias, suscríbete y activa la campanita. Cada semana traemos una leyenda nueva de algún rincón de México.",
  S("title_bg", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.2)), fx=[FOG], tr="xfade", tl=0.6), music="mystery")

# ======================================================================== III
B("Cerca del puente del arroyo, el perro blanco se detuvo de golpe. Bajó la cabeza. Y por primera vez… gruñó.",
  S("bridge", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], tr="fade", tl=1.0, grade="night",
    text=[T("CAPÍTULO III|Las pezuñas", "chapter", 0.6, 5.0)]),
  S("white_growl", WGLOW, cam=((0.5, 0.45, 1.15), (0.5, 0.45, 1.4), "in"), fx=[SH(0.5, 1.2, 4)], grade="moon", tr="xfade", tl=0.6),
  music="tension", amb=["river", {"name": "wind", "gain": -8}])
B("Tomás sintió el olor antes que nada. Un olor a cerillo quemado, a huevo podrido, que le picaba la garganta. Azufre.",
  S("bridge_far", SMOKE, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL], grade="blood",
    text=[T("AZUFRE|", "big", 4.5, 7.5)]))
B("Y luego el ruido. Tac… tac… tac. Algo caminaba sobre las tablas del puente. Algo pesado, que pisaba con pezuñas.",
  S("hooves", cam=((0.4, 0.55, 1.2), (0.6, 0.6, 1.5), "linear"), fx=[FOGL], grade="cold"),
  sfx=[X("hooves", 0.8, -8, dur=7, distance=0.3, bpm=50)])
B("Tomás miró al perro blanco. Pero el perro blanco no lo miraba a él. Tenía los ojos fijos en la neblina, y temblaba. No de miedo. De rabia.",
  S("white_growl", WGLOW, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.5), "in"), fx=[SH(2.0, 3.5, 3)], grade="moon"))
B("Y detrás del sonido, como un arrastre, el tintineo de una cadena.",
  S("chain", cam=((0.5, 0.6, 1.2), (0.5, 0.6, 1.5), "in"), fx=[FOGL], grade="night"),
  sfx=[X("chains", 0.3, -6)])
B("Del otro lado del puente, entre la neblina, se encendieron dos puntos rojos. Luego se acercaron.",
  S("bridge_far", EYES, cam=((0.5, 0.5, 1.2), (0.5, 0.48, 1.6), "in"), fx=[FOGL, PU(80, 0.08)], grade="night"),
  sfx=[X("heartbeat", 0.0, -10, dur=7, bpm=95)])
B("Era un perro negro, más grande que cualquier perro que Tomás hubiera visto. El pelo le colgaba en greñas enredadas. Y donde debían estar las patas… había pezuñas.",
  S("black_eyes", tr="flash", tl=0.12, dur=1.4, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.5)), fx=[SH(0, 0.6, 9)]),
  S("black_full", cam=((0.5, 0.5, 1.1), (0.5, 0.6, 1.4), "in"), fx=[FOGL, PU(60, 0.06)], grade="night"),
  sfx=[X("sting", 0.0, -2), X("boom", 0.0, -3)])
B("Por eso, dicen, se llama Cadejo. En el español antiguo, un cadejo es un mechón de pelo enredado. Una greña. Así es su pelo. Y así, dicen, es su alma.",
  S("black_close", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FOGL], grade="night",
    text=[T("CADEJO|mechón de pelo enredado", "big", 1.0, 5.0)]))
B("El perro negro no se movió. Solo miró a Tomás. Y Tomás sintió algo muy extraño. Ganas de ir hacia él. De cruzar el puente. De seguirlo al monte, lejos del camino.",
  S("tomas_trance", cam=((0.5, 0.42, 1.1), (0.5, 0.42, 1.4), "in"), fx=[FOG, PU(50, 0.06)], grade="blood"),
  music="dread")
B("Tomás… ven… ya es tarde… vente conmigo…",
  S("black_eyes", cam=((0.5, 0.45, 1.2), (0.5, 0.45, 1.5), "in"), fx=[FOG], grade="blood",
    text=[T("Tomás… vente conmigo…|", "whisper", 0.5, 5.0)]), **CAD)
B("Dio un paso. Luego otro. Las piernas se le movían solas.",
  S("bridge_steps", cam=((0.5, 0.6, 1.1), (0.5, 0.55, 1.4), "in"), fx=[FOGL], grade="night"),
  sfx=[X("footsteps", 0.2, -10, dur=4)])
B("Cuentan que a quien sigue al Cadejo negro lo encuentran días después, perdido en el monte, sin saber quién es, con la mirada vacía. Dicen que ya nunca vuelve a ser el mismo.",
  S("lost_man", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOG], grade="cold"))
B("Y entonces, algo blanco pasó junto a él como un relámpago.",
  S("white_leap", tr="flash", tl=0.12, cam=((0.45, 0.5, 1.1), (0.55, 0.5, 1.3), "linear"), fx=[SH(0, 0.5, 6)], grade="moon"),
  sfx=[X("whoosh", 0.0, -4), X("boom", 0.1, -6)], pause=0.8)

# ======================================================================== IV
B("El perro blanco se plantó en medio del puente, entre Tomás y la bestia. El pelo erizado. Los dientes al aire.",
  S("standoff", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], tr="fade", tl=0.8, grade="night",
    text=[T("CAPÍTULO IV|La pelea", "chapter", 0.6, 5.0)]),
  music="climax", amb=["river", {"name": "wind", "gain": -6}])
B("El Cadejo negro abrió el hocico. Y lo que salió no fue un ladrido. Fue un sonido largo, ronco, como un hombre riéndose en el fondo de un pozo.",
  S("black_close", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.5), "in"), fx=[FOGL, PU(70, 0.1)], grade="blood"),
  S("red_flash", tr="flash", tl=0.1, dur=1.0, fx=[SH(0, 0.6, 10)]),
  sfx=[X("howl", 0.8, -6), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("Los dos animales se lanzaron uno contra el otro.",
  S("fight", cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.4), "in"), fx=[SH(0.2, 2.5, 8), {"type": "lightning", "at": [0.4]}], grade="night"),
  sfx=[X("boom", 0.2, -4), X("thunder", 0.4, -6)])
B("Tomás no vio la pelea. Solo vio sombras. Una blanca y una negra, rodando sobre las tablas, en la neblina. Chispas, como cuando se golpea un pedernal. Gruñidos que hacían temblar el puente.",
  S("fight2", cam=((0.4, 0.5, 1.15), (0.6, 0.5, 1.35), "linear"), fx=[FOGL, SH(1.0, 3.0, 6), "embers"], grade="night"),
  S("fight", cam=((0.6, 0.45, 1.4), (0.4, 0.5, 1.6), "linear"), fx=[SH(0.0, 2.0, 8), {"type": "lightning", "at": [0.8]}], tr="xfade", tl=0.4),
  sfx=[X("whoosh", 1.0, -8), X("boom", 4.0, -8), X("thunder", 7.0, -10)])
B("Y escuchó, clarita, la voz de su abuela dentro de su cabeza. No corras. No corras.",
  S("abuela", cam=((0.5, 0.4, 1.4), (0.5, 0.4, 1.6), "in"), fx=[FL], grade="candle"))
B("No corrió. Se quedó ahí, temblando, con las manos juntas, rezando lo único que se sabía completo. El Padre Nuestro.",
  S("tomas_pray", cam=((0.5, 0.45, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FOG, FL], grade="moon"),
  sfx=[X("whisper", 1.0, -16, dur=5)])
B("No supo cuánto tiempo pasó. Un minuto. Una hora. Hasta que, de repente… silencio.",
  S("fight2", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.3), "in"), fx=[FOGL], grade="night", out=1.0),
  S("bridge", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.3), "in"), fx=[FOGL], grade="cold", tr="fade", tl=1.0),
  music="silence", amb=["river"], pause=1.2)
B("La neblina se abrió. El puente estaba vacío. No había perro negro. No había perro blanco. Solo el olor a azufre, cada vez más débil, y el agua del arroyo corriendo abajo.",
  S("bridge", FOGLAY, cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.2), "linear"), fx=[FOGL], grade="cold"),
  music="sad")
B("Tomás cruzó el puente corriendo, ahora sí. Y no se detuvo hasta ver el fogón encendido de su casa.",
  S("road_night2", WALK, cam=((0.4, 0.55, 1.2), (0.65, 0.55, 1.3), "linear"), fx=[FOGL]),
  S("house", FIRE, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  sfx=[X("footsteps", 0.0, -8, dur=5)], amb=["night"])
B("La abuela Chabela estaba en la puerta. Como si lo hubiera estado esperando. Lo miró de arriba abajo y solo le preguntó una cosa.",
  S("abuela_door", FIRE, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=[FL], grade="candle"))
B("¿De qué color era el que te trajo?",
  S("abuela", cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.4), "in"), fx=[FL], grade="candle",
    text=[T("¿De qué color era el que te trajo?|doña Chabela", "quote", 0.4, 4.0)]), **ABU)
B("Blanco, abuela. Era blanco.",
  S("tomas_fear", cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.4), "in"), fx=[FL], grade="candle"), **TOM)
B("La abuela cerró los ojos y se persignó. Luego puso un plato de tortillas afuera de la puerta, del lado del camino.",
  S("door_plate", FIRE, cam=((0.5, 0.55, 1.05), (0.5, 0.6, 1.3), "in"), fx=[FL], grade="candle"))
B("Esto es para él. Para que sepa que se lo agradecemos.",
  S("abuela", cam=((0.5, 0.4, 1.3), (0.5, 0.4, 1.45), "in"), fx=[FL], grade="candle"), **ABU, pause=1.0)

# ======================================================================== V
B("Al amanecer, Tomás volvió al puente con su tío y dos vecinos.",
  S("bridge_dawn", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=[FOGL], tr="fade", tl=1.0, grade="cold",
    text=[T("CAPÍTULO V|El mechón blanco", "chapter", 0.6, 5.0)]),
  music="mystery", amb=["river", {"name": "wind", "gain": -10}], sfx=[X("bell", 1.5, -18, freq=300)])
B("Las tablas estaban rayadas, como arañadas por garras enormes. Y en el lodo de la orilla había huellas de perro… y, mezcladas con ellas, huellas de pezuñas.",
  S("prints", cam=((0.4, 0.55, 1.1), (0.6, 0.55, 1.4), "linear"), fx=["dust"], grade="cold",
    text=[T("PEZUÑAS|", "big", 6.0, 9.0)]))
B("Pero lo que nadie supo explicar fue lo que había al final del puente. Un círculo de hierba quemada, negra, como si ahí hubiera caído un rayo.",
  S("burnt", SMOKE, cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=["ash"], grade="cold"))
B("Y en medio, enredado entre la hierba… un mechón de pelo blanco.",
  S("fur_close", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.45), "in"), fx=["dust"], grade="moon"),
  sfx=[X("sting", 0.5, -10)], pause=0.9)
B("Cuando volvieron a la casa, el plato de tortillas de la puerta estaba vacío. Limpio. Como lamido.",
  S("plate_empty", cam=((0.5, 0.5, 1.1), (0.5, 0.55, 1.4), "in"), fx=["dust"], grade="warm"))
B("La abuela no dijo nada. Solo sonrió, por primera vez en mucho tiempo. Y guardó el mechón blanco en una cajita de madera, junto a la imagen de la Virgen.",
  S("altar_box", L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 2.0}]), cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FL, "dust"], grade="candle"))
B("Tomás vivió muchos años. Nunca dejó de tocar la marimba. Pero nunca más volvió a tomar el camino viejo de noche. Y todas las noches de su vida, hasta la última, dejó un plato de tortillas en la puerta.",
  S("old_tomas", FIRE, cam=((0.5, 0.42, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust", FL], grade="candle"),
  S("door_plate", FIRE, cam=((0.5, 0.6, 1.2), (0.5, 0.6, 1.35), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8),
  music="sad")
B("Antes de morir, le contó a su nieta lo único que nunca le había dicho a nadie.",
  S("old_tomas", cam=((0.5, 0.4, 1.3), (0.5, 0.4, 1.5), "in"), fx=[FOG], grade="night"),
  music="dread")
B("Que desde aquella noche, cada vez que caminaba solo, escuchaba detrás de él unos pasos suaves. De perro. Siempre. Toda la vida.",
  S("road_night2", WALK, cam=((0.45, 0.55, 1.2), (0.55, 0.55, 1.35), "linear"), fx=[FOGL], grade="night"),
  sfx=[X("footsteps", 0.5, -12, dur=8)])
B("Y que nunca, ni una sola vez, se atrevió a voltear… para ver de qué color era.",
  S("road_fog", EYES, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.5), "in"), fx=[FOGL], grade="night"),
  S("black_eyes", tr="flash", tl=0.1, dur=1.4, fx=[SH(0, 0.5, 8)], cam=((0.5, 0.45, 1.35), (0.5, 0.45, 1.55))),
  sfx=[X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)], pause=1.2)

# ======================================================================== HISTORIA
B("Ahora, lo que sí es historia.",
  S("book", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2), "in"), fx=["dust"], tr="fade", tl=1.0, grade="sepia",
    text=[T("LO QUE DICE LA HISTORIA|", "chapter", 0.4, 4.0)]),
  music="calm", amb=["room"])
B("La leyenda del Cadejo se cuenta en Chiapas y en otros lugares del sureste mexicano, y también en Guatemala, El Salvador, Honduras, Nicaragua y Costa Rica. En cada lugar cambia un poco.",
  S("map", cam=((0.4, 0.5, 1.1), (0.55, 0.55, 1.3), "linear"), fx=["dust"], grade="sepia"))
B("En unos pueblos solo existe el negro. En otros, el blanco cuida a las mujeres que vuelven tarde, o a los borrachos, para que nadie les robe ni les haga daño. Y en algunos se dice que, si el Cadejo te lame, ya no te deja nunca.",
  S("drunk", WGLOW, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3), "in"), fx=[FOGL], grade="moon"),
  S("moon_two", cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.35), "in"), fx=[FOG], tr="xfade", tl=0.8))
B("La palabra sí es real. El diccionario la registra: cadejo es una porción de cabello enredado. Y en mil novecientos treinta, el escritor guatemalteco Miguel Ángel Asturias, que años después ganaría el Premio Nobel de Literatura, publicó en Madrid sus Leyendas de Guatemala.",
  S("book", cam=((0.45, 0.5, 1.15), (0.55, 0.5, 1.35), "linear"), fx=["dust"], grade="sepia",
    text=[T("Leyendas de Guatemala|Miguel Ángel Asturias, 1930", "date", 5.0, 10.0)]))
B("En una de ellas, el Cadejo nace de la trenza de una joven novicia, en un convento. De un mechón de pelo… nace la bestia.",
  S("braid_scene", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.4), "in"), fx=["dust", FL], grade="candle"))
B("Algunos investigadores ven en el Cadejo una mezcla de dos mundos: los perros negros de las leyendas que llegaron de España, y el perro de los pueblos mesoamericanos, que acompañaba a las almas en su camino al Mictlán, el lugar de los muertos.",
  S("xolo", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust", "embers"], grade="warm"))
B("Un perro que te acompaña en el camino. Para cuidarte… o para llevarte.",
  S("moon_two", cam=((0.5, 0.45, 1.2), (0.5, 0.5, 1.05), "out"), fx=[FOG], grade="night"), pause=1.0)
B("Y tú, ¿has oído pasos detrás de ti en un camino de noche? ¿En tu pueblo cuentan del Cadejo blanco o del negro? Te leo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOG], tr="fade", tl=0.8), music="mystery")
B("En el próximo video entraremos a un convento de la Ciudad de México, el de La Concepción, donde una joven novicia fue encerrada contra su voluntad. Y lo que sus compañeras encontraron una mañana en el huerto todavía se cuenta en voz baja.",
  S("convent", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOGL], grade="night",
    text=[T("PRÓXIMO VIDEO|La Monja de La Concepción", "big", 2.0, 7.0)]), sfx=[X("bell", 1.0, -14, freq=200)])
B("Hasta la próxima leyenda. Y si alguna noche, caminando solo, escuchas detrás de ti unos pasos suaves… no voltees.",
  S("road_night2", WALK, cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.45), "in"), fx=[FOGL], grade="night", out=2.0),
  pause=1.0, music="dread")

VARIANTS = {"abuela": ["abuela", "abuela", "abuela2", "abuela2", "abuela", "abuela"], "road_night2": ["road_night2", "road_night3"], "bridge": ["bridge", "bridge2"]}
_cnt = {}
for b in BEATS:
    for sc in b["scenes"]:
        n = sc["layers"][0]["src"][4:-4]
        if n in VARIANTS:
            k = _cnt.get(n, 0); _cnt[n] = k + 1
            sc["layers"][0]["src"] = f"art/{VARIANTS[n][k % len(VARIANTS[n])]}.png"

# timeline-aware pass: split long shots, resolve sfx relative to a scene
TL = os.path.join(HERE, "audio", "timeline.json")
MAXSHOT = 9.5
if os.path.exists(TL):
    tl = json.load(open(TL)); tb = tl["beats"]
    for i, b in enumerate(BEATS):
        if i >= len(tb): break
        end = tb[i + 1]["start"] if i + 1 < len(tb) else tl["duration"] + 5.0
        d = end - tb[i]["start"]; sc = b["scenes"]
        fixed = sum(s.get("dur", 0) for s in sc); wsum = sum(s.get("weight", 1) for s in sc if "dur" not in s) or 1
        # split
        new = []; idxmap = []
        for j, s in enumerate(sc):
            sd = s["dur"] if "dur" in s else max(0, d - fixed) * s.get("weight", 1) / wsum
            k = max(1, math.ceil(sd / MAXSHOT)) if "dur" not in s else 1
            idxmap.append(len(new))
            if k == 1: new.append(s); continue
            cam = s.get("cam", {"from": [0.5, 0.5, 1.05], "to": [0.5, 0.5, 1.25], "ease": "inout"})
            f, t = cam["from"], cam["to"]
            for m in range(k):
                c = json.loads(json.dumps(s))
                c["weight"] = s.get("weight", 1) / k
                if m > 0:
                    c.pop("text", None); c["transition"] = "xfade"; c["transition_len"] = 0.7
                    c.pop("fx", None) if False else None
                    z = max(f[2], t[2]) + 0.12 * m
                    dx = 0.08 if m % 2 else -0.08
                    c["cam"] = {"from": [min(0.75, max(0.25, t[0] + dx)), t[1], min(1.8, z)],
                                "to": [min(0.75, max(0.25, t[0] - dx)), t[1] - 0.02, min(1.85, z + 0.12)], "ease": "inout"}
                if m < k - 1: c.pop("out", None); c.pop("out_len", None)
                new.append(c)
        b["scenes"] = new
        sc = new
        fixed = sum(s.get("dur", 0) for s in sc); wsum = sum(s.get("weight", 1) for s in sc if "dur" not in s) or 1
        offs = []; t = 0.0
        for s in sc:
            offs.append(t); t += s["dur"] if "dur" in s else max(0, d - fixed) * s.get("weight", 1) / wsum
        for c in b.get("sfx", []):
            if "scene" in c:
                c["at"] = round(offs[idxmap[c["scene"]]] + c["at"], 3); del c["scene"]

story = {"title": "El Cadejo", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "D", "seed": 93, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# El Cadejo — guion\n",
                  "Narración en español (narrador: em_alex; doña Chabela: ef_dora; Tomás: em_santa; el Cadejo negro: em_santa con eco).\n"]
WHO = {"ef_dora": "DOÑA CHABELA: ", "em_santa": "TOMÁS: "}
for b in BEATS:
    for sc in b["scenes"]:
        for t in sc.get("text", []):
            if t["style"] in ("chapter", "title"): out.append(f"\n## {t['str'].replace('|', ' — ').rstrip(' —')}\n")
    if b["text"]:
        out.append(WHO.get(b.get("voice"), "") + b["text"]); words += len(b["text"].split())
open(os.path.join(HERE, "script.md"), "w").write("\n\n".join(out) + "\n")
arts = sorted({l["src"] for b in BEATS for sc in b["scenes"] for l in sc["layers"]})
print(f"beats {len(BEATS)}  scenes {sum(len(b['scenes']) for b in BEATS)}  words {words}  art {len(arts)}")
print(" ".join(a[4:-4] for a in arts))
