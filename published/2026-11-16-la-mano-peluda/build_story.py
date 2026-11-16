#!/usr/bin/env python3
"""Builds story.json and script.md for 'La Mano Peluda'. Edit BEATS here, then run."""
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
RAIN = {"type": "rain", "strength": 0.35}
def SH(a, b, amp=7): return {"type": "shake", "amp": amp, "at": [a, b]}
def LI(*t): return {"type": "lightning", "at": list(t)}
CANDLE = L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 2.0}])
HAND_IN = L("l_hand_reach", depth=1.05, anim=[{"type": "drift", "dx": -0.05, "dy": -0.03, "ease": "out"}])
HAND_CRAWL = L("l_hand_crawl", depth=1.08, anim=[{"type": "drift", "dx": -0.10, "ease": "linear"}, {"type": "float", "amp": 0.004, "period": 0.7}])
WIN_RAIN = L("l_window_rain", blend="screen", opacity=[0, 0.7], anim=[{"type": "drift", "dy": 0.05, "ease": "linear"}])
COINS = L("l_coins", blend="screen", anim=[{"type": "drift", "dy": 0.06, "ease": "linear"}, {"type": "flicker", "amp": 0.2, "speed": 1.2}])

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)

ABU = dict(voice="ef_dora", speed=0.80)
PAN = dict(voice="em_santa", speed=0.80)
MANO = dict(voice="em_santa", speed=0.70, fx="eco")

# ======================================================================== COLD OPEN
B("Tres de la mañana. Una casona vieja de Puebla. Un niño duerme… con el brazo colgando fuera de la cama.",
  S("bedroom_wide", CANDLE, cam=((0.5, 0.5, 1.05), (0.42, 0.6, 1.35), "in"), fx=[FL, "dust"], grade="night", tr="fade", tl=1.2),
  pre=0.4, music="dread", amb=["night", {"name": "clock", "gain": -8}])
B("Debajo del colchón, en esa oscuridad donde nunca llega la luz… algo se mueve.",
  S("bed_arm", cam=((0.5, 0.45, 1.2), (0.5, 0.55, 1.5), "in"), fx=[FOG]),
  S("under_bed", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.4), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  sfx=[X("whisper", 2.0, -12, at_scene=1, dur=3)])
B("Primero, un roce. Pelo áspero… en las yemas de los dedos.",
  S("hand_under", cam=((0.45, 0.6, 1.25), (0.42, 0.55, 1.6), "in"), fx=[FOGL]),
  sfx=[X("heartbeat", 0.5, -8, dur=7, bpm=78)])
B("Y entonces… una mano lo toma de la muñeca.",
  S("hand_under", cam=((0.42, 0.55, 1.6), (0.42, 0.55, 1.7)), fx=[FOGL], w=0.6),
  S("hand_grab", tr="flash", tl=0.12, dur=2.0, cam=((0.5, 0.5, 1.35), (0.5, 0.5, 1.6)), fx=[SH(0, 0.6, 9)], grade="night"),
  pause=0.8, sfx=[X("sting", -0.1, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("LA MANO PELUDA|nunca dejes el brazo fuera de la cama", "title", 0.6, 6.4)]),
  pause=5.0, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("A la mañana siguiente, su abuela encontró la cama vacía. Y lo que el niño traía apretado en el puño… todavía se cuenta en voz baja en Puebla.",
  S("bed_empty", cam=((0.5, 0.5, 1.1), (0.5, 0.55, 1.35), "in"), fx=["dust"], grade="cold"),
  S("fist_closed", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.55), "in"), fx=["dust"], grade="cold", tr="xfade", tl=0.6),
  music="tension", amb=["night", {"name": "wind", "gain": -6}])
B("Esta es la leyenda de la Mano Peluda. Y antes de que termine, vas a saber qué era… y por qué esa mano sigue regresando.",
  S("hand_crawl_street", HAND_CRAWL, cam=((0.5, 0.6, 1.2), (0.45, 0.6, 1.4)), fx=[FOGL], grade="moon"))

