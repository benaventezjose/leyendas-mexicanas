#!/usr/bin/env python3
"""Builds story.json and script.md for 'El Callejón del Aguacate'. Edit BEATS here, then run."""
import json, os
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
LAMP = L("l_lamp_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.4}])
CANDLE = L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 2.0}])
FOGLAY = L("l_fog", blend="screen", opacity=[0, 0.8], anim=[{"type": "drift", "dx": -0.06, "ease": "linear"}])
WING = L("l_window_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.1, "speed": 0.9}])
MANQ = L("l_mannequin", depth=1.0)
WALKER = L("l_walker", depth=1.2, anim=[{"type": "drift", "dx": 0.0, "dy": -0.015, "ease": "linear"}, {"type": "float", "amp": 0.003, "period": 0.9}])
GHOSTB = L("l_bride_ghost", blend="screen", opacity=[0, 0.85], fade_in=1.6, anim=[{"type": "float", "amp": 0.004, "period": 5}, {"type": "flicker", "amp": 0.15, "speed": 0.7}])
SPIDER = L("l_spider", depth=1.05, anim=[{"type": "drift", "dx": -0.05, "dy": 0.03, "ease": "inout"}])
CROWD = L("l_crowd", depth=1.25, anim=[{"type": "drift", "dx": 0.02, "ease": "linear"}])
DANCE = L("l_dance", blend="screen", opacity=[0, 0.85], fade_in=1.5, anim=[{"type": "sway", "deg": 3, "period": 3, "pivot": [0.5, 0.9]}])
VEILW = L("l_veil_wind", blend="screen", opacity=[0, 0.7], anim=[{"type": "drift", "dx": -0.1, "dy": -0.03, "ease": "linear"}, {"type": "sway", "deg": 2, "period": 4, "pivot": [0.5, 0.2]}])

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)


MOM = dict(voice="ef_dora", speed=0.82)
HIJA = dict(voice="ef_dora", speed=0.95)
EMP = dict(voice="ef_dora", speed=0.9)
GHO = dict(voice="ef_dora", speed=0.8, fx="eco")
MAN = dict(voice="em_santa", speed=0.85)

# ======================================================================== COLD OPEN
B("Chihuahua. Pasada la medianoche.",
  S("street_chih", LAMP, FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.25), "in"), fx=["dust"], tr="fade", tl=1.2),
  pre=0.6, music="dread", amb=["night", {"name": "wind", "gain": -9}], sfx=[X("bell", 0.4, -14, freq=140)])
B("Imagina que caminas solo por el centro de la ciudad. Las tiendas están cerradas. Solo un aparador sigue encendido, en la esquina.",
  S("street_chih", WALKER, LAMP, cam=((0.5, 0.6, 1.15), (0.5, 0.55, 1.35), "in"), fx=[FOGL], w=1.0),
  S("shop_front", MANQ, WING, cam=((0.5, 0.5, 1.05), (0.55, 0.5, 1.3), "in"), fx=["dust"], tr="xfade", tl=0.8, w=1.0),
  sfx=[X("footsteps", 0.0, -8, dur=8)])
B("Adentro, detrás del cristal, hay una novia. Vestido blanco, velo largo, un ramo de flores entre las manos.",
  S("window_close", WING, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.35), "in"), fx=["dust"], grade="moon"), music="tension")
B("Das un paso atrás. Volteas un segundo hacia la calle vacía. Y cuando regresas la mirada al aparador…",
  S("street_chih", LAMP, cam=((0.5, 0.55, 1.3), (0.45, 0.55, 1.4)), fx=[FOGL], grade="cold", dur=3.4),
  S("window_close", WING, cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.4)), fx=[FOG], grade="moon"))
B("la novia ya no mira hacia el frente. Te está mirando a ti.",
  S("window_turned", WING, cam=((0.5, 0.4, 1.35), (0.5, 0.38, 1.6), "in"), fx=[PU(80, 0.08)], grade="cold"),
  S("face_flash", tr="flash", tl=0.12, dur=1.5, cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.5)), fx=[SH(0, 0.5, 9)]),
  pause=0.6, sfx=[X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("",
  S("title_bg", GHOSTB, cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("LA PASCUALITA|la novia del aparador", "title", 0.6, 6.4)]),
  pause=5.2, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Desde hace casi cien años, esa novia mira pasar a la gente de Chihuahua. Le cambian el vestido, le cambian el peinado. Pero la mirada… la mirada siempre es la misma.",
  S("shop_front", MANQ, WING, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.05), "out"), fx=[FOGL], grade="night"))
