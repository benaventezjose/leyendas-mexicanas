#!/usr/bin/env python3
"""Builds story.json and script.md for 'Los Aluxes'. Edit BEATS here, then run."""
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
def SH(a, b, amp=7): return {"type": "shake", "amp": amp, "at": [a, b]}
FIRE = L("l_fire_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.25, "speed": 2.4}])
EYES = L("l_eyes", blend="screen", anim=[{"type": "flicker", "amp": 0.15, "speed": 0.8}])
BEAST_WALK = L("l_beast_walk", depth=1.08, anim=[{"type": "drift", "dx": 0.06, "ease": "linear"}])
LANTERN = L("l_lantern_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.6}])
CANDLE = L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 2.0}])

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)


GEYES = L("l_eyes_gold", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 0.7}])
STONES = L("l_stones", anim=[{"type": "drift", "dy": 0.10, "ease": "in"}])
CORN = L("l_corn_fg", depth=1.35, anim=[{"type": "sway", "deg": 1.4, "period": 6, "pivot": [0.5, 1.0]}])
BRUSH = L("l_brush_fg", depth=1.35, anim=[{"type": "sway", "deg": 1.2, "period": 7, "pivot": [0.5, 1.0]}])
ALUXW = L("l_alux_walk", depth=1.08, anim=[{"type": "drift", "dx": 0.05, "ease": "linear"}])
COPAL = L("l_copal", blend="screen", opacity=[0, 0.75], fade_in=2.0, anim=[{"type": "drift", "dy": -0.04, "ease": "linear"}])

EUS = dict(voice="em_santa", speed=0.88)
ABU = dict(voice="em_santa", speed=0.78)
JUA = dict(voice="ef_dora", speed=0.86)
HMEN = dict(voice="em_santa", speed=0.76)
ALUX = dict(voice="ef_dora", speed=0.96, fx="eco")

# ======================================================================== COLD OPEN
B("Tac… tac… tac. Algo cae sobre el techo de palma. Son piedritas. Pequeñas, redondas… y vienen de la milpa.",
  S("champa_inside", FIRE, cam=((0.5, 0.62, 1.45), (0.5, 0.52, 1.15)), fx=["embers", FL], grade="candle", tr="fade", tl=1.2),
  pre=0.4, music="dread", amb=["night", {"name": "crickets", "gain": -6}], sfx=[X("knock", 0.2, -8, times=3), X("knock", 2.2, -10, times=2)])
B("Eusebio se levanta de la hamaca con el machete en la mano. Afuera, la luna pinta de plata las cañas del maíz. Y entre las cañas… se oye una risa. Una risa de niño.",
  S("eusebio_scared", cam=((0.5, 0.45, 1.25), (0.5, 0.42, 1.45), "in"), fx=[FL], w=1.0),
  S("milpa_night", CORN, cam=((0.5, 0.6, 1.4), (0.5, 0.55, 1.15)), fx=[FOGL], tr="xfade", tl=0.6, w=1.2),
  amb=["night"], sfx=[X("whisper", 6.0, -10, dur=3)])
B("Pero en tres kilómetros a la redonda no hay ningún niño. Solo está él… y la casita de piedra que construyó su abuelo, al borde del monte.",
  S("casita_alux", cam=((0.5, 0.55, 1.05), (0.52, 0.58, 1.35), "in"), fx=[FOGL, "fireflies"]),
  sfx=[X("heartbeat", 3.0, -10, dur=7, bpm=72)])
B("Ya te olvidaste de mí.",
  S("alux_peek", GEYES, cam=((0.5, 0.55, 1.3), (0.5, 0.55, 1.55), "in"), fx=[FOGL]),
  S("alux_close", tr="flash", tl=0.12, dur=1.2, cam=((0.5, 0.45, 1.5), (0.5, 0.45, 1.7)), fx=[SH(0, 0.4, 6)]),
  sfx=[X("sting", -0.1, -4, at_scene=1)], **ALUX)
