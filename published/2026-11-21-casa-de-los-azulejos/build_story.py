#!/usr/bin/env python3
"""Builds story.json and script.md for 'La Casa de los Azulejos' (Ciudad de México). Edit BEATS here, then run.
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
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)

FOGLAY = L("l_fog", blend="screen", opacity=[0, 0.8], anim=[{"type": "drift", "dx": -0.06, "ease": "linear"}])
CAND = L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.15, "speed": 1.8}])
FIREG = L("l_fire_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 1.2}])
DIEGO = L("l_diego_candle", anim=[{"type": "flicker", "amp": 0.05, "speed": 1.5}])
INTR = L("l_intruder", depth=1.05, anim=[{"type": "drift", "dx": 0.03, "dy": -0.025, "ease": "inout"}])
GHOST = L("l_ghost_diego", blend="screen", opacity=[0, 0.9], fade_in=2.0, anim=[{"type": "float", "amp": 0.004, "period": 5}, {"type": "flicker", "amp": 0.12, "speed": 0.8}])
GHOSTQ = L("l_ghost_diego", blend="screen", opacity=[0, 0.95], appear_at=0.6, fade_in=0.4, vanish_at=3.4, fade_out=0.4)
FLOAT = L("l_float_candle", blend="screen", anim=[{"type": "float", "amp": 0.01, "period": 4}, {"type": "drift", "dx": -0.05, "dy": 0.04, "ease": "inout"}, {"type": "flicker", "amp": 0.2, "speed": 2}])

DIE = dict(voice="em_santa", speed=0.78)
DIEG = dict(voice="em_santa", speed=0.72, fx="eco")
PAD = dict(voice="em_santa", speed=0.8)
HIJ = dict(voice="em_santa", speed=0.9)
NIGHT = ["night", {"name": "wind", "gain": -9}]
HOUSE = ["room", {"name": "clock", "gain": -16}]
RIOT = ["fire", {"name": "city", "gain": -8}, {"name": "wind", "gain": -10}]
FLASH = lambda img="ghost_flash": S(img, tr="flash", tl=0.12, dur=1.4, cam=((0.5, 0.45, 1.25), (0.5, 0.45, 1.5)), fx=[SH(0, 0.6, 9)])
SCARE = [X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)]
STEPS = lambda at=0.3, d=5, g=-12: X("footsteps", at, g, dur=d)

# ======================================================================== COLD OPEN
B("Ciudad de México. Diciembre de mil ochocientos veintiocho. Afuera, la ciudad arde.",
  S("riot_night", FIREG, cam=((0.5, 0.5, 1.05), (0.5, 0.52, 1.25), "in"), fx=["embers", {"type": "flicker", "amp": 0.06}], tr="fade", tl=1.2,
    text=[T("Ciudad de México|diciembre de 1828", "date", 0.6, 5.0)]),
  pre=0.6, music="dread", amb=RIOT, sfx=[X("bell", 1.0, -14, freq=170), X("bell", 3.5, -16, freq=170)])
B("Imagina una casa enorme, cubierta de azulejos azules y blancos que brillan con la luz de los incendios. Adentro, todos duermen. Todos… menos uno.",
  S("facade_red", FIREG, cam=((0.5, 0.5, 1.02), (0.5, 0.45, 1.25), "in"), fx=["embers"]),
  S("tile_close", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.6), "in"), fx=[{"type": "flicker", "amp": 0.08}], grade="warm", tr="xfade", tl=0.6))
B("Un hombre entra por una ventana del entresuelo. Lleva capa de militar. Y en la mano, algo que brilla.",
  S("window_break", cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL]),
  S("dagger", CAND, cam=((0.5, 0.5, 1.2), (0.55, 0.5, 1.5), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.5),
  amb=HOUSE, sfx=[X("door", 0.5, -10), X("whoosh", 4.0, -10)])
B("Sube despacio por la gran escalera. Un escalón. Otro. Y entonces, arriba, en el descanso… se enciende una vela.",
  S("stairs", INTR, cam=((0.4, 0.6, 1.1), (0.55, 0.45, 1.3), "inout"), fx=[FOG]),
  S("stairs", DIEGO, CAND, cam=((0.7, 0.3, 1.4), (0.72, 0.28, 1.6), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.5, w=0.6),
  music="tension", sfx=[STEPS(0.3, 6, -10), X("heartbeat", 3.0, -12, dur=6, bpm=80)])
B("¿Quién anda ahí?",
  S("diego_portrait", CAND, cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.45), "in"), fx=[FL], grade="candle",
    text=[T("¿Quién anda ahí?|", "whisper", 0.3, 3.0)]), **DIE, pause=0.4)
B("",
  S("diego_shock", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.4), "in"), fx=[FL], grade="candle", dur=1.6),
  FLASH("red_flash"), pause=0.8, sfx=SCARE)
B("Nadie volvió a ver con vida al dueño de esa voz.",
  S("candle_floor", cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.4), "in"), fx=[FL], grade="candle"), music="silence", pause=0.9)
B("Casi dos siglos después, esa escalera sigue ahí. La subes tú, la sube cualquiera. Y hay quien jura que, cuando el edificio se queda vacío, alguien sigue bajando por ella… con una vela en la mano.",
  S("stairs_today", cam=((0.4, 0.6, 1.05), (0.6, 0.45, 1.25), "inout"), fx=["dust"], grade="night"),
  S("stairs_dark", FLOAT, cam=((0.6, 0.4, 1.2), (0.55, 0.5, 1.35), "in"), fx=[FOG], tr="xfade", tl=0.8),
  music="dread", amb=["room"], sfx=[STEPS(6.0, 4, -14)])
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("LA CASA|de los Azulejos", "title", 0.6, 6.4)]),
  pause=5.2, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Pero para entender quién baja esa escalera, primero hay que saber cómo una casa terminó vestida de azulejos. Y esa historia empieza con un padre furioso… y una frase que se volvió refrán.",
  S("facade_night", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOGL]),
  S("father_angry", cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.35), "in"), fx=[FL], tr="xfade", tl=0.6))
B("Qué es lo que busca esa vela cada noche… lo vas a saber al final.",
  S("stairs_dark", FLOAT, cam=((0.7, 0.35, 1.3), (0.7, 0.35, 1.5), "in"), fx=[FOG]), sfx=[STEPS(0.5, 3, -14)])

# ======================================================================== I
B("Cuentan que en el siglo dieciocho, en la calle de San Francisco, la que hoy es la calle de Madero, vivían los condes del Valle de Orizaba. Una de las familias más ricas de la Nueva España.",
  S("street_colonial", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], tr="fade", tl=1.0, grade="warm",
    text=[T("CAPÍTULO I|El hijo que no hacía casa", "chapter", 0.6, 5.0), T("Calle de San Francisco|Ciudad de México, siglo XVIII", "date", 6.0, 11.0)]),
  music="calm", amb=["city", {"name": "wind", "gain": -12}])
B("Tenían haciendas, títulos y carruajes con el escudo pintado en la puerta. Cuando un conde del Valle de Orizaba pasaba por la calle, la gente se quitaba el sombrero.",
  S("carriage", cam=((0.4, 0.55, 1.05), (0.6, 0.55, 1.2), "linear"), fx=["dust"], grade="warm"), sfx=[X("hooves", 0.5, -12, dur=5)])
B("Su casa era un palacio de piedra y tezontle, con patios, caballerizas y una capilla. Pero por fuera era como tantas otras. Gris. Seria. Sin un solo azulejo.",
  S("facade_plain", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="warm"),
  S("patio_old", CAND, cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.25), "linear"), fx=["dust"], grade="candle", tr="xfade", tl=0.6))
B("El conde tenía un hijo. Y el hijo tenía un problema. No le gustaba trabajar.",
  S("son_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust"]), music="mystery")
B("Le gustaban las noches. Las mesas de juego, los dados, las cartas, las peleas de gallos. Las fiestas que terminaban cuando ya amanecía.",
  S("gambling", CAND, cam=((0.45, 0.6, 1.1), (0.55, 0.6, 1.35), "in"), fx=[FL], grade="candle"),
  S("son_smile", CAND, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  amb=["room", {"name": "fire", "gain": -12}], sfx=[X("coins", 1.0, -10), X("coins", 5.0, -12)])
B("Imagina el ruido de las monedas sobre la mesa. El humo de los puros. Y la risa del muchacho, que perdía en una noche lo que a su padre le había costado un año.",
  S("dice_close", CAND, cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.5), "in"), fx=[FL, "dust"], grade="candle"),
  S("gambling", CAND, cam=((0.6, 0.55, 1.3), (0.4, 0.55, 1.4), "linear"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  sfx=[X("coins", 0.5, -8)])
B("El conde lo veía llegar al amanecer, con la ropa arrugada y los bolsillos vacíos. Y cada vez, la paciencia se le acababa un poco más.",
  S("street_dawn", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], grade="cold"),
  S("father_portrait", CAND, cam=((0.5, 0.42, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  amb=HOUSE, sfx=[X("door", 1.0, -12)])
B("Hasta que una mañana, delante de los criados, el viejo le dijo la frase que nadie en esa casa iba a olvidar.",
  S("confront", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.3), "in"), fx=["dust"], grade="candle"), music="tension")
B("Hijo… tú nunca harás casa de azulejos.",
  S("father_angry", cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.5), "in"), fx=[FL],
    text=[T("Tú nunca harás casa de azulejos.|el conde", "quote", 0.4, 5.0)]), **PAD, pause=1.0, sfx=[X("boom", 0.2, -10)])
B("En aquel tiempo, eso era una sentencia. Hacer casa de azulejos quería decir llegar lejos. Tener fortuna. Ser alguien. Cubrir tu casa con talavera era cosa de ricos de verdad.",
  S("tile_close", cam=((0.4, 0.4, 1.1), (0.6, 0.6, 1.4), "linear"), fx=["dust"], grade="none",
    text=[T("HACER CASA DE AZULEJOS|llegar lejos, tener fortuna", "big", 2.5, 7.5)]), music="mystery")
B("Decirle a un hijo que nunca haría casa de azulejos era decirle, delante de todos: tú no vales nada.",
  S("son_shame", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.4), "in"), fx=["dust"], grade="moon"), pause=0.9, music="sad")

# ======================================================================== II
B("El muchacho no contestó. Esa noche no salió a jugar. Se quedó despierto en su cuarto, mirando la pared, a la luz de una vela.",
  S("son_room", CAND, cam=((0.5, 0.5, 1.05), (0.45, 0.5, 1.3), "in"), fx=[FL], tr="fade", tl=1.0, grade="candle",
    text=[T("CAPÍTULO II|La promesa de talavera", "chapter", 0.6, 5.0)]),
  amb=HOUSE)
B("Y cuentan que, antes del amanecer, hizo una promesa en voz baja.",
  S("son_night", CAND, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=[FL], grade="candle"))
B("Un día, padre, esta casa va a brillar más que ninguna.",
  S("son_night", CAND, cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.55), "in"), fx=[FL], grade="candle",
    text=[T("Esta casa va a brillar más que ninguna.|el hijo", "quote", 0.4, 4.5)]), **HIJ, pause=0.8)
B("Y se fue.",
  S("road_dawn", cam=((0.4, 0.55, 1.05), (0.6, 0.55, 1.2), "linear"), fx=[FOGL], grade="cold"), pause=0.8, music="hope",
  amb=["wind"], sfx=[X("hooves", 0.0, -14, dur=5, distance=0.6)])
B("No se llevó criados ni carruaje. Solo un caballo, una capa y el orgullo herido. Su padre no salió a despedirlo.",
  S("father_window", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FOGL], grade="cold"))
B("Lo que pasó en los años siguientes, cada quien lo cuenta a su manera. Unos dicen que trabajó en las minas de plata. Otros, que se hizo comerciante, que viajó por los caminos con recuas de mulas, que compró y vendió de todo.",
  S("mine", CAND, cam=((0.4, 0.5, 1.1), (0.55, 0.5, 1.3), "linear"), fx=["dust", FL], grade="candle"),
  S("road_mules", L("l_mules", anim=[{"type": "drift", "dx": 0.05, "ease": "linear"}]), cam=((0.6, 0.55, 1.1), (0.4, 0.55, 1.2), "linear"), fx=["dust"], grade="warm", tr="xfade", tl=0.8),
  S("coins", CAND, cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.45), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  sfx=[X("chains", 1.0, -18), X("coins", 14.0, -10)])
B("Pero todas las versiones coinciden en algo. Volvió rico.",
  S("son_rich", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="warm"), pause=0.8)
B("Años después, un jinete se detuvo frente a la casa gris de la calle de San Francisco. Más delgado, más serio, con las manos endurecidas por el trabajo. Los criados tardaron en reconocerlo.",
  S("rider_return", cam=((0.4, 0.55, 1.05), (0.55, 0.5, 1.25), "in"), fx=["dust"], grade="warm"), sfx=[X("hooves", 0.0, -10, dur=4)])
B("Y lo primero que hizo fue ir a Puebla, a los talleres donde se hacía la talavera. Hornos encendidos día y noche. Manos llenas de barro. Pinceles de azul cobalto.",
  S("taller", FIREG, cam=((0.4, 0.55, 1.05), (0.6, 0.5, 1.25), "linear"), fx=["embers", FL], grade="warm",
    text=[T("Puebla de los Ángeles|", "date", 1.0, 5.0)]),
  S("painting_tile", CAND, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.5), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  amb=["fire", {"name": "room", "gain": -10}])
B("Encargó miles de azulejos. Azules, blancos, amarillos. Y los mandó traer en carretas hasta la Ciudad de México.",
  S("tile_stacks", cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.3), "linear"), fx=["dust"], grade="warm"),
  S("road_mules", L("l_mules", anim=[{"type": "drift", "dx": 0.05, "ease": "linear"}]), cam=((0.3, 0.55, 1.2), (0.6, 0.55, 1.3), "linear"), fx=["dust"], grade="warm", tr="xfade", tl=0.6),
  amb=["wind"], sfx=[X("hooves", 3.0, -14, dur=5, distance=0.5)])
B("Uno por uno, los albañiles fueron cubriendo la fachada. Semanas. Meses. Hasta que una mañana, cuando el sol salió por encima de los volcanes… la casa entera se encendió de azul.",
  S("tiling_work", cam=((0.4, 0.55, 1.1), (0.55, 0.5, 1.3), "linear"), fx=["dust"], grade="warm"),
  S("volcanoes_dawn", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.2), "in"), fx=[FOGL], grade="warm", tr="xfade", tl=0.8),
  S("facade_dawn", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.02), "out"), fx=["dust"], grade="none", tr="xfade", tl=1.0,
    text=[T("AZUL|", "big", 1.0, 4.0)]),
  amb=["city"], sfx=[X("bell", 13.0, -10, freq=200)])
B("Dicen que el viejo conde salió a la calle, levantó la vista… y se quedó callado mucho tiempo.",
  S("father_tear", cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.4), "in"), fx=["dust"], grade="warm"), music="sad")
B("Su hijo, el que nunca iba a hacer casa de azulejos, le había vestido la casa entera con ellos. Desde entonces, la gente la llamó así. La Casa de los Azulejos.",
  S("facade_day", cam=((0.4, 0.5, 1.15), (0.6, 0.5, 1.15), "linear"), fx=["dust"], grade="none"),
  S("tile_close2", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.45), "in"), fx=["dust"], grade="none", tr="xfade", tl=0.6))
B("Pero cuentan los criados que esa primera noche, con la fachada terminada, alguien tocó la puerta tres veces.",
  S("door_night", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.4), "in"), fx=[FOGL], grade="night"),
  music="dread", amb=NIGHT, sfx=[X("knock", 4.0, -6, times=3)])
B("Abrieron. No había nadie. Solo, en el suelo, frente a la puerta… un azulejo roto.",
  S("door_open", cam=((0.5, 0.55, 1.1), (0.5, 0.6, 1.35), "in"), fx=[FOGL], grade="night"),
  FLASH("tile_crack"), pause=0.9, sfx=[X("door", 0.3, -10)] + SCARE)
B("Si te gustan estas historias, suscríbete al canal, porque lo que viene ahora ya no es una historia de orgullo. Es una historia de sangre.",
  S("facade_night", FOGLAY, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=[FOGL]), music="mystery")

# ======================================================================== III
B("Pasó el tiempo. Pasaron los condes. La Nueva España dejó de ser Nueva España y se convirtió en México.",
  S("plaza_1820", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], tr="fade", tl=1.0, grade="sepia",
    text=[T("CAPÍTULO III|La noche del motín", "chapter", 0.6, 5.0)]),
  music="calm", amb=["city"])
B("Y a finales de noviembre de mil ochocientos veintiocho estalló en la capital el motín de la Acordada. Una revuelta por las elecciones presidenciales, que terminó con el saqueo del Parián, el gran mercado de la Plaza Mayor.",
  S("riot_night", FIREG, cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.25), "linear"), fx=["embers"],
    text=[T("Motín de la Acordada|noviembre y diciembre de 1828", "date", 1.0, 6.0)]),
  S("parian", FIREG, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=["embers", "ash"], tr="xfade", tl=0.6),
  music="tension", amb=RIOT, sfx=[X("boom", 3.0, -12), X("boom", 9.0, -14)])
B("Durante días, la ciudad fue de nadie. Tiendas rotas, disparos, incendios. Y en medio del desorden, cada quien aprovechaba para arreglar sus propias cuentas.",
  S("riot_street", FIREG, cam=((0.5, 0.5, 1.1), (0.45, 0.5, 1.3), "in"), fx=["embers", {"type": "shake", "amp": 3, "at": [2.0, 3.0]}]),
  sfx=[X("boom", 2.0, -8), X("whoosh", 6.0, -12)])
B("En la Casa de los Azulejos vivía entonces un anciano de la familia, don Diego Suárez de Peredo, que había llevado el título de conde. Y vivía también una muchacha joven de la casa, llamada Graciana.",
  S("diego_portrait", CAND, cam=((0.5, 0.42, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle",
    text=[T("don Diego Suárez de Peredo|", "date", 1.0, 6.0)]),
  S("graciana", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust"], tr="xfade", tl=0.6),
  amb=HOUSE, music="mystery")
B("A Graciana la pretendía un militar. Manuel Palacios. Un hombre de uniforme, de mirada dura, que no estaba acostumbrado a que le dijeran que no.",
  S("palacios", CAND, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=[FL], grade="candle",
    text=[T("Manuel Palacios|", "date", 1.5, 6.0)]))
B("Dicen que la seguía a misa. Que se paraba bajo sus balcones de noche, envuelto en la capa, mirando hacia arriba. Y que Graciana, al verlo, cerraba las cortinas con las manos temblando.",
  S("watcher_street", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOGL], grade="night"),
  S("graciana_fear", CAND, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6), amb=NIGHT)
B("Pero la familia le dijo que no. Le cerraron la puerta. Le prohibieron acercarse a ella.",
  S("graciana_window", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=[FOGL], grade="night"),
  sfx=[X("door", 3.0, -8)])
B("Y Manuel Palacios esperó. Esperó a que la ciudad estuviera en llamas. A que nadie fuera a escuchar un grito.",
  S("palacios_red", FIREG, cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.45), "in"), fx=[FL], grade="blood"), music="dread")
B("Una noche de diciembre, entró por las ventanas del entresuelo.",
  S("window_break", cam=((0.5, 0.5, 1.2), (0.5, 0.55, 1.45), "in"), fx=[FOGL]), amb=HOUSE, sfx=[X("door", 1.0, -10)])
B("Ahora ya sabes cómo empieza. Un hombre con capa. Una escalera de piedra. Pasos que suben en la oscuridad.",
  S("stairs", INTR, cam=((0.35, 0.65, 1.15), (0.5, 0.5, 1.35), "inout"), fx=[FOG]), sfx=[STEPS(0.5, 7, -9)])
B("Y arriba, en el descanso, una vela. Don Diego lo había oído entrar.",
  S("stairs", DIEGO, CAND, cam=((0.72, 0.3, 1.3), (0.72, 0.28, 1.6), "in"), fx=[FL], grade="candle"),
  sfx=[X("heartbeat", 0.0, -10, dur=6, bpm=90)])
B("¿Quién anda ahí?",
  S("diego_shock", CAND, cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.5), "in"), fx=[FL], grade="candle",
    text=[T("¿Quién anda ahí?|", "whisper", 0.3, 3.0)]), **DIE, pause=0.5)
B("No hubo respuesta. Solo el brillo del acero.",
  S("palacios_red", cam=((0.5, 0.42, 1.4), (0.5, 0.42, 1.55), "in"), fx=[FL], grade="blood"),
  FLASH("red_flash"), pause=1.0, music="climax", sfx=SCARE)
B("Lo que pasó en ese descanso duró apenas unos segundos. Cuando los criados llegaron con luces, el anciano estaba en el suelo, y la vela seguía encendida a su lado. El hombre de la capa había desaparecido en la noche.",
  S("servants_light", CAND, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FL], grade="candle"),
  S("fallen_stairs", CAND, cam=((0.5, 0.55, 1.15), (0.5, 0.55, 1.35), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  S("riot_street", FIREG, cam=((0.5, 0.5, 1.2), (0.6, 0.5, 1.35), "linear"), fx=["embers", FOGL], tr="xfade", tl=0.6),
  music="sad", sfx=[STEPS(0.5, 3, -10)])
B("La familia supo quién había sido. Lo dijo con nombre y apellido. Pero en una ciudad revuelta, con las autoridades ocupadas en otras cosas… nadie lo castigó.",
  S("graciana_fear", CAND, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=[FL], grade="candle"),
  S("chronicle", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="sepia", tr="xfade", tl=0.6))
B("Manuel Palacios nunca pagó.",
  S("palacios", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.5), "in"), fx=["dust"], grade="cold",
    text=[T("NUNCA PAGÓ|", "big", 0.6, 3.5)]), pause=1.0, sfx=[X("boom", 0.4, -8)])

# ======================================================================== IV
B("Dicen que fue entonces cuando empezaron los pasos.",
  S("stairs_dark", cam=((0.5, 0.5, 1.05), (0.55, 0.45, 1.3), "in"), fx=[FOG], tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|La escalera", "chapter", 0.6, 5.0)]),
  music="dread", amb=["room", {"name": "drips", "gain": -14}])
B("Los criados los oían de madrugada. Lentos, cansados, como de alguien viejo. Bajaban la escalera… se detenían en el descanso… y volvían a subir.",
  S("servant_bed", CAND, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=[FL], grade="candle"),
  S("stairs_dark", cam=((0.7, 0.3, 1.3), (0.5, 0.55, 1.35), "inout"), fx=[FOG], tr="xfade", tl=0.8),
  sfx=[STEPS(2.0, 4, -12), STEPS(9.0, 3, -14)])
B("Algunos vieron la luz. Una vela que flotaba a la altura de un hombre, sin nadie que la sostuviera.",
  S("stairs_dark", FLOAT, cam=((0.65, 0.35, 1.25), (0.6, 0.4, 1.45), "in"), fx=[FOG]), sfx=[X("whisper", 2.0, -16, dur=3)])
B("Y una cocinera, cuentan, lo vio de frente. Un anciano pálido, de levita, con la vela en una mano y la otra extendida, como si quisiera detener a alguien.",
  S("stairs_ghost", GHOST, cam=((0.6, 0.4, 1.1), (0.68, 0.32, 1.4), "in"), fx=[FOG], grade="cold"),
  FLASH("ghost_flash"), sfx=SCARE)
B("Gritó. Soltó la charola. Y cuando los demás llegaron corriendo, en la escalera no había nadie. Solo un olor a cera quemada… y el frío.",
  S("candle_floor", cam=((0.5, 0.55, 1.15), (0.5, 0.55, 1.4), "in"), fx=[FOG], grade="cold"), sfx=[X("splash", 0.6, -14)])
B("La familia vendió la casa años después. Se fueron. Pero la escalera se quedó.",
  S("facade_night", FOGLAY, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.05), "out"), fx=[FOGL]), music="mystery", amb=NIGHT)
B("En mil ochocientos ochenta y uno, el piso de arriba lo rentó el club de caballeros más exclusivo de la ciudad. Bailes, cenas, brindis. Y aun así, cuentan que los meseros no querían quedarse solos cerca de la escalera después de medianoche.",
  S("ballroom", CAND, cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust", FL], grade="warm",
    text=[T("1881|el club de caballeros", "date", 1.0, 5.0)]),
  S("waiter_stairs", CAND, cam=((0.5, 0.5, 1.15), (0.6, 0.4, 1.35), "in"), fx=[FL, FOG], grade="candle", tr="xfade", tl=0.6),
  amb=["room"], sfx=[X("clock", 12.0, -12, dur=5)])
B("Uno de ellos contó que una noche, recogiendo copas, vio a un señor muy viejo parado en el descanso. Le preguntó si se le ofrecía algo. El viejo no contestó. Solo levantó la mano… y señaló la ventana.",
  S("stairs_ghost", GHOST, cam=((0.55, 0.45, 1.15), (0.68, 0.32, 1.45), "in"), fx=[FOG], grade="cold"),
  S("window_break", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.45), "in"), fx=[FOGL], grade="night", tr="xfade", tl=0.5, w=0.5), sfx=[X("whisper", 6.0, -14, dur=3)])
B("Luego vino la Revolución. Soldados, banquetes, gobiernos que llegaban y se iban.",
  S("revolution", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="sepia",
    text=[T("1910 – 1920|la Revolución", "date", 0.8, 4.5)]))
B("Y a finales de esa década, los hermanos Sanborn abrieron ahí su famoso restaurante, el mismo que sigue funcionando hoy.",
  S("patio_today", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25), "in"), fx=["dust"], grade="warm"))
B("En mil novecientos veinticinco, José Clemente Orozco pintó un mural en el muro de la escalera. Lo llamó Omnisciencia. La que todo lo ve.",
  S("stairs_today", cam=((0.5, 0.5, 1.1), (0.75, 0.3, 1.45), "in"), fx=["dust"], grade="warm",
    text=[T("OMNISCIENCIA|José Clemente Orozco, 1925", "big", 3.0, 8.0)]))
B("Y hay quien dice que no es casualidad. Que en esa escalera, más que en ningún otro lugar de la ciudad, alguien sigue mirando.",
  S("ghost_eyes", cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.5), "in"), fx=[FOG], grade="cold"), music="dread")
B("Meseros que cierran de noche cuentan que se oyen pasos en los escalones cuando ya no queda nadie. Que una luz pequeña, como de vela, baja hasta el descanso… y se apaga.",
  S("patio_night", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOG], grade="night"),
  S("stairs_dark", FLOAT, cam=((0.7, 0.3, 1.35), (0.7, 0.32, 1.55), "in"), fx=[FOG], tr="xfade", tl=0.6, out=0.6),
  sfx=[STEPS(1.5, 4, -12), X("whoosh", 9.5, -12)])

# ======================================================================== HISTORIA
B("Ahora, lo que sí es historia.",
  S("book", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2), "in"), fx=["dust"], tr="fade", tl=1.0, grade="sepia",
    text=[T("LO QUE DICE LA HISTORIA|", "chapter", 0.4, 4.0)]),
  music="calm", amb=["room"])
B("La Casa de los Azulejos existe, y puedes visitarla, en la calle de Madero, en el Centro Histórico de la Ciudad de México. Perteneció de verdad a los condes del Valle de Orizaba desde finales del siglo dieciséis.",
  S("facade_today", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25), "in"), fx=["dust"], grade="none",
    text=[T("Casa de los Azulejos|calle de Madero, Centro Histórico", "date", 1.0, 6.0)]))
B("En el siglo diecinueve, para abrir la avenida Cinco de Mayo, le cortaron una parte de su lado norte. Y en mil novecientos treinta y uno fue declarada monumento nacional.",
  S("facade_day", cam=((0.6, 0.5, 1.1), (0.4, 0.5, 1.2), "linear"), fx=["dust"], grade="sepia",
    text=[T("Monumento nacional|1931", "date", 6.0, 11.0)]))
B("Y la fachada de talavera de Puebla tampoco es leyenda. Pero según los documentos, no la mandó poner un hijo arrepentido, sino una mujer. Doña Graciana Suárez de Peredo, quinta condesa del Valle de Orizaba, hacia mil setecientos treinta y siete.",
  S("countess", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust"], grade="warm",
    text=[T("Graciana Suárez de Peredo|quinta condesa, hacia 1737", "date", 4.0, 10.0)]),
  S("tile_close2", cam=((0.4, 0.4, 1.15), (0.6, 0.55, 1.35), "linear"), fx=["dust"], grade="none", tr="xfade", tl=0.6))
B("La historia del hijo que no hacía casa es eso, una leyenda. Una manera de explicar un dicho que la gente usaba de verdad: hacer casa de azulejos, para decir que alguien había prosperado.",
  S("son_rich", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.3), "in"), fx=["dust"], grade="sepia"))
B("En cambio, el asesinato de mil ochocientos veintiocho sí aparece en las crónicas de la ciudad, durante los días del motín de la Acordada. Los detalles cambian según quién los cuente. Los fantasmas, como siempre, los puso la gente.",
  S("chronicle", cam=((0.45, 0.5, 1.15), (0.55, 0.5, 1.35), "linear"), fx=["dust"], grade="sepia"),
  S("stairs_today", cam=((0.5, 0.55, 1.1), (0.55, 0.45, 1.3), "in"), fx=["dust"], grade="night", tr="xfade", tl=0.8))

# ======================================================================== FINAL
B("Y aquí está la respuesta a la pregunta del principio. ¿Qué busca esa vela cada noche?",
  S("stairs_dark", FLOAT, cam=((0.6, 0.4, 1.1), (0.68, 0.32, 1.4), "in"), fx=[FOG]), music="dread", amb=["room", {"name": "drips", "gain": -14}])
B("Dicen que don Diego no baja la escalera por miedo. Baja porque sigue haciendo lo que hacía aquella noche. Cuidando la casa. Esperando al hombre que entró por la ventana… para que esta vez no llegue arriba.",
  S("stairs_ghost", GHOST, cam=((0.55, 0.45, 1.1), (0.68, 0.32, 1.4), "in"), fx=[FOG], grade="cold"),
  S("ghost_diego", cam=((0.5, 0.42, 1.15), (0.5, 0.42, 1.4), "in"), fx=[FOG, {"type": "flicker", "amp": 0.08}], grade="cold", tr="xfade", tl=0.8))
B("Porque Manuel Palacios nunca pagó. Y el viejo, todavía, no ha dejado de esperarlo.",
  S("ghost_eyes", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.5), "in"), fx=[FOG], grade="cold"), pause=1.0)
B("Así que si algún día subes esa escalera, entre los azulejos y el mural… y sientes que alguien te mira desde el descanso… no subas con prisa. No vaya a ser que te confunda.",
  S("stairs_pov", cam=((0.5, 0.6, 1.05), (0.6, 0.4, 1.35), "in"), fx=[FOG], grade="night"),
  FLASH("ghost_flash"), sfx=SCARE + [STEPS(0.5, 5, -12)])
B("¿Tú has entrado a la Casa de los Azulejos? ¿Te atreverías a subir esa escalera de noche? Te leo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("¿Subirías esa escalera de noche?|", "quote", 1.0, 7.0, pos="center")]), music="mystery", pause=0.8)
B("En el próximo video nos vamos a Oaxaca, a un pueblo donde, cada año, un hombre se casa con una lagarta. La leyenda del Hombre Caimán.",
  S("river_night", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOGL], grade="night",
    text=[T("PRÓXIMO VIDEO|El Hombre Caimán", "big", 2.0, 7.0)]), amb=["river", "crickets"])
B("Hasta la próxima leyenda. Y recuerda… en esa casa, alguien todavía tiene la vela encendida.",
  S("facade_night", FLOAT, cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.4), "in"), fx=[FOGL], out=2.0),
  pause=1.0, music="dread", amb=NIGHT)
VARIANTS = {}
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

story = {"title": "La Casa de los Azulejos", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "D", "seed": 131, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# La Casa de los Azulejos — guion\n",
                  "Narración en español (narrador: em_alex; voces de personajes: em_santa; Graciana: ef_dora).\n"]
WHO = {"ef_dora": "GRACIANA: ", "em_santa": "VOZ: "}
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