# ======================================================================== I
B("Julián tenía diez años cuando sus papás lo mandaron a pasar el verano con su abuela Refugio, en Puebla de los Ángeles. Era de la Ciudad de México, hijo único, y nunca había dormido lejos de su casa.",
  S("puebla_road", cam=((0.5, 0.5, 1.05), (0.55, 0.5, 1.25)), fx=["dust"], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO I|Las tres reglas", "chapter", 0.6, 5.0)]),
  S("julian_portrait", cam=((0.5, 0.42, 1.15), (0.5, 0.4, 1.35)), fx=["dust"], grade="warm", tr="xfade", tl=0.8,
    text=[T("Puebla, verano de 1962|el centro histórico", "date", 0.5, 4.5)]), music="calm", amb=["city"])
B("La casa estaba en una calle empedrada, cerca de la catedral. Fachada de azulejos de talavera, balcones de hierro, y un zaguán tan grande que por ahí, decían, entraban antes los carruajes.",
  S("puebla_street", cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=["dust"], grade="warm"),
  S("zaguan", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.35), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("Adentro, un patio con macetas de geranios, una fuente seca… y cuartos altísimos, con vigas de madera negra y olor a humedad.",
  S("patio_day", cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="warm"))
B("La abuela Refugio era una mujer pequeña, de rebozo gris y trenzas blancas. Lo recibió con chocolate caliente y pan de dulce. Pero esa primera noche, antes de apagar la vela, se sentó en la orilla de su cama y le dijo algo que Julián nunca olvidó.",
  S("abuela_portrait", CANDLE, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3)), fx=[FL], grade="candle"),
  S("abuela_bedside", CANDLE, cam=((0.5, 0.5, 1.1), (0.45, 0.5, 1.35), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8),
  music="mystery", amb=["night", {"name": "crickets", "gain": -8}])
B("Mijo, aquí hay tres reglas. Nunca dejes el brazo fuera de la cama. Nunca saques el pie. Y si se te cae algo de noche… ahí se queda hasta que salga el sol.",
  S("abuela_close", CANDLE, cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.55), "in"), fx=[FL], grade="candle",
    text=[T("Nunca dejes el brazo fuera de la cama|abuela Refugio", "quote", 1.0, 6.0)]), **ABU)
B("Julián se rio. Tenía diez años, no cinco. Le preguntó por qué.",
  S("julian_bed", CANDLE, cam=((0.5, 0.5, 1.15), (0.5, 0.48, 1.3)), fx=[FL], grade="candle"))
B("Porque en esta casa… cobra la Mano Peluda.",
  S("abuela_close", CANDLE, cam=((0.5, 0.42, 1.55), (0.5, 0.4, 1.75), "in"), fx=[FL], grade="candle"),
  pause=1.0, sfx=[X("sting", 2.2, -6)], **ABU)
B("Ella apagó la vela y se fue. Y en la oscuridad, Julián escuchó algo que no supo explicar. Debajo de las tablas del piso… algo rascaba. Despacio. Como uñas largas contra la madera.",
  S("candle_smoke", cam=((0.5, 0.5, 1.3), (0.5, 0.45, 1.5), "in"), fx=["dust"], grade="night", w=0.6),
  S("floor_scratch", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.5), "in"), fx=[FOGL], grade="night", tr="xfade", tl=0.6, w=1.4),
  music="dread", amb=["night", {"name": "clock", "gain": -8}], sfx=[X("whoosh", 0.4, -12), X("whisper", 6.0, -10, dur=4)])
B("Se tapó hasta la cabeza. Y por primera vez en su vida… durmió hecho bolita, con las manos bien metidas bajo la cobija.",
  S("julian_covers", cam=((0.5, 0.5, 1.1), (0.5, 0.52, 1.35), "in"), fx=[FOG], grade="night", out=0.8))

# ======================================================================== II
B("En la mañana, cuando se agachó a buscar sus huaraches, vio algo en las tablas, debajo de la cama. Cinco rayas largas, paralelas, frescas. Como si alguien hubiera arañado el piso… desde abajo.",
  S("floor_scratch", cam=((0.5, 0.5, 1.3), (0.52, 0.5, 1.6), "in"), fx=["dust"], grade="cold"),
  pause=0.8, sfx=[X("sting", 8.0, -6)])