B("Eusebio voltea. A la altura de su rodilla, entre el maíz, dos ojitos amarillos lo están mirando.",
  S("alux_peek", cam=((0.5, 0.6, 1.5), (0.5, 0.62, 1.75), "in"), fx=[FOG], w=1.3),
  S("alux_scare", tr="flash", tl=0.15, dur=2.0, cam=((0.5, 0.45, 1.35), (0.5, 0.45, 1.6)), fx=[SH(0, 0.6, 9)], grade="night"),
  pause=0.8, sfx=[X("sting", -0.1, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), fx=[FOGL, "fireflies"], tr="fade", tl=0.8,
    text=[T("LOS ALUXES|los guardianes de la milpa", "title", 0.6, 6.4)]),
  pause=6.0, music="mystery", amb=["night", {"name": "crickets", "gain": -6}], sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Esta es la leyenda de los aluxes, los pequeños dueños del monte de Yucatán. Y antes de que termine, vas a saber qué encontraron, muchos años después, dentro de esa casita de piedra que nadie se atrevía a abrir.",
  S("casita_close", cam=((0.5, 0.55, 1.15), (0.5, 0.58, 1.45), "in"), fx=[FOGL], grade="moon"))

# ======================================================================== I
B("Cuentan que todo empezó con el abuelo, don Anastasio Chan, un milpero del sur de Yucatán, allá por los cerros de Tekax. Su milpa era la más verde del pueblo. Nunca se secaba, ni en los años de sequía.",
  S("milpa_day", cam=((0.5, 0.5, 1.05), (0.45, 0.52, 1.25)), fx=["dust"], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO I|El barro virgen", "chapter", 0.6, 5.0)]),
  S("abuelo_portrait", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), fx=["dust"], grade="warm", tr="xfade", tl=0.8,
    text=[T("Sur de Yucatán, hacia 1950|los cerros de Tekax", "date", 0.5, 4.5)]), music="calm", amb=["wind"])
B("Los vecinos decían que tenía suerte. Pero don Anastasio sabía que no era suerte. Era un trato.",
  S("abuelo_portrait", cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.55), "in"), grade="warm"))
B("Una noche, siete semanas antes del Viernes Santo, fue a buscar al jmen del pueblo, el sacerdote maya que todavía sabía hablar con los vientos y con los dueños del monte.",
  S("hmen_portrait", CANDLE, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), fx=[FL], grade="candle", tr="fade", tl=0.8),
  music="mystery")
B("Juntos sacaron barro virgen, barro que nadie había tocado, de la orilla de un cenote escondido.",
  S("barro_pit", cam=((0.4, 0.55, 1.1), (0.55, 0.55, 1.3)), fx=[FOGL], grade="moon"), amb=["drips", {"name": "night", "gain": -6}])
B("Y cada viernes, rezando en maya, el jmen fue dando forma a un muñequito. Primero los pies. Luego las manos. Luego una carita de viejo, con barba… y un sombrerito.",
  S("hands_clay", CANDLE, cam=((0.5, 0.5, 1.15), (0.5, 0.55, 1.45), "in"), fx=[FL], grade="candle"),
  S("clay_figure", CANDLE, cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.5), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8),
  amb=["room", {"name": "fire", "gain": -10}])
B("La última noche, don Anastasio dejó caer sobre el barro unas gotas de sangre de la palma de su mano. Así, dicen, el muñeco queda atado a su dueño.",
  S("palm_blood", CANDLE, cam=((0.5, 0.5, 1.2), (0.5, 0.52, 1.5), "in"), fx=[FL], grade="candle"),
  pause=0.8, sfx=[X("heartbeat", 0.5, -8, dur=6, bpm=60)])
B("Y al amanecer… el muñeco ya no estaba en la mesa.",
  S("altar_empty", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=["dust"], grade="moon"),
  pause=1.0, music="tension", sfx=[X("sting", 1.5, -5)])