B("Te acercas. Y notas algo que no tiene sentido. Sus manos tienen arrugas finas en los nudillos. Uñas de verdad. Y bajo la piel… unas venitas azules.",
  S("hand_close", cam=((0.5, 0.5, 1.0), (0.5, 0.5, 1.25), "in"), fx=["dust"], grade="moon"),
  sfx=[X("heartbeat", 1.0, -10, dur=8, bpm=70)])
B("Muchos juran que no es una maniquí. Que debajo de ese vestido hay algo más. Y qué es eso… lo vas a saber al final.",
  S("eyes_close", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3), "in"), fx=[PU(60, 0.05)], grade="cold"))
B("Esta es la leyenda de La Pascualita.",
  S("window_close", WING, cam=((0.5, 0.45, 1.3), (0.5, 0.5, 1.1)), fx=[FOG], grade="moon"))

# ======================================================================== I
B("Chihuahua nació en mil setecientos nueve, en el corazón del desierto, como un pueblo de mineros. La plata de las sierras cercanas la hizo crecer y llenarse de casonas de cantera.",
  S("desert", cam=((0.4, 0.5, 1.05), (0.6, 0.48, 1.2), "linear"), fx=["dust"], tr="fade", tl=1.0, grade="warm",
    text=[T("CAPÍTULO I|La tienda de la esquina", "chapter", 0.6, 5.0)]),
  S("mine", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=["dust", "embers"], grade="candle", tr="xfade", tl=0.8),
  music="calm", amb=["wind"], sfx=[X("howl", 2.5, -12)])
B("En mil novecientos treinta, la ciudad apenas dejaba atrás los años de la Revolución. Por sus calles habían pasado las tropas de Francisco Villa, y la gente tenía ganas de volver a celebrar: bautizos, quince años… y bodas.",
  S("street_day", cam=((0.4, 0.55, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="sepia",
    text=[T("Chihuahua, años veinte|después de la Revolución", "date", 0.5, 4.8)]), sfx=[X("hooves", 0.5, -14, dur=5, distance=0.7)])
B("En su centro se levanta una catedral barroca de dos torres, que tardó casi un siglo en terminarse. Y a unas cuadras de ella, en la esquina de las calles Victoria y Ocampo, había una tienda llamada La Popular.",
  S("cathedral", cam=((0.5, 0.5, 1.05), (0.5, 0.42, 1.3), "in"), fx=["dust"], grade="warm", w=1.0),
  S("street_day", cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3), "in"), fx=["dust"], tr="xfade", tl=0.8, w=1.0,
    text=[T("Calles Victoria y Ocampo|centro de Chihuahua", "date", 0.5, 4.8)]))
B("Ahí se vendían vestidos de novia. Telas de encaje, velos de tul, coronas de azahar. Las muchachas de la ciudad entraban con sus mamás y salían soñando con el día de su boda.",
  S("shop_interior", LAMP, cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.25), "linear"), fx=["dust"], grade="warm"),
  amb=["room"])
B("La dueña se llamaba Pascuala Esparza. Una mujer seria, de vestido oscuro y voz baja, que conocía a cada clienta por su nombre.",
  S("mother_portrait", CANDLE, cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle"))
B("Pascuala tenía una hija. Cuentan que era la muchacha más bonita del barrio: cabello oscuro, ojos grandes, una sonrisa tranquila.",
  S("daughter_portrait", cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=["dust"], grade="warm"), music="hope")
B("Pasaba las tardes en la tienda, ayudando a su madre. Doblaba los velos, acomodaba las cajas, y a veces se probaba los vestidos frente al espejo, cuando creía que nadie la veía.",
  S("mirror_shop", LAMP, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=["dust"], grade="warm"))
B("Un día, un joven de buena familia comenzó a visitarla. Le llevaba flores. La esperaba a la salida de misa, en la plaza frente a la catedral.",
  S("plaza_couple", cam=((0.4, 0.55, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="warm"), amb=["city"])
B("Y una tarde le pidió matrimonio. Pascuala, que casi nunca sonreía, dicen que esa noche lloró de felicidad.",
  S("mother_portrait", CANDLE, cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.45)), fx=[FL], grade="candle"))
B("Mi hija se va a casar con el vestido más hermoso que haya visto Chihuahua.",
  S("sewing", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.3), "in"), fx=[FL], grade="candle"), **MOM)