B("Al día siguiente, mientras molía el chile para el mole en el metate, la abuela le contó de dónde venía esa mano. Y como en toda buena leyenda… hay más de una versión.",
  S("kitchen_day", cam=((0.5, 0.5, 1.05), (0.5, 0.52, 1.3), "in"), fx=["dust", "embers"], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|Lo que cuentan", "chapter", 0.6, 5.0)]), music="mystery", amb=["room", {"name": "fire", "gain": -10}])
B("La más antigua nos lleva a los tiempos de la Colonia, cuando en la Nueva España funcionaba el Tribunal del Santo Oficio, la Inquisición, establecido en la capital del virreinato en mil quinientos setenta y uno.",
  S("virreinato_plaza", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="sepia",
    text=[T("Nueva España, siglos de la Colonia|el Santo Oficio llegó en 1571", "date", 0.5, 5.0)]), amb=["wind"])
B("Cuentan que un hombre pobre fue acusado de robar en la casa de un señor muy rico. Él juró que era inocente. Nadie le creyó.",
  S("accused", cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.35), "in"), fx=[FL, "dust"], grade="candle"))
B("El castigo fue terrible: le cortaron la mano. Y poco después, el hombre murió… y lo enterraron sin nombre, en un camposanto a las afueras.",
  S("block_axe", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.45), "in"), fx=[FL], grade="candle", w=0.8),
  S("camposanto", cam=((0.5, 0.55, 1.1), (0.55, 0.55, 1.3)), fx=[FOGL], grade="moon", tr="xfade", tl=0.8),
  sfx=[X("boom", 0.6, -6), X("bell", 6.0, -10, freq=160)])
B("Pero dicen que antes de morir hizo un juramento: que su mano volvería a buscar a los que lo acusaron. Y que nunca descansaría.",
  S("camposanto", cam=((0.55, 0.55, 1.3), (0.5, 0.6, 1.55), "in"), fx=[FOGL], grade="moon"),
  music="tension")
B("Desde entonces, la mano camina sola. Grande, el doble que la de un hombre. Negra, cubierta de pelo duro, con uñas largas y amarillas. Sale de las grietas, de debajo de las puertas… y de debajo de las camas.",
  S("hand_portrait", cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.35), "in"), fx=[FOG], grade="night",
    text=[T("LA MANO|el doble que la de un hombre", "big", 2.0, 5.0)]),
  S("door_gap", cam=((0.5, 0.6, 1.2), (0.5, 0.65, 1.45), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  S("hand_scare", tr="flash", tl=0.12, dur=1.6, cam=((0.5, 0.5, 1.4), (0.5, 0.5, 1.6)), fx=[SH(0, 0.5, 8)]),
  sfx=[X("sting", -0.1, -3, at_scene=2), X("boom", 0.0, -4, at_scene=2)])
B("Algunos dicen que deja un rastro de tierra mojada por donde pasa. Otros, que también sale de las paredes, y por eso nunca hay que dormir pegado al muro. Y en Colombia, donde también se cuenta, aseguran que sus uñas están envenenadas.",
  S("hand_portrait", cam=((0.5, 0.48, 1.35), (0.5, 0.45, 1.6), "in"), fx=[FOG], grade="night"),
  S("door_gap", cam=((0.5, 0.65, 1.45), (0.5, 0.65, 1.2), "out"), fx=[FOGL], tr="xfade", tl=0.6))
B("Pero la abuela Refugio conocía otra versión. La de Puebla.",
  S("abuela_portrait", CANDLE, cam=((0.5, 0.42, 1.25), (0.5, 0.4, 1.45), "in"), fx=[FL], grade="candle"), music="mystery")
B("Hace más de cien años, contaba, cerca del mercado, había una casa de empeño. El dueño era un hombre bajito, gordo… y tan velludo que hasta los dedos tenía cubiertos de pelo negro. Le decían el Peludo.",
  S("empeno_ext", cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=["dust"], grade="sepia"),
  S("peludo_portrait", CANDLE, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.4), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8,
    text=[T("EL PELUDO", "big", 3.0, 6.0)]), amb=["room", {"name": "clock", "gain": -10}], sfx=[X("coins", 1.0, -8, at_scene=1)])