B("Lo encontraron en la milpa, sentado dentro de una casita de piedra que el abuelo le había levantado al borde del monte, con su techito de palma y su puertita mirando hacia el maíz.",
  S("casita_day", cam=((0.5, 0.55, 1.1), (0.5, 0.58, 1.35)), fx=["dust"], grade="warm"))
B("Desde esa noche, la milpa tuvo guardián.",
  S("alux_roof", cam=((0.5, 0.45, 1.2), (0.5, 0.4, 1.0), "out"), fx=[FOGL]), sfx=[X("owl", 0.5, -10)])

# ======================================================================== II
B("Cuentan que los aluxes miden lo que un niño de tres años. Que tienen cara de viejito, sandalias, sombrero… y que casi nunca se dejan ver. Se oyen. Se oyen silbar, reír, correr entre las hojas.",
  S("alux_full", cam=((0.5, 0.55, 1.1), (0.55, 0.5, 1.3)), fx=[FOGL, "fireflies"], tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|Los dueños del monte", "chapter", 0.6, 5.0)]),
  S("milpa_night", ALUXW, CORN, cam=((0.4, 0.6, 1.3), (0.6, 0.6, 1.3), "linear"), fx=[FOGL], tr="xfade", tl=0.6),
  music="mystery", amb=["night", {"name": "wind", "gain": -6}], sfx=[X("whisper", 4.0, -12, dur=3)])
B("De día son barro. De noche… caminan.",
  S("clay_figure", cam=((0.5, 0.45, 1.4), (0.5, 0.42, 1.7), "in"), fx=[FL], grade="moon", text=[T("DE NOCHE|caminan", "big", 1.2, 4.0)]),
  pre=0.3, sfx=[X("boom", 0.2, -6)])
B("El alux de don Anastasio cuidaba la milpa como un perro bravo. Al ladrón que se metía a robar elotes lo recibían con una lluvia de piedritas que salían de ningún lado.",
  S("thief_stones", STONES, cam=((0.5, 0.5, 1.1), (0.5, 0.55, 1.3)), fx=[FOGL]),
  sfx=[X("knock", 1.5, -8, times=4), X("whoosh", 1.0, -10)])
B("Y si un animal del monte se acercaba al maíz, al otro día amanecía lejos, como espantado, sin querer volver.",
  S("monte_dense", GEYES, cam=((0.5, 0.5, 1.15), (0.55, 0.5, 1.35)), fx=[FOGL]))
B("Dicen también que un alux bien cuidado llama a la lluvia cuando la milpa tiene sed, y que espanta los malos vientos, esos aires del monte que enferman a la gente.",
  S("milpa_night", CORN, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3)), fx=[FOGL, {"type": "rain", "strength": 0.3}]), amb=["rain", {"name": "wind", "gain": -8}])
B("Pero un alux no se cuida solo. Hay que darle de comer.",
  S("abuelo_offering", CANDLE, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.35)), fx=[FL], grade="candle"), music="calm")
B("Antes de sembrar, don Anastasio le dejaba una jícara de sacab, la bebida de maíz y miel. Y después de la cosecha, los primeros elotes eran para él. Antes que para la familia. Antes que para nadie.",
  S("ofrenda_jicara", CANDLE, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.45), "in"), fx=[FL], grade="candle"),
  S("casita_alux", cam=((0.5, 0.55, 1.2), (0.5, 0.58, 1.05)), fx=[FOGL, "fireflies"], tr="xfade", tl=0.6))
B("Su nieto, Eusebio, creció escuchando las reglas.",
  S("eusebio_young", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), grade="warm"))
B("Nunca le faltes con su comida. Nunca le quites nada de su casita. Y nunca, nunca, abras esa puerta.",
  S("abuelo_candle", CANDLE, cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.5), "in"), fx=[FL], grade="candle"), **ABU)
B("Si el alux se queda con hambre, deja de cuidar. Y empieza a cobrar.",
  S("abuelo_candle", cam=((0.5, 0.4, 1.5), (0.5, 0.38, 1.7), "in"), fx=[FL], grade="candle"), pause=0.9, sfx=[X("sting", 2.0, -6)], **ABU)