B("Y se puso a coserlo ella misma. Noche tras noche, a la luz de una lámpara, puntada por puntada.",
  S("sewing", CANDLE, cam=((0.6, 0.5, 1.3), (0.55, 0.45, 1.5), "in"), fx=[FL], grade="candle"),
  sfx=[X("clock", 0.0, -16, dur=7)], amb=["room", {"name": "clock", "gain": -8}])

# ======================================================================== II
B("Llegó el día de la boda.",
  S("cathedral_bells", cam=((0.5, 0.45, 1.05), (0.5, 0.35, 1.3), "in"), fx=["dust"], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|El día de la boda", "chapter", 0.6, 4.8)]),
  pre=1.0, pause=2.2, music="hope", amb=["city"], sfx=[X("bell", 0.5, -6, freq=180), X("bell", 2.0, -8, freq=150)])
B("La novia se vistió en su casa, rodeada de mujeres. Le acomodaron el velo, le pusieron la corona de azahares, le dieron el ramo de flores blancas.",
  S("daughter_bride", CANDLE, cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle"))
B("Estás lista, hija.",
  S("daughter_bride", CANDLE, cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.5)), fx=[FL], grade="candle"), **MOM)
B("Mamá… tengo un presentimiento.",
  S("daughter_bride", cam=((0.5, 0.42, 1.45), (0.5, 0.42, 1.6)), fx=[FL], grade="cold"), **HIJA)
B("Son nervios. Nada va a salir mal.",
  S("mother_portrait", CANDLE, cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.4)), fx=[FL], grade="candle"), **MOM)
B("Nadie se dio cuenta de que, entre los pliegues del ramo, algo se movía.",
  S("bouquet", SPIDER, cam=((0.5, 0.5, 1.1), (0.45, 0.5, 1.5), "in"), fx=["dust"], grade="candle"),
  music="tension", sfx=[X("whisper", 1.0, -16, dur=3)])
B("Una araña pequeña, negra y brillante. Con una mancha roja en el vientre, como una gota de sangre.",
  S("spider_close", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.6), "in"), fx=[PU(80, 0.06)], grade="night",
    text=[T("VIUDA NEGRA|", "big", 3.2, 6.8)]),
  sfx=[X("heartbeat", 0.0, -10, dur=7, bpm=85)])
B("La catedral estaba llena. Velas encendidas, flores en cada banca. El novio esperaba frente al altar.",
  S("wedding", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="candle"),
  amb=["room"], sfx=[X("whisper", 0.5, -22, dur=5)])
B("La novia caminó por el pasillo del brazo de un tío. Todos voltearon a verla. Dicen que nunca se había visto una novia tan hermosa.",
  S("wedding", cam=((0.5, 0.68, 1.55), (0.5, 0.6, 1.8), "in"), fx=["dust"], grade="candle"),
  sfx=[X("footsteps", 0.0, -14, dur=6)])
B("Pero a mitad del camino sintió un piquete en la muñeca. Pequeño. Como una espina.",
  S("wrist_close", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.5), "in"), fx=["dust"], grade="candle"),
  S("red_flash", tr="flash", tl=0.1, dur=0.9, fx=[SH(0, 0.4, 6)], grade="blood"),
  sfx=[X("sting", 0.0, -5, at_scene=1)])
B("No dijo nada. No quería arruinar el momento. Siguió caminando, sonriendo, con el ramo apretado contra el pecho.",
  S("wedding", cam=((0.48, 0.62, 1.7), (0.48, 0.6, 1.85), "in"), fx=["dust", PU(90, 0.05)], grade="candle"))