B("Era cruel. Prestaba poco y cobraba mucho. Si alguien se atrasaba un día, se quedaba con todo: el anillo de bodas, la máquina de coser, la cobija del niño enfermo.",
  S("empeno_int", CANDLE, cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.2), "linear"), fx=[FL, "dust"], grade="candle"),
  S("peludo_hands", CANDLE, cam=((0.5, 0.55, 1.25), (0.5, 0.55, 1.5), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  sfx=[X("coins", 4.0, -8)])
B("Y la gente, al salir de su tienda, le decía en voz baja: que Dios te seque esa mano.",
  S("empeno_woman", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=[FOGL, RAIN], grade="moon",
    text=[T("Que Dios te seque esa mano|lo que decía la gente", "quote", 2.5, 6.5)]), amb=["rain"])
B("Cuando el Peludo murió, nadie fue a su entierro. Ni un vecino, ni un cura. Pero semanas después, el panteonero contó algo que hizo temblar a media ciudad.",
  S("panteon", cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.3), "in"), fx=[FOGL], grade="moon"),
  S("panteonero", L("l_lantern_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.6}]),
    cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=[FOG], grade="moon", tr="xfade", tl=0.8),
  amb=["night", {"name": "wind", "gain": -6}], sfx=[X("owl", 2.0, -10)])
B("De su tumba sale una mano. Peluda. Rasca la tierra desde adentro… y se va caminando sobre los dedos, rumbo a la ciudad.",
  S("panteonero", L("l_lantern_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.6}]),
    cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.55), "in"), fx=[FOG], grade="moon", w=0.8),
  S("grave_hand", cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.45), "in"), fx=[FOGL], grade="moon", tr="xfade", tl=0.6),
  music="tension", **PAN)
B("Dicen que la mano sigue cobrando. Que todavía busca lo que le deben. Y que entra a las casas de noche, cuando todos duermen… y se lleva lo primero que encuentra fuera de la cama.",
  S("hand_crawl_street", HAND_CRAWL, cam=((0.5, 0.6, 1.15), (0.45, 0.6, 1.35)), fx=[FOGL], grade="moon"),
  S("hand_scare", tr="flash", tl=0.12, dur=1.6, cam=((0.5, 0.45, 1.45), (0.5, 0.45, 1.65)), fx=[SH(0, 0.5, 8)]),
  pause=0.8, sfx=[X("sting", -0.1, -3, at_scene=1), X("boom", 0.0, -4, at_scene=1)])
B("Si te gustan estas historias, suscríbete y activa la campanita. Aquí te contamos las leyendas de México… con la luz apagada.",
  S("title_bg", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.2)), fx=[FOG], grade="night", tr="fade", tl=0.6), music="mystery")

# ======================================================================== III
B("Esa noche llovió. Truenos sobre las cúpulas, agua corriendo por las canaletas del patio. Y Julián, por terco, dejó junto a la cama una canica de vidrio. La azul. Su favorita.",
  S("storm_domes", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.2)), fx=[RAIN, LI(1.5, 4.5)], grade="cold", tr="fade", tl=1.0,
    text=[T("CAPÍTULO III|La canica", "chapter", 0.6, 5.0)]),
  S("marble_bed", cam=((0.5, 0.55, 1.2), (0.5, 0.58, 1.45), "in"), fx=[FOGL], grade="night", tr="xfade", tl=0.6),
  music="tension", amb=["rain", {"name": "wind", "gain": -8}], sfx=[X("thunder", 1.4, -3)])
B("A medianoche, la canica rodó. Sola. Tac… tac… tac… sobre las tablas. Y se detuvo justo debajo de la cama.",
  S("marble_floor", cam=((0.3, 0.6, 1.3), (0.6, 0.6, 1.3), "linear"), fx=[FOGL], grade="night"),
  sfx=[X("knock", 2.8, -10, times=3)])