B("Si te gustan estas historias de nuestra tierra, suscríbete y activa la campanita. Cada semana te traigo una leyenda nueva.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.15)), fx=[FOGL, "fireflies"]), music="mystery")

# ======================================================================== III
B("Don Anastasio murió viejo, en su hamaca, con la milpa todavía verde. Y Eusebio, que tenía veinte años, se fue a buscar trabajo a la costa de Quintana Roo, donde estaban construyendo una ciudad nueva en medio de la selva y del mar: Cancún.",
  S("abuelo_hammock", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=[FL], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO III|El olvido", "chapter", 0.6, 5.0)]),
  S("cancun_build", cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.25)), fx=["dust"], grade="warm", tr="xfade", tl=0.8,
    text=[T("Cancún, principios de los setenta|una ciudad nueva sobre la selva", "date", 0.5, 4.5)]),
  music="sad", amb=["sea", {"name": "wind", "gain": -8}])
B("Trabajaba de sol a sol cargando block y cemento, con el mar más azul que había visto en su vida a un lado… y la selva, oscura y callada, al otro.",
  S("cancun_build", cam=((0.6, 0.55, 1.3), (0.45, 0.5, 1.15)), fx=["dust"], grade="warm"))
B("Allá oyó por primera vez una historia que los albañiles mayas contaban en voz baja, junto a la fogata.",
  S("workers_fire", FIRE, cam=((0.5, 0.55, 1.1), (0.5, 0.52, 1.3)), fx=["embers"], grade="candle"), amb=["fire", {"name": "sea", "gain": -8}], music="mystery")

B("Decían que en un puente cerca de donde hoy está el aeropuerto, las cosas no salían. Las herramientas desaparecían en la noche. Los fierros amanecían doblados. Y lo que se levantaba de día… amanecía en el suelo.",
  S("bridge_night", cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=[FOGL]),
  S("bent_rebar", cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.45), "in"), fx=[FOG], tr="xfade", tl=0.6),
  amb=["night", {"name": "sea", "gain": -6}], sfx=[X("chains", 3.0, -10)])
B("Hasta que un maestro de obra dijo lo que todos pensaban: son los aluxes. Esta tierra tiene dueño, y nadie le pidió permiso.",
  S("workers_fire", FIRE, cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.5), "in"), fx=["embers"], grade="candle"))
B("Cuentan que hicieron una ceremonia, que les dejaron ofrendas y que les construyeron, debajo del puente, una casita en forma de pirámide. Y que desde entonces, el puente sigue en pie.",
  S("bridge_shrine", CANDLE, cam=((0.5, 0.55, 1.1), (0.5, 0.6, 1.35), "in"), fx=[FOGL, FL]))
B("Eusebio se rio de esa historia. Pasó siete años en la costa. Y en siete años, nunca mandó a nadie a llevarle su jícara al alux del abuelo.",
  S("eusebio_portrait", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), grade="warm"),
  S("casita_overgrown", cam=((0.5, 0.55, 1.3), (0.5, 0.58, 1.1)), fx=[FOGL], tr="xfade", tl=0.8), music="tension")

# ======================================================================== IV
B("Regresó al pueblo casado, con su mujer, Juana, y con un hijo de siete años, Mateo. Volvió a abrir la milpa del abuelo. Tumbó el monte, quemó, sembró. Pero no pidió permiso. Y no dejó nada en la casita de piedra.",
  S("milpa_burn", cam=((0.5, 0.5, 1.05), (0.55, 0.5, 1.25)), fx=["embers", "ash"], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|Las piedritas", "chapter", 0.6, 5.0)]),
  S("juana_portrait", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), grade="warm", tr="xfade", tl=0.6),
  music="tension", amb=["wind", {"name": "fire", "gain": -6}])
B("Eusebio, ¿y la jícara del alux? Tu abuelo nunca la olvidaba.",
  S("juana_portrait", cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.5)), grade="warm"), **JUA)