B("Frente al altar, el sacerdote comenzó a hablar. Y la novia empezó a sentir frío. Un frío que le subía por el brazo. La vista se le nublaba. Las velas se volvieron manchas de luz.",
  S("altar_blur", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.45), "in"), fx=[FOG, PU(100, 0.1)], grade="candle"),
  music="dread", sfx=[X("heartbeat", 0.0, -6, dur=12, bpm=110), X("riser", 6.0, -10, dur=4)])
B("Antes de decir que sí… se desplomó sobre el piso de la catedral.",
  S("white_flash", tr="flash", tl=0.1, dur=1.0, fx=[SH(0, 0.5, 12)]),
  S("veil_floor", cam=((0.5, 0.55, 1.15), (0.5, 0.6, 1.4), "in"), fx=[FOG], grade="cold"),
  pre=0.3, sfx=[X("boom", 0.0, -2), X("sting", 0.0, -4)])
B("El ramo rodó por el suelo. Y de entre las flores salió la araña, que se perdió en la oscuridad de las bancas.",
  S("veil_floor", SPIDER, cam=((0.5, 0.6, 1.4), (0.4, 0.65, 1.6)), fx=[FOG], grade="cold"), pause=1.0, music="sad")
B("La llevaron a su casa. Llamaron al médico. Pero ya no había nada que hacer. Esa misma noche, la novia se fue… todavía vestida de blanco.",
  S("sickbed", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FL], grade="candle", w=1.2),
  S("candle_out", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.4)), fx=[FOG], grade="cold", tr="xfade", tl=1.0, w=0.8),
  sfx=[X("gust", 8.0, -8)])

# ======================================================================== III
B("Si te gustan estas historias, suscríbete al canal: aquí contamos las leyendas de todo México.",
  S("street_chih", LAMP, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.3)), fx=[FOGL], grade="night", tr="fade", tl=0.8), music="calm")
B("Pascuala no volvió a ser la misma. Dejó de ir a misa. Dejó de abrir la tienda. Los vecinos la veían pasar por la calle sin mirar a nadie, como un fantasma vestido de negro.",
  S("mother_grief", CANDLE, cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="cold", tr="xfade", tl=0.8,
    text=[T("CAPÍTULO III|El luto", "chapter", 0.6, 4.6, pos="bottom")]), music="sad")
B("La Popular se quedó con las cortinas cerradas. Pero de noche, por las rendijas, se veía una luz encendida en el cuarto del fondo.",
  S("shop_closed", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL], grade="night"), amb=["night", {"name": "wind", "gain": -9}])
B("Nadie sabía qué hacía ahí dentro. Algunos decían que rezaba. Otros, que hablaba sola.",
  S("back_room", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FL], grade="candle"),
  sfx=[X("whisper", 0.5, -12, dur=5)])
B("Y otros, en voz muy baja, que escuchaban dos voces.",
  S("back_room", CANDLE, cam=((0.5, 0.5, 1.35), (0.5, 0.5, 1.55), "in"), fx=[FL, PU(60, 0.05)], grade="cold"),
  sfx=[X("whisper", 0.3, -9, dur=4, pan=-0.5), X("whisper", 1.5, -11, dur=3, pan=0.5)], music="dread")
B("Una madrugada, un vecino vio salir por la puerta de atrás a un hombre con un maletín negro. Caminaba rápido, con el sombrero hasta los ojos. Nadie supo quién era. Pero meses después, el barrio entero se acordó de él.",
  S("back_door", LAMP, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL], grade="night"),
  sfx=[X("door", 0.6, -8), X("footsteps", 1.5, -10, dur=4)])
B("Pasaron los meses. Y el veinticinco de marzo de mil novecientos treinta, La Popular volvió a abrir sus puertas.",
  S("crate", LAMP, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="warm",
    text=[T("25 de marzo de 1930|Chihuahua", "date", 0.5, 4.8)]), music="mystery", amb=["city"])
B("Esa mañana, en el aparador, había algo nuevo. Una maniquí vestida de novia. La más perfecta que nadie hubiera visto.",
  S("shop_day", MANQ, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="warm"))
B("La gente empezó a detenerse frente al cristal. Primero por curiosidad. Luego… por algo más.",
  S("crowd_window", CROWD, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.25)), fx=["dust"], grade="warm"),
  sfx=[X("whisper", 1.0, -16, dur=5)])