B("Julián se asomó por la orilla. Estaba ahí, brillando apenas, al alcance de la mano. Solo tenía que estirar el brazo.",
  S("julian_peek", cam=((0.5, 0.45, 1.15), (0.5, 0.45, 1.4), "in"), fx=[FOG], grade="night"),
  S("marble_under", cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.5), "in"), fx=[FOGL], grade="night", tr="xfade", tl=0.6),
  sfx=[X("heartbeat", 1.0, -9, dur=8, bpm=84)])
B("Y entonces recordó la tercera regla. Si se te cae algo de noche… ahí se queda.",
  S("abuela_close", CANDLE, cam=((0.5, 0.42, 1.4), (0.5, 0.42, 1.55)), fx=[FL], grade="candle", vig=0.75))
B("Se quedó quieto. Y en ese momento, desde la oscuridad, otra cosa se acercó a la canica. Algo negro, lento, con cinco patas largas… que no eran patas.",
  S("marble_under", HAND_IN, cam=((0.5, 0.55, 1.4), (0.52, 0.55, 1.6), "in"), fx=[FOGL], grade="night"),
  music="dread", sfx=[X("whisper", 2.0, -10, dur=4)])
B("Eran dedos. La mano tomó la canica… y se la llevó de vuelta a la oscuridad.",
  S("hand_marble", tr="flash", tl=0.12, cam=((0.5, 0.5, 1.35), (0.5, 0.5, 1.55)), fx=[SH(0, 0.5, 7)], grade="night", w=1.0),
  S("under_bed", cam=((0.5, 0.55, 1.4), (0.5, 0.55, 1.2), "out"), fx=[FOGL], grade="night", tr="xfade", tl=0.6, out=0.8),
  pause=1.0, sfx=[X("sting", -0.1, -3), X("boom", 0.0, -4)])
B("Al día siguiente Julián no dijo nada. Pero esa mañana, recorriendo la casa, notó algo en cada cuarto: todas las camas estaban lejos de las paredes. Y ninguna tenía nada debajo. Ni una caja. Ni un zapato. Nada que una mano pudiera agarrar.",
  S("bedroom_day", cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=["dust"], grade="warm", tr="fade", tl=0.8), music="sad", amb=["room"])
B("Esa tarde, buscando un trompo en el ropero de la abuela, encontró una fotografía vieja: dos niños en el patio de esa misma casa. Una niña de trenzas… y un niño un poco más grande.",
  S("patio_day", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.3)), fx=["dust"], grade="warm", w=0.6),
  S("old_photo", cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.4), "in"), fx=["dust"], grade="sepia", tr="xfade", tl=0.8),
  )
B("La abuela la tomó con las manos temblorosas.",
  S("abuela_photo", cam=((0.5, 0.45, 1.15), (0.5, 0.45, 1.35), "in"), fx=["dust"], grade="warm"))
B("Esa soy yo. Y ese es mi hermano Chucho. Él tampoco creía en las reglas.",
  S("abuela_photo", cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.55), "in"), fx=["dust"], grade="warm"), **ABU)
B("Le contó que una noche Chucho durmió con el brazo afuera. Que a la mañana siguiente lo encontraron en el patio, sentado junto a la fuente, con la mirada perdida. Y que desde ese día… nunca volvió a hablar.",
  S("chucho_fountain", cam=((0.5, 0.5, 1.05), (0.5, 0.52, 1.35), "in"), fx=[FOGL], grade="sepia"),
  music="dread", sfx=[X("bell", 5.0, -12, freq=140)])
B("En su muñeca, dijo la abuela, tenía cinco marcas moradas. Como dedos.",
  S("wrist_marks", cam=((0.5, 0.5, 1.25), (0.5, 0.5, 1.55), "in"), fx=["dust"], grade="sepia",
    text=[T("CINCO MARCAS|como dedos", "big", 2.0, 5.5)]), pause=1.0, sfx=[X("sting", 2.0, -5)])