B("Mi abuelo creía en cuentos, Juana. El maíz crece con lluvia, no con muñecos de barro.",
  S("eusebio_portrait", cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.55), "in"), grade="warm"), **EUS)
B("Esa misma noche empezaron las piedritas.",
  S("alux_roof", STONES, cam=((0.5, 0.4, 1.3), (0.5, 0.45, 1.1)), fx=[FOGL], text=[T("PIEDRITAS|toda la noche", "big", 0.8, 3.6)]), pause=0.8,
  music="dread", amb=["night"], sfx=[X("knock", 0.6, -6, times=3), X("knock", 2.0, -8, times=4)])
B("Primero en el techo, toda la noche. Luego en la puerta. Luego, en la mañana, encontraron huellitas en la ceniza del fogón. Huellitas de pie descalzo… del tamaño de un dedo de la mano.",
  S("champa_inside", FIRE, cam=((0.5, 0.4, 1.2), (0.5, 0.45, 1.35)), fx=["embers", FL], grade="candle"),
  S("footprints_ash", cam=((0.5, 0.5, 1.2), (0.5, 0.55, 1.5), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.6),
  sfx=[X("sting", -0.2, -6, at_scene=1)])
B("La coa de Eusebio apareció colgada en lo más alto de un árbol de ramón. Las gallinas amanecían encerradas dentro de la olla del nixtamal. Y el maíz… el maíz tierno amanecía mordido, mazorca por mazorca, con dientes pequeñitos.",
  S("tool_tree", cam=((0.5, 0.6, 1.1), (0.5, 0.35, 1.3)), fx=[FOGL]),
  S("corn_bitten", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.5), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.6))
B("Juana empezó a dejar tortillas en la puerta, a escondidas de su marido. Al otro día, las tortillas seguían ahí… intactas. No era eso lo que el alux quería. Quería que se lo diera su dueño.",
  S("juana_door", CANDLE, cam=((0.5, 0.5, 1.1), (0.55, 0.5, 1.3)), fx=[FOGL, FL]))
B("Eusebio se puso a velar con la escopeta. Y una madrugada lo vio: un hombrecito sentado en el techo de su casita de piedra, columpiando las piernas, mirándolo… y riéndose.",
  S("eusebio_gun", cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.35)), fx=[FOGL]),
  S("alux_roof", GEYES, cam=((0.5, 0.45, 1.25), (0.5, 0.4, 1.55), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  sfx=[X("whisper", 4.0, -8, dur=3)])
B("Eusebio disparó.",
  S("alux_scare", tr="flash", tl=0.12, dur=1.6, cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.7)), fx=[SH(0, 0.7, 12)], grade="blood"),
  pause=0.6, sfx=[X("boom", 0.0, -1), X("sting", 0.05, -3)])
B("Y en ese instante, todas las piedritas del monte cayeron al mismo tiempo sobre la casa.",
  S("champa_out", STONES, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.3)), fx=[FOGL, SH(0.3, 3.0, 6)]),
  pause=1.0, sfx=[X("knock", 0.2, -2, times=10), X("thunder", 0.8, -6)])
B("Dos días después, Eusebio cayó en cama con una calentura que ningún doctor supo curar. Temblaba en la hamaca, con los ojos abiertos, y repetía una sola frase.",
  S("eusebio_fever", CANDLE, cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.4), "in"), fx=[FL], grade="candle"), music="sad")
B("Ya no está enojado conmigo… está enojado con el niño.",
  S("eusebio_fever", cam=((0.5, 0.42, 1.45), (0.5, 0.42, 1.7), "in"), fx=[FL], grade="candle"), pause=0.9, **EUS)
B("Esa noche, Juana despertó y la hamaca de Mateo estaba vacía.",
  S("hammock_empty", cam=((0.5, 0.5, 1.1), (0.5, 0.55, 1.4), "in"), fx=[FOGL], text=[T("VACÍA", "big", 1.5, 4.0)]), pause=0.8, music="dread", sfx=[X("sting", 1.6, -3)])