B("Porque la maniquí tenía la cara de la hija de Pascuala.",
  S("window_close", cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.55), "in"), fx=[PU(80, 0.08)], grade="cold"),
  S("face_flash", tr="flash", tl=0.12, dur=1.2, fx=[SH(0, 0.5, 9)]),
  sfx=[X("riser", -2.5, -9, at_scene=1, dur=2.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -4, at_scene=1)], pause=0.8)
B("Los mismos ojos. La misma boca. La misma forma de inclinar la cabeza.",
  S("eyes_close", cam=((0.4, 0.5, 1.3), (0.6, 0.5, 1.3), "linear"), fx=["dust"], grade="moon"))
B("Las señoras del barrio se persignaban al pasar. Y una de ellas, la que había vestido a la novia el día de la boda, dijo lo que todos estaban pensando.",
  S("gossip", cam=((0.4, 0.55, 1.05), (0.55, 0.5, 1.25), "linear"), fx=["dust"], grade="warm"))
B("Esa no es una muñeca. Es ella.",
  S("gossip", cam=((0.5, 0.45, 1.35), (0.5, 0.45, 1.5)), fx=["dust"], grade="cold"), **EMP)

# ======================================================================== IV
B("Y como la maniquí se parecía tanto a la dueña, la ciudad le dio un nombre que nunca se le quitó: la Pascualita.",
  S("shop_front", MANQ, WING, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=["dust"], grade="night"))
B("Pascuala lo negó siempre. Decía que la había mandado traer de Francia. Que era solo una maniquí muy fina, hecha por artesanos.",
  S("mother_portrait", CANDLE, cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|La novia del aparador", "chapter", 0.6, 4.8)]), music="mystery")
B("Es una maniquí. Nada más.",
  S("mother_portrait", CANDLE, cam=((0.5, 0.42, 1.4), (0.5, 0.42, 1.55)), fx=[FL], grade="cold"), **MOM)
B("Pero los que se acercaban al cristal veían cosas que ninguna maniquí debería tener. Las líneas en las palmas. Las grietas finas en la punta de los dedos, como huellas digitales.",
  S("hand_close", cam=((0.45, 0.5, 1.05), (0.55, 0.5, 1.25), "in"), fx=["dust"], grade="moon"),
  sfx=[X("heartbeat", 0.5, -12, dur=8, bpm=70)])
B("Pestañas una por una. Un cabello oscuro que, dicen, era cabello de verdad. Y una piel que no parecía de cera ni de yeso… sino de alguien que acaba de quedarse dormida.",
  S("eyes_close", cam=((0.5, 0.45, 1.2), (0.5, 0.45, 1.5), "in"), fx=["dust"], grade="moon", w=1.0),
  S("window_close", WING, cam=((0.5, 0.45, 1.25), (0.5, 0.45, 1.4)), fx=["dust"], grade="moon", tr="xfade", tl=0.8, w=1.0))
B("Cuentan que un fotógrafo llegó una tarde con su cámara para retratarla de cerca. Disparó un rollo entero. Y cuando reveló las fotos, en todas… la Pascualita tenía los ojos cerrados.",
  S("photographer", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="sepia", w=1.3),
  S("white_flash", tr="flash", tl=0.1, dur=0.5),
  S("eyes_shut", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.4), "in"), fx=[PU(60, 0.05)], grade="bw", w=1.0),
  sfx=[X("sting", 0.0, -6, at_scene=2), X("boom", 0.0, -8, at_scene=1)])
B("Con los años, las empleadas de La Popular empezaron a contar cosas.",
  S("shop_interior", LAMP, cam=((0.6, 0.5, 1.2), (0.4, 0.5, 1.3), "linear"), fx=["dust"], grade="night"))