# ======================================================================== IV
B("La tercera noche, la tormenta tumbó la luz en todo el barrio. La abuela le dejó una vela en el buró… y algo más. Una moneda de plata, vieja, debajo de la almohada.",
  S("storm_domes", cam=((0.55, 0.45, 1.2), (0.5, 0.5, 1.05), "out"), fx=[RAIN, LI(0.8, 3.0)], grade="cold", tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|La moneda", "chapter", 0.6, 5.0)], w=0.8),
  S("coin_pillow", CANDLE, cam=((0.5, 0.5, 1.2), (0.5, 0.52, 1.5), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8),
  music="tension", amb=["rain", {"name": "wind", "gain": -6}], sfx=[X("thunder", 0.7, -3)])
B("Si te agarra, mijo, no jales. Ábrele la mano y dale la moneda. Lo único que quiere es cobrar.",
  S("abuela_bedside", CANDLE, cam=((0.45, 0.48, 1.3), (0.42, 0.45, 1.5), "in"), fx=[FL], grade="candle",
    text=[T("No jales. Dale la moneda|abuela Refugio", "quote", 1.0, 6.0)]), **ABU)
B("Julián quiso preguntarle cómo sabía eso. Pero la abuela ya había cerrado la puerta. Y por la rendija de abajo, durante un largo rato, se vio la luz de su vela… quieta. Como si ella se hubiera quedado del otro lado, escuchando.",
  S("door_candle", cam=((0.5, 0.55, 1.1), (0.5, 0.62, 1.4), "in"), fx=[FL], grade="candle"))
B("Julián se durmió contando relámpagos. Y en algún momento de la noche, dormido, se dio la vuelta… y su brazo resbaló fuera del colchón.",
  S("bedroom_wide", CANDLE, WIN_RAIN, cam=((0.5, 0.5, 1.1), (0.42, 0.58, 1.4), "in"), fx=[FL, LI(2.0)], grade="night"),
  S("bed_arm", cam=((0.5, 0.45, 1.2), (0.5, 0.55, 1.45), "in"), fx=[FOG], tr="xfade", tl=0.6),
  music="dread", amb=["rain", {"name": "clock", "gain": -8}])
B("La vela se apagó.",
  S("candle_smoke", cam=((0.5, 0.5, 1.4), (0.5, 0.45, 1.6), "in"), fx=["dust"], grade="night"),
  pre=0.4, pause=1.2, music="silence", sfx=[X("whoosh", 0.2, -8)])
B("Primero, el roce. Pelo áspero en las yemas de los dedos. Luego, el frío. Un frío de tierra mojada… de tumba.",
  S("hand_under", cam=((0.45, 0.6, 1.3), (0.42, 0.55, 1.65), "in"), fx=[FOGL], grade="night"),
  music="dread", sfx=[X("heartbeat", 0.0, -6, dur=9, bpm=96)])
B("Y la mano lo tomó de la muñeca. Fuerte. Con una fuerza que no era de este mundo.",
  S("hand_grab", tr="flash", tl=0.12, cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.6)), fx=[SH(0, 1.0, 10)], grade="night"),
  sfx=[X("sting", -0.1, -2), X("boom", 0.0, -3)])
B("Jaló. Julián sintió que su hombro bajaba por la orilla de la cama, que el piso ya no estaba ahí, que debajo del colchón había un hueco mucho más grande que el cuarto… un hueco que olía a monedas viejas y a vela apagada.",
  S("julian_pulled", cam=((0.5, 0.45, 1.2), (0.5, 0.55, 1.5), "in"), fx=[FOG, SH(0, 2.0, 5)], grade="night", w=0.9),
  S("abyss", COINS, cam=((0.5, 0.4, 1.0), (0.5, 0.6, 1.5), "in"), fx=[FOG], grade="night", tr="xfade", tl=0.8, w=1.3),
  amb=["drips", {"name": "wind", "gain": -10}], sfx=[X("riser", 3.0, -8, dur=6), X("coins", 9.0, -10)])
B("Y desde el fondo, una voz ronca, como de alguien que habla con la boca llena de tierra:",
  S("abyss", COINS, cam=((0.5, 0.6, 1.5), (0.5, 0.65, 1.75), "in"), fx=[FOG], grade="night"))