B("La puerta estaba abierta. Y afuera, a la luz de la luna, se veían dos figuras entre el maíz: una era su hijo. La otra, más pequeña, lo llevaba de la mano hacia el monte.",
  S("juana_scared", cam=((0.5, 0.45, 1.25), (0.5, 0.42, 1.5), "in"), fx=[FL]),
  S("mateo_corn", CORN, cam=((0.5, 0.6, 1.1), (0.5, 0.58, 1.4), "in"), fx=[FOGL], tr="xfade", tl=0.6, w=1.3),
  sfx=[X("heartbeat", 0.0, -6, dur=12, bpm=96)])
B("Ven a jugar… ven a jugar conmigo.",
  S("alux_close", tr="flash", tl=0.15, cam=((0.5, 0.45, 1.35), (0.5, 0.45, 1.6), "in"), fx=[FOG, SH(0, 0.5, 6)], grade="moon"),
  sfx=[X("sting", -0.1, -4), X("boom", 0.0, -6)], **ALUX)
B("Juana corrió gritando su nombre. Pero cuando llegó al borde de la milpa… ya no había nadie. Solo el monte negro. Y una risita que se alejaba.",
  S("monte_dense", BRUSH, cam=((0.5, 0.55, 1.4), (0.5, 0.5, 1.1)), fx=[FOGL], out=1.0),
  pause=1.2, sfx=[X("whisper", 3.5, -10, dur=4)])

# ======================================================================== V
B("Fueron a buscar al jmen, don Pastor, que ya era muy viejo. No hizo preguntas. Miró la casita de piedra, cubierta de hierba, y movió la cabeza.",
  S("hmen_portrait", CANDLE, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.4)), fx=[FL], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO V|La ofrenda", "chapter", 0.6, 5.0)]),
  music="mystery", amb=["night", {"name": "crickets", "gain": -8}])
B("Siete años sin comer. Siete años solo. No se llevó al niño para hacerle daño… se lo llevó para tener con quién jugar.",
  S("hmen_portrait", cam=((0.5, 0.42, 1.4), (0.5, 0.4, 1.6), "in"), fx=[FL], grade="candle"), **HMEN)
B("Esa misma noche armaron una mesa en medio de la milpa. Pusieron velas, copal, tortillas de maíz nuevo, una jícara de sacab y otra de balché. Y el jmen empezó a rezar, en maya, hacia los cuatro rumbos del monte.",
  S("ritual_altar", COPAL, CANDLE, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FL], grade="candle"),
  S("ritual_wide", COPAL, cam=((0.5, 0.5, 1.05), (0.5, 0.52, 1.2)), fx=[FOGL, FL], tr="xfade", tl=0.8),
  amb=["night", {"name": "fire", "gain": -8}], sfx=[X("whisper", 2.0, -14, dur=6)])
B("Eusebio, temblando de fiebre, se arrodilló frente a la casita y pidió perdón. Por el olvido. Por el disparo. Por los siete años.",
  S("eusebio_kneel", CANDLE, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=[FL, FOGL], grade="candle"))
B("Perdóname. Aquí está tu comida. Devuélveme a mi hijo.",
  S("eusebio_scared", cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.55), "in"), fx=[FL], grade="candle"), **EUS)
B("Durante horas no pasó nada. El copal se consumió. Las velas se fueron apagando, una por una. Y justo antes del amanecer, el viento se detuvo.",
  S("ritual_altar", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.1)), fx=[FL, "dust"], grade="moon"),
  music="silence", amb=[], sfx=[X("heartbeat", 1.0, -8, dur=8, bpm=56)])
B("Tac.",
  S("ofrenda_jicara", cam=((0.5, 0.55, 1.5), (0.5, 0.55, 1.65)), grade="moon", dur=2.0), pre=0.6, pause=0.8, sfx=[X("knock", 0.0, -2, times=1)])