B("Que cuando le cambiaban el vestido, lo hacían detrás de una cortina, para que nadie viera su cuerpo. Que ninguna quería hacerlo sola. Que las manos de la maniquí no se sentían frías… sino tibias.",
  S("curtain", LAMP, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust", FL], grade="candle"),
  sfx=[X("whisper", 2.0, -14, dur=4)])
B("Yo le estaba acomodando el velo… y sentí que me miraba.",
  S("curtain", cam=((0.5, 0.45, 1.35), (0.5, 0.45, 1.5)), fx=[FL, PU(70, 0.05)], grade="cold"), **EMP)
B("Decían que por las mañanas la encontraban en otra posición. Una mano más arriba. La cabeza un poco ladeada. Como si en la noche… se hubiera movido.",
  S("window_close", WING, cam=((0.5, 0.45, 1.1), (0.5, 0.45, 1.3)), fx=["dust"], grade="moon", w=1.0),
  S("window_turned", WING, cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.45)), fx=[FOG], grade="cold", tr="xfade", tl=0.3, w=1.0),
  music="dread", sfx=[X("sting", 0.0, -8, at_scene=1)])
B("Y los que pasaban de noche frente al aparador aseguraban que sus ojos los seguían. De un lado al otro de la banqueta.",
  S("street_chih", WALKER, LAMP, cam=((0.4, 0.55, 1.2), (0.6, 0.55, 1.3), "linear"), fx=[FOGL], grade="night", w=1.0),
  S("eyes_close", cam=((0.45, 0.5, 1.35), (0.55, 0.5, 1.45), "linear"), fx=[PU(70, 0.06)], grade="cold", w=1.0),
  sfx=[X("footsteps", 0.0, -10, dur=6)])
B("Hubo hombres que se enamoraron de ella. Que iban todas las noches a verla a través del cristal… y que, dicen, terminaron perdiendo la razón.",
  S("man_window", WING, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL], grade="night"))

# ======================================================================== V
B("Hay otra versión, la más extraña de todas. Dicen que años después llegó a Chihuahua un mago francés, de capa negra y sombrero de copa.",
  S("magician", cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FOG, FL], grade="night", tr="fade", tl=1.0,
    text=[T("CAPÍTULO V|El mago francés", "chapter", 0.6, 4.8)]), music="mystery")
B("Que se paró frente al aparador una noche entera, sin moverse. Y que al amanecer, entró a la tienda y habló a solas con Pascuala.",
  S("man_window", WING, cam=((0.5, 0.5, 1.2), (0.5, 0.48, 1.4), "in"), fx=[FOGL], grade="cold"))
B("Nadie supo qué le dijo. Pero desde entonces, cuentan, cada noche, cuando la ciudad duerme, el mago conoce el secreto para despertarla.",
  S("back_room", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=[FL], grade="candle"))
B("Y la novia sale del aparador. Camina por las calles vacías del centro con su vestido blanco. Va a bailar. Va a cenar. Vive la noche que nunca tuvo.",
  S("street_chih", GHOSTB, LAMP, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL], grade="moon", w=1.0),
  S("ballroom", DANCE, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=["dust"], grade="candle", tr="xfade", tl=1.0, w=1.0),
  sfx=[X("whisper", 1.0, -16, dur=4)])
B("Y antes de que salga el sol, vuelve a su lugar detrás del cristal. Con las manos juntas. Con los ojos abiertos. Esperando.",
  S("window_close", WING, cam=((0.5, 0.45, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="cold"), music="dread")
B("También dicen que las novias que compran el vestido que ella lleva puesto tienen un matrimonio largo y feliz. Como si la Pascualita les regalara la boda que a ella le quitaron.",
  S("shop_interior", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25)), fx=["dust"], grade="warm"), music="hope")

# ======================================================================== HISTORIA
B("Ahora, lo que sí sabemos. La tienda existe. La Popular, en la esquina de Victoria y Ocampo, en el centro de Chihuahua. Y la maniquí apareció en su aparador en marzo de mil novecientos treinta.",
  S("street_today", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="none", tr="fade", tl=1.0,
    text=[T("LO QUE DICE LA HISTORIA|", "chapter", 0.6, 4.6)]), music="mystery", amb=["city"])
B("La dueña de entonces se llamaba Pascuala Esparza, y la gente notó que la maniquí se le parecía. De ahí el nombre: la Pascualita.",
  S("archive", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FL], grade="candle"))