B("¿Qué me traes?",
  S("hand_scare", cam=((0.5, 0.48, 1.4), (0.5, 0.48, 1.6), "in"), fx=[FOG, SH(0, 0.4, 5)], grade="night",
    text=[T("¿Qué me traes?", "whisper", 0.3, 3.0)]),
  pre=0.3, pause=1.0, sfx=[X("whisper", 0.0, -8, dur=3)], **MANO)
B("Julián quiso gritar, quiso jalar con todas sus fuerzas. Pero recordó a la abuela. No jales. Con la otra mano buscó debajo de la almohada… y apretó la moneda.",
  S("julian_pulled", cam=((0.5, 0.42, 1.4), (0.5, 0.4, 1.6), "in"), fx=[FOG], grade="night"),
  S("coin_pillow", cam=((0.5, 0.5, 1.5), (0.5, 0.52, 1.7), "in"), fx=[FOG], grade="night", tr="xfade", tl=0.6))
B("Abrió los dedos. Y la dejó caer en esa palma enorme, peluda, helada.",
  S("coin_give", cam=((0.5, 0.45, 1.2), (0.5, 0.5, 1.45), "in"), fx=[FOG], grade="night",
    text=[T("LA MONEDA", "big", 2.5, 5.0)]), pause=0.8)
B("La mano se detuvo. Hubo un silencio largo. Se oyó el tintineo de una moneda contra otras monedas, muy abajo… y la mano lo soltó.",
  S("abyss", COINS, cam=((0.5, 0.6, 1.6), (0.5, 0.5, 1.0), "out"), fx=[FOG], grade="night", out=1.2),
  pause=1.4, music="silence", sfx=[X("coins", 4.0, -6), X("boom", 7.5, -8)])

# ======================================================================== V
B("Lo encontraron al amanecer. No en su cama, sino debajo de ella, dormido sobre las tablas, hecho bolita. La abuela lo sacó de ahí llorando, rezando.",
  S("dawn_room", cam=((0.5, 0.5, 1.05), (0.5, 0.58, 1.35), "in"), fx=["dust"], grade="cold", tr="fade", tl=1.2,
    text=[T("CAPÍTULO V|La deuda", "chapter", 0.6, 5.0)]),
  S("julian_floor", cam=((0.45, 0.78, 1.45), (0.45, 0.8, 1.7), "in"), fx=["dust"], grade="cold", tr="xfade", tl=0.8),
  music="sad", amb=["city", {"name": "wind", "gain": -10}])
B("En la muñeca tenía cinco marcas moradas. Y en el otro puño, apretado con fuerza, traía algo que no era suyo.",
  S("wrist_marks", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=["dust"], grade="cold", w=1.0),
  S("fist_closed", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.6), "in"), fx=["dust"], grade="cold", tr="xfade", tl=0.6),
  music="tension")
B("Un papelito amarillo, frágil, casi deshecho. Una boleta de empeño. Con el nombre de una casa que había cerrado hacía muchísimos años… y el nombre de la mujer que había empeñado ahí su anillo de bodas: la mamá de la abuela Refugio.",
  S("boleta", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.35), "in"), fx=["dust"], grade="sepia",
    text=[T("LA BOLETA", "big", 1.5, 4.5)]), sfx=[X("sting", 13.5, -6)])
B("La abuela se sentó en la cama y lloró en silencio. Su mamá nunca se lo había contado. Fueron años de hambre, dijo. Empeñó el anillo para comprar medicina… y nunca pudo recuperarlo.",
  S("abuela_photo", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.4), "in"), fx=["dust"], grade="cold"), music="sad")
B("La deuda que nadie pagó. La que el Peludo, desde su tumba, seguía viniendo a cobrar a esa casa… noche tras noche.",
  S("peludo_portrait", CANDLE, cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.55), "in"), fx=[FL], grade="candle", w=0.8),
  S("hand_crawl_street", HAND_CRAWL, cam=((0.5, 0.6, 1.15), (0.45, 0.6, 1.35)), fx=[FOGL], grade="moon", tr="xfade", tl=0.6))
B("Julián volvió a su casa al terminar el verano. Creció, se hizo viejo, y contó esta historia muchas veces. Pero siempre la terminaba igual.",
  S("julian_old", CANDLE, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3)), fx=[FL], grade="candle"), music="mystery", amb=["night"])