B("Una sola piedrita cayó dentro de la jícara vacía. El sacab ya no estaba.",
  S("ofrenda_jicara", cam=((0.5, 0.55, 1.6), (0.5, 0.58, 1.85), "in"), grade="moon"), music="mystery")
B("Y del otro lado de la casita, acurrucado en la hierba, dormía Mateo. Tenía los pies llenos de barro… y las manos llenas de granos de maíz.",
  S("mateo_found", cam=((0.5, 0.55, 1.1), (0.5, 0.58, 1.35), "in"), fx=[FOGL, "dust"], grade="cold"),
  music="hope", amb=["wind", {"name": "crickets", "gain": -10}])
B("No recordaba nada. Solo decía que había jugado toda la noche con un señor chiquito… que le enseñó a hacer bailar su trompo como nadie.",
  S("trompo", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.45), "in"), fx=["dust"], grade="warm"))
B("Y que el señor chiquito se quedó con el trompo.",
  S("trompo", cam=((0.5, 0.5, 1.45), (0.5, 0.5, 1.6)), grade="moon"), pause=0.9, sfx=[X("sting", 0.6, -8)])
B("La fiebre de Eusebio se fue esa misma semana. Y nunca más, en toda su vida, olvidó la jícara de sacab.",
  S("casita_alux", cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.25)), fx=[FOGL, "fireflies"]))

# ======================================================================== VI history
B("Hasta aquí, la leyenda. Ahora, lo que sí es historia.",
  S("ruins_dawn", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=["dust"], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO VI|Lo que dice la historia", "chapter", 0.6, 5.0)]), music="calm", amb=["wind"])
B("La creencia en los aluxes, que en algunos pueblos llaman aruxes, sigue viva en toda la península: en Yucatán, en Campeche y en Quintana Roo. Muchos campesinos mayas todavía piden permiso al monte antes de sembrar, y ofrecen la primicia del maíz.",
  S("milpa_day", cam=((0.4, 0.5, 1.2), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="warm"),
  S("ofrenda_jicara", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.35)), grade="warm", tr="xfade", tl=0.6))
B("Una de las historias más antiguas cuenta que los aluxes fueron seres que los dioses dejaron sin terminar. Escapaban del cielo de noche, y cuando el sol los sorprendía, se quedaban hechos piedra. Por eso, dicen, solo cobran vida en la oscuridad.",
  S("stone_figures", cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=["dust"], grade="warm"))
B("Y en las milpas, cuando el arado saca de la tierra figuritas de barro de los antiguos mayas, hay quien no se las lleva a su casa. Las deja donde estaban. Por si acaso.",
  S("figurines", cam=((0.5, 0.5, 1.15), (0.5, 0.52, 1.4), "in"), fx=["dust"], grade="sepia"))
B("Los estudiosos de la cultura maya ven en los aluxes algo más que duendes traviesos: son parte de una manera antigua de entender el monte, donde cada cerro, cada cenote y cada milpa tiene un dueño al que hay que respetar.",
  S("ruins_dawn", cam=((0.4, 0.5, 1.2), (0.55, 0.5, 1.1)), fx=["dust"], grade="warm"))
B("Todavía hoy, en casas, ranchos y hasta en grandes obras de la península, hay quien construye una pequeña casita para los aluxes. No cuesta nada. Y nadie quiere averiguar qué pasa si no se hace.",
  S("casita_day", cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.05)), fx=["dust"], grade="warm"),
  S("bridge_shrine", cam=((0.5, 0.55, 1.2), (0.5, 0.58, 1.4)), fx=[FOGL], tr="xfade", tl=0.6))

# ======================================================================== payoff
B("¿Y la casita de piedra? Sigue ahí, al borde de la milpa de los Chan. Eusebio murió muy viejo. Y fue Mateo, ya con el pelo blanco, el que un día encontró la puertita caída por las lluvias.",
  S("casita_close", cam=((0.5, 0.55, 1.1), (0.5, 0.58, 1.35), "in"), fx=[FOGL], grade="moon", tr="fade", tl=1.0,
    text=[T("Muchos años después", "date", 0.5, 4.0)]), music="tension", amb=["night", {"name": "wind", "gain": -6}])