B("Hay quien dice que al principio la llamaban la Chonita, y que fue la gente de la calle la que, poco a poco, le cambió el nombre.",
  S("crowd_window", CROWD, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.3)), fx=["dust"], grade="sepia"))
B("Pero no hay ningún documento que confirme la muerte de una hija el día de su boda. Ni siquiera hay acuerdo en la causa: unos dicen que fue una viuda negra, otros que fue un alacrán.",
  S("archive", CANDLE, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.45)), fx=[FL], grade="candle", w=1.0),
  S("spider_close", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.35)), fx=["dust"], grade="night", tr="xfade", tl=0.8, w=0.8))
B("La explicación más sencilla es que se trata de una maniquí de gran calidad, de las que se fabricaban en Europa en esa época, con ojos de vidrio y pelo natural.",
  S("window_close", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=["dust"], grade="warm"))
B("Durante más de noventa años estuvo en ese aparador, y se volvió una de las leyendas más famosas del norte de México. En tiempos recientes, según algunos reportes, ya no siempre se exhibe… lo que solo hace crecer el misterio.",
  S("shop_front", WING, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL], grade="night"))
B("Si algún día la ves, mírala con respeto. Detrás de la leyenda, al final, hay una historia de amor de una madre.",
  S("mother_grief", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.35)), fx=[FL], grade="candle"), music="calm")

# ======================================================================== PAYOFF
B("Pero ¿qué hay debajo de ese vestido? Cuentan que una sola persona lo supo de verdad: la empleada más vieja de La Popular, la que la vistió durante cuarenta años.",
  S("curtain", LAMP, cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.35), "in"), fx=[FL], grade="candle", tr="fade", tl=1.0),
  music="dread", amb=["night", {"name": "wind", "gain": -8}])
B("Antes de morir, dicen, solo dijo una cosa. Que cada vez que le quitaba los zapatos, encontraba en las suelas tierra fresca del desierto.",
  S("shoes", cam=((0.5, 0.55, 1.1), (0.5, 0.6, 1.45), "in"), fx=["dust"], grade="cold"),
  sfx=[X("heartbeat", 0.0, -9, dur=9, bpm=80)])
B("Como si cada noche… alguien saliera a caminar.",
  S("street_chih", VEILW, LAMP, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.5), "in"), fx=[FOGL], grade="cold", w=1.4),
  S("face_flash", tr="flash", tl=0.1, dur=1.4, fx=[SH(0, 0.5, 10)]),
  sfx=[X("riser", -3.0, -8, at_scene=1, dur=3), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -2, at_scene=1)], pause=0.8)
B("Todavía estoy esperando.",
  S("eyes_close", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.45)), fx=[FOG], grade="cold"), pause=1.2, **GHO)
B("Y tú, ¿crees que la Pascualita es solo una maniquí? ¿Te atreverías a pasar de noche frente a su aparador? Te leo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOG], tr="fade", tl=0.8), music="mystery")
B("En el próximo video conocerás a un hombrecito de sombrero enorme que recorre los pueblos de noche, montado en su caballo negro, buscando muchachas de cabello largo para trenzarles el pelo. Lo llaman El Sombrerón.",
  S("sombreron", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOG], grade="night",
    text=[T("PRÓXIMO VIDEO|El Sombrerón", "big", 2.0, 7.0)]), sfx=[X("hooves", 1.0, -12, dur=6, distance=0.6)])
B("Hasta la próxima leyenda. Y si alguna noche una novia te mira desde un aparador… no le sostengas la mirada.",
  S("window_close", WING, GHOSTB, cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.45), "in"), fx=[FOGL], grade="moon", out=2.0), pause=1.0, music="dread")