B("Porque en la boleta, escrito con tinta roja, todavía se alcanzaba a leer… abono uno… de tres.",
  S("boleta_red", cam=((0.5, 0.5, 1.3), (0.55, 0.55, 1.75), "in"), fx=["dust"], grade="sepia",
    text=[T("ABONO 1 DE 3", "big", 4.0, 8.0)]),
  S("hand_scare", tr="flash", tl=0.12, dur=1.8, cam=((0.5, 0.5, 1.45), (0.5, 0.5, 1.7)), fx=[SH(0, 0.6, 9)], out=0.8),
  pause=1.4, music="silence", sfx=[X("sting", -0.1, -3, at_scene=1), X("boom", 0.0, -2, at_scene=1)])
B("Lo que sí es historia es esto: la Mano Peluda es uno de los miedos más compartidos de México, y también de Colombia y de otros países. Generaciones de abuelas la usaron para que los niños no se levantaran de noche.",
  S("abuela_portrait", CANDLE, cam=((0.5, 0.45, 1.05), (0.5, 0.45, 1.2)), fx=[FL], grade="candle", tr="fade", tl=0.8),
  music="calm", amb=["crickets"])
B("Y en mil novecientos noventa y cinco, su nombre se volvió famoso en todo el país: así se llamó un programa de radio nocturno donde la gente llamaba para contar sus experiencias de miedo. Estuvo al aire más de veinte años, y para muchos, escucharlo con la luz apagada era casi un ritual.",
  S("radio_night", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.35), "in"), fx=["dust", FL], grade="candle",
    text=[T("1995|un programa de radio nocturno", "date", 0.8, 5.0)]))
B("Así que esta noche, cuando apagues la luz… revisa dónde quedó tu brazo.",
  S("bed_arm", cam=((0.5, 0.45, 1.2), (0.5, 0.52, 1.45), "in"), fx=[FOG], grade="night"), music="dread")
B("Y tú, ¿de niño te asustaron con la Mano Peluda? ¿Dormías con los pies bien tapados? Cuéntamelo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOG], tr="fade", tl=0.8), music="mystery")
B("En el próximo video nos vamos al centro de la Ciudad de México, a una calle que todavía recuerda a una mujer tan hermosa que, para que nadie más muriera por ella, prefirió perder su belleza. Es la leyenda de la Calle de la Quemada.",
  S("quemada_tease", cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.05)), fx=[FOG, "embers"], grade="night",
    text=[T("PRÓXIMO VIDEO|La Calle de la Quemada", "big", 2.0, 7.0)]), sfx=[X("whisper", 3.0, -12, dur=4)])
B("Hasta la próxima leyenda. Y si de noche sientes un roce en los dedos… no jales.",
  S("under_bed", HAND_IN, cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.4), "in"), fx=[FOGL], out=2.0), pause=1.0, music="dread")

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

story = {"title": "La Mano Peluda: nunca dejes el brazo fuera de la cama", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "E", "seed": 41, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# La Mano Peluda — guion\n",
                  "Narración en español (narrador: em_alex; abuela Refugio: ef_dora; el panteonero y la voz de la mano: em_santa).\n"]
WHO = {"ef_dora": "ABUELA REFUGIO: ", "em_santa": "PERSONAJE: "}
for b in BEATS:
    for sc in b["scenes"]:
        for t in sc.get("text", []):
            if t["style"] in ("chapter", "title"): out.append(f"\n## {t['str'].replace('|', ' — ')}\n")
    if b["text"]:
        out.append(WHO.get(b.get("voice"), "") + b["text"]); words += len(b["text"].split())
open(os.path.join(HERE, "script.md"), "w").write("\n\n".join(out) + "\n")
arts = sorted({l["src"] for b in BEATS for sc in b["scenes"] for l in sc["layers"]})
print(f"beats {len(BEATS)}  scenes {sum(len(b['scenes']) for b in BEATS)}  words {words}  art {len(arts)}")
print(" ".join(a[4:-4] for a in arts))