B("Se agachó. Miró adentro.",
  S("casita_dark", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.65), "in"), fx=[FOG]), pause=1.0, music="dread", sfx=[X("heartbeat", 0.0, -6, dur=6, bpm=80)])
B("Ahí estaba el muñequito de barro del abuelo, con su barba y su sombrero, sentado en la oscuridad. Tenía los pies cubiertos de lodo fresco… aunque no había llovido en semanas.",
  S("clay_inside", cam=((0.5, 0.5, 1.2), (0.5, 0.55, 1.5), "in"), fx=[FOG], grade="moon"))
B("Y en su manita de barro, apretado… tenía un trompo de madera. El mismo trompo que Mateo perdió aquella noche, cuando tenía siete años.",
  S("clay_trompo", cam=((0.5, 0.55, 1.3), (0.5, 0.58, 1.7), "in"), fx=[FOG], grade="moon", text=[T("EL TROMPO", "big", 2.5, 5.5)]),
  pause=1.0, sfx=[X("sting", 3.0, -4)])
B("Y la pintura del trompo… estaba gastada, como si alguien lo hubiera hecho bailar todas las noches durante cincuenta años.",
  S("alux_close", tr="flash", tl=0.15, cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.65)), fx=[SH(0, 0.6, 8)], grade="night", out=0.8),
  pause=1.4, music="silence", sfx=[X("whisper", 0.5, -8, dur=3), X("boom", 0.0, -3)])
B("Y ahora dime tú: ¿en tu pueblo se cuenta de los aluxes? ¿Alguien de tu familia les deja ofrenda? Cuéntamelo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOGL, "fireflies"], tr="fade", tl=0.8), music="mystery", amb=["crickets"])
B("En el próximo video dejamos Yucatán. Porque hay una mano, una mano peluda, que sale de debajo de la cama cuando apagas la luz. Es la leyenda de la Mano Peluda… y nunca deberías dejar el brazo colgando fuera del colchón.",
  S("mano_tease", cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.05)), fx=[FOG], grade="night",
    text=[T("PRÓXIMO VIDEO|La Mano Peluda", "big", 2.0, 7.0)]), sfx=[X("whisper", 3.0, -12, dur=4)])
B("Hasta la próxima leyenda. Y si de noche oyes piedritas en el techo… deja algo de comer afuera.",
  S("casita_alux", GEYES, cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.0), "out"), fx=[FOGL], out=2.0), pause=1.0, music="dread")

# resolve sfx relative to a scene (needs audio/timeline.json from tts.py)
TL = os.path.join(HERE, "audio", "timeline.json")
if os.path.exists(TL):
    tl = json.load(open(TL)); tb = tl["beats"]
    for i, b in enumerate(BEATS):
        if i >= len(tb): break
        end = tb[i + 1]["start"] if i + 1 < len(tb) else tl["duration"] + 5.0
        d = end - tb[i]["start"]; sc = b["scenes"]
        fixed = sum(s.get("dur", 0) for s in sc); wsum = sum(s.get("weight", 1) for s in sc if "dur" not in s)
        offs = []; t = 0.0
        for s in sc:
            offs.append(t); t += s["dur"] if "dur" in s else max(0, d - fixed) * s.get("weight", 1) / wsum
        for c in b.get("sfx", []):
            if "scene" in c:
                c["at"] = round(offs[c["scene"]] + c["at"], 3)

story = {"title": "Los Aluxes: los duendes mayas que cobran cuando te olvidas de ellos", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "D", "seed": 33, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# Los Aluxes — guion\n",
                  "Narración en español (narrador: em_alex; Juana y el alux: ef_dora; Eusebio, el abuelo Anastasio y el jmen don Pastor: em_santa).\n"]
WHO = {"ef_dora": "JUANA / ALUX: ", "em_santa": "PERSONAJE: "}
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