# --- second shots for long beats (keeps every shot under ~10 s)
EXTRA = {
 "b008": S("hand_close", cam=((0.35, 0.55, 1.2), (0.42, 0.55, 1.35)), fx=["dust"], grade="cold", tr="xfade", tl=0.6),
 "b007": S("window_close", WING, cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.4), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.8),
 "b012": S("plaza_couple", cam=((0.45, 0.55, 1.1), (0.55, 0.5, 1.25)), fx=["dust"], grade="warm", tr="xfade", tl=0.8),
 "b014": S("bouquet", cam=((0.5, 0.45, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.8),
 "b017": S("daughter_portrait", cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.4), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.8),
 "b033": S("daughter_bride", cam=((0.5, 0.4, 1.4), (0.5, 0.4, 1.7), "in"), fx=[FOG, PU(110, 0.1)], grade="cold", tr="xfade", tl=0.6),
 "b038": S("street_chih", WALKER, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.4), "in"), fx=[FOGL], grade="cold", tr="xfade", tl=0.8),
 "b042": S("back_door", cam=((0.62, 0.65, 1.5), (0.64, 0.62, 1.7), "in"), fx=[FOGL], grade="night", tr="xfade", tl=0.6),
 "b053": S("hand_close", cam=((0.68, 0.55, 1.2), (0.72, 0.55, 1.35)), fx=["dust"], grade="moon", tr="xfade", tl=0.6),
 "b057": S("window_close", cam=((0.5, 0.5, 1.3), (0.5, 0.55, 1.5)), fx=[FL], grade="candle", tr="xfade", tl=0.8),
 "b067": S("daughter_bride", CANDLE, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3)), fx=[FL], grade="warm", tr="xfade", tl=1.0),
 "b068": S("shop_day", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=["dust"], grade="none", tr="xfade", tl=0.8),
 "b073": S("crowd_window", CROWD, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.3)), fx=["dust"], grade="sepia", tr="xfade", tl=0.8),
 "b075": S("eyes_close", cam=((0.5, 0.55, 1.2), (0.5, 0.6, 1.4)), fx=[FOG], grade="cold", tr="xfade", tl=0.8),
 "b080": S("sombreron", cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.6), "in"), fx=[FOG], grade="night", tr="xfade", tl=0.8),
 "b081": S("shop_front", WING, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.0), "out"), fx=[FOGL], grade="night", tr="xfade", tl=0.8),
}
for b in BEATS:
    if b["id"] in EXTRA:
        last = b["scenes"][-1]
        ex = EXTRA[b["id"]]
        if "text" in last and b["id"] in ("b080",):
            pass
        if "out" in last:  # keep the fade-out on the final shot
            ex["out"] = last.pop("out"); ex["out_len"] = last.pop("out_len")
        b["scenes"].append(ex)

VARIANTS = {"window_close": ["window_close", "window_reflect", "window_waist", "window_dress2"],
            "street_chih": ["street_chih", "street_chih2", "street_chih3"], "eyes_close": ["eyes_close", "eyes_side"],
            "shop_front": ["shop_front", "shop_fog"], "mother_portrait": ["mother_portrait", "mother_dark"],
            "daughter_bride": ["daughter_bride", "daughter_veil"]}
_cnt = {}
for b in BEATS:
    for sc in b["scenes"]:
        n = sc["layers"][0]["src"][4:-4]
        if n in VARIANTS:
            k = _cnt.get(n, 0); _cnt[n] = k + 1
            sc["layers"][0]["src"] = f"art/{VARIANTS[n][k % len(VARIANTS[n])]}.png"

# resolve sfx relative to a scene (needs audio/timeline.json from tts.py)
TL = os.path.join(HERE, "audio", "timeline.json")
if os.path.exists(TL):
    tl = json.load(open(TL)); tb = tl["beats"]
    for i, b in enumerate(BEATS):
        if i >= len(tb): break
        end = tb[i + 1]["start"] if i + 1 < len(tb) else tl["duration"] + 5.0
        d = end - tb[i]["start"]; sc = b["scenes"]
        fixed = sum(s.get("dur", 0) for s in sc); wsum = sum(s.get("weight", 1) for s in sc if "dur" not in s) or 1
        offs = []; t = 0.0
        for s in sc:
            offs.append(t); t += s["dur"] if "dur" in s else max(0, d - fixed) * s.get("weight", 1) / wsum
        for c in b.get("sfx", []):
            if "scene" in c:
                c["at"] = round(offs[c["scene"]] + c["at"], 3)

story = {"title": "La Pascualita", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "D", "seed": 73, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# La Pascualita — guion\n",
                  "Narración en español (narrador: em_alex; Pascuala, la hija y la empleada: ef_dora).\n"]
WHO = {"ef_dora": "VOZ FEMENINA: "}
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
