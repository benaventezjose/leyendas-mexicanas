#!/usr/bin/env python3
"""Builds story.json and script.md for 'El Nahual'. Edit BEATS here, then run."""
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

LUPE = dict(voice="ef_dora", speed=0.86)
TOMAS = dict(voice="em_santa", speed=0.88)
FERMIN = dict(voice="em_santa", speed=0.78)
ABUELA = dict(voice="ef_dora", speed=0.76)
BEAST = dict(voice="em_santa", speed=0.74, fx="eco")

# ======================================================================== COLD OPEN
B("La lumbre del fogón todavía está encendida. Pero en la choza… no hay nadie.",
  S("hut_inside", FIRE, cam=((0.5, 0.62, 1.45), (0.5, 0.58, 1.2)), fx=[FOG, "embers"], grade="candle", tr="fade", tl=1.2),
  pre=0.4, music="dread", amb=["fire", {"name": "night", "gain": -10}], sfx=[X("fire", 0.0, -12, dur=8)])
B("Tomás empuja la puerta de carrizo con el machete. Huele a copal… y a pelo mojado.",
  S("hut_door", FIRE, cam=((0.42, 0.55, 1.15), (0.5, 0.55, 1.4), "in"), fx=[FOG, FL], grade="candle"),
  sfx=[X("door", 0.4, -6)])
B("Y entonces lo ve. Junto a las brasas, doblado como ropa antes de dormir… hay algo que no debería estar ahí.",
  S("tomas_portrait", FIRE, cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.5), "in"), fx=[FL], grade="candle", w=1.1),
  S("hut_inside", FIRE, cam=((0.42, 0.72, 1.7), (0.42, 0.7, 1.5)), fx=[FL, "embers"], grade="candle"),
  sfx=[X("heartbeat", 0.0, -9, dur=8, bpm=84)])
B("Afuera, algo aúlla. Y un coyote no aúlla… con voz de hombre.",
  S("hill_moon", cam=((0.5, 0.5, 1.05), (0.55, 0.55, 1.3)), fx=[FOGL]),
  S("beast_eyes", tr="flash", tl=0.2, cam=((0.5, 0.45, 1.35), (0.5, 0.45, 1.6)), fx=[SH(0, 0.6, 9)], grade="night",
    text=[T("VOZ DE HOMBRE", "big", 0.3, 2.6, pos="bottom")]),
  pause=0.9, sfx=[X("howl", 0.4, -4), X("sting", -0.1, -2, at_scene=1), X("boom", 3.6, -3)])
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), fx=[FOGL, "dust"], tr="fade", tl=0.8,
    text=[T("EL NAHUAL|el que se viste de animal", "title", 0.6, 6.4)]),
  pause=6.0, music="mystery", amb=["wind", {"name": "crickets", "gain": -6}], sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Esta es la leyenda del nahual. Y antes de que termine, vas a saber qué encontró Tomás junto al fuego… y por qué en algunos pueblos de México todavía se pintan cruces blancas en las puertas.",
  S("crosses_doors", cam=((0.35, 0.5, 1.3), (0.6, 0.5, 1.15)), fx=[FOGL], grade="moon"))

# ======================================================================== I
B("Cuentan que esto pasó en un pueblito de la sierra, de esos que no salen en los mapas. Casas de adobe con techo de teja, magueyes a la orilla del camino… y un cerro negro que, de noche, parecía respirar.",
  S("village_night", cam=((0.5, 0.5, 1.05), (0.45, 0.55, 1.25)), fx=[FOGL, "fireflies"], tr="fade", tl=1.0,
    text=[T("CAPÍTULO I|Las gallinas", "chapter", 0.6, 5.0)]),
  S("hill_moon", cam=((0.5, 0.55, 1.2), (0.5, 0.48, 1.05)), fx=[FOG], tr="xfade", tl=0.8), music="calm")
B("Ahí vivían Tomás y Lupe, recién casados. Él sembraba maíz y frijol en la ladera. Ella criaba gallinas y guajolotes, y los cuidaba como si fueran de la familia.",
  S("couple_dawn", cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.3)), fx=["dust"], grade="warm", w=1.2),
  S("lupe_portrait", cam=((0.5, 0.42, 1.25), (0.5, 0.4, 1.45)), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("Lupe tenía la costumbre de dejarle al santito de la casa una veladora y un vaso de agua cada noche. Decía que así nada malo entraba. Pero ese otoño, la veladora empezó a apagarse sola… siempre a la misma hora.",
  S("altar_candle", CANDLE, cam=((0.5, 0.5, 1.15), (0.5, 0.48, 1.4), "in"), fx=[FL], grade="candle"), sfx=[X("gust", 6.5, -10)])
B("Una mañana de noviembre, Lupe salió al corral con su rebozo y su olla de maíz… y se quedó helada.",
  S("corral_dawn", cam=((0.4, 0.55, 1.15), (0.55, 0.6, 1.35)), fx=[FOGL], grade="cold"),
  music="mystery", amb=["wind"])
B("Las gallinas estaban regadas por el suelo. Sin una mordida. Sin una gota de sangre. Solo plumas… y unas huellas enormes en el lodo.",
  S("dead_hens", cam=((0.5, 0.6, 1.2), (0.5, 0.65, 1.5), "in"), fx=[FOGL, {"type": "darken", "amount": 0.2}], grade="cold"),
  S("tracks_mud", tr="flash", tl=0.2, cam=((0.5, 0.5, 1.3), (0.62, 0.55, 1.55)), fx=[FOGL], grade="cold",
    text=[T("HUELLAS|más grandes que una mano", "big", 0.3, 3.0)]),
  sfx=[X("sting", -0.1, -3, at_scene=1)])
B("Tomás… ven a ver esto. Esas no son patas de coyote.",
  S("lupe_scared", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.5)), grade="cold"), **LUPE)
B("Tomás se agachó. Las huellas eran de perro, sí. Pero cada una era tan grande como la palma de su mano. Y la última, junto a la cerca… ya no era de pata. Era la marca de un pie descalzo.",
  S("tomas_portrait", cam=((0.5, 0.42, 1.2), (0.5, 0.45, 1.4)), grade="cold"),
  S("footprint", cam=((0.5, 0.5, 1.15), (0.5, 0.55, 1.6), "in"), fx=[FOGL, {"type": "pulse", "bpm": 70, "amp": 0.1}], grade="cold", tr="xfade", tl=0.5),
  sfx=[X("heartbeat", 4.0, -9, dur=6, bpm=70)])
B("Esa misma semana pasó lo mismo en otras casas. Una vaca amaneció echada, sin fuerzas para levantarse. A los marranos de don Chencho los encontraron temblando en un rincón, con los ojos en blanco.",
  S("village_dawn", cam=((0.4, 0.5, 1.2), (0.6, 0.5, 1.2)), fx=[FOGL], grade="cold"))
B("Y cada noche, a la misma hora, todos los perros del pueblo se ponían a aullar al mismo tiempo… y luego, de golpe, se callaban.",
  S("dogs_roofs", cam=((0.3, 0.5, 1.3), (0.7, 0.5, 1.3), "linear"), fx=[FOGL]),
  amb=["night", {"name": "wind", "gain": -6}], sfx=[X("howl", 0.5, -8), X("howl", 1.8, -10, pan=-0.5), X("howl", 3.0, -10, pan=0.6)])
B("Imagina que estás acostado en tu petate, en la oscuridad completa, y escuchas cómo todos los perros se callan a la vez. Ese silencio… es peor que cualquier aullido.",
  S("bedroom_dark", CANDLE, cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.45), "in"), fx=[{"type": "darken", "amount": 0.25}], grade="night"),
  amb=[], music="silence", pause=1.2)

# ======================================================================== II
B("Una noche, Tomás decidió esperarlo. Afiló el machete en la piedra, apagó el quinqué y se sentó detrás de la puerta del corral.",
  S("tomas_wait", LANTERN, cam=((0.5, 0.55, 1.2), (0.45, 0.5, 1.35)), fx=[FOGL], tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|Los ojos", "chapter", 0.6, 5.0)]),
  music="tension", amb=["crickets", {"name": "wind", "gain": -8}], sfx=[X("whoosh", 2.0, -14)])
B("No vayas, Tomás. Mi abuela dice que a esos animales no se les busca… que ellos lo buscan a uno.",
  S("lupe_window", CANDLE, cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.4)), grade="candle"), **LUPE)
B("Si no lo paro yo, mañana se va a llevar algo más que gallinas.",
  S("tomas_portrait", LANTERN, cam=((0.5, 0.45, 1.45), (0.5, 0.42, 1.25)), grade="night"), **TOMAS)
B("Pasó la medianoche. El frío de la sierra se le metía en los huesos. Y uno por uno, los grillos se fueron callando.",
  S("corral_night", cam=((0.5, 0.55, 1.1), (0.5, 0.58, 1.3)), fx=[FOGL]),
  amb=["wind"], sfx=[X("clock", 0.0, -16, dur=4)])
B("Entonces escuchó los pasos. No eran pasos de animal. Eran lentos… pesados… como de alguien que camina en cuatro patas sin estar acostumbrado.",
  S("fence_gap", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.5), "in"), fx=[FOGL, {"type": "pulse", "bpm": 80, "amp": 0.1}]),
  sfx=[X("footsteps", 0.5, -10, dur=7), X("heartbeat", 0.5, -10, dur=8, bpm=80)])
B("Por una rendija de la cerca vio la silueta. Un perro negro, más grande que un becerro, con el lomo erizado y la cabeza gacha, olfateando la tierra.",
  S("corral_night", BEAST_WALK, cam=((0.35, 0.6, 1.3), (0.55, 0.6, 1.4)), fx=[FOGL]),
  S("beast_side", cam=((0.45, 0.5, 1.1), (0.55, 0.5, 1.35)), fx=[FOGL], tr="xfade", tl=0.5), music="dread")
B("Y cuando la luna le dio en la cara… Tomás vio sus ojos.",
  S("beast_eyes", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=[{"type": "darken", "amount": 0.35}]),
  pause=0.3, sfx=[X("riser", -1.0, -6, dur=3.5)])
B("No eran ojos de perro. Eran ojos de hombre. Ojos cansados, con párpados, que parpadeaban despacio. Y lo estaban mirando a él.",
  S("beast_eyes", tr="flash", tl=0.2, cam=((0.5, 0.42, 1.45), (0.5, 0.41, 1.65)), fx=[SH(0, 0.6, 10)],
    text=[T("OJOS DE HOMBRE", "big", 0.3, 3.0, pos="bottom")]),
  sfx=[X("sting", -0.1, -1), X("boom", 0.0, -3)])
B("Y el animal… sonrió.",
  S("beast_smile", cam=((0.5, 0.5, 1.3), (0.5, 0.52, 1.5), "in"), fx=[FL], grade="blood"), pause=1.0, sfx=[X("whisper", 0.2, -12, dur=3)])
B("Tomás gritó y lanzó el machetazo. Sintió cómo el filo mordía algo duro. El perro soltó un chillido que no era de perro… y se perdió en el monte.",
  S("strike", tr="flash", tl=0.2, cam=((0.5, 0.5, 1.2), (0.52, 0.5, 1.35)), fx=[SH(0, 1.0, 12)], grade="night", w=0.8),
  S("hill_moon", BEAST_WALK, cam=((0.5, 0.55, 1.15), (0.6, 0.5, 1.3)), fx=[FOGL], tr="xfade", tl=0.4),
  sfx=[X("whoosh", 0.8, -3), X("boom", 1.2, -4), X("howl", 3.2, -5)])
B("Sobre la tierra quedó un rastro de gotas oscuras. Y el rastro subía, derechito, cerro arriba… hacia la choza de don Fermín.",
  S("blood_trail", cam=((0.5, 0.75, 1.4), (0.5, 0.45, 1.2)), fx=[FOGL], grade="night"),
  S("hut_hill", FIRE, cam=((0.5, 0.5, 1.15), (0.6, 0.45, 1.5), "in"), fx=[FOGL], tr="xfade", tl=0.6),
  music="mystery", sfx=[X("heartbeat", 2.0, -10, dur=5, bpm=64)])
B("Si estas historias te ponen la piel chinita, suscríbete y quédate con nosotros. Todavía falta lo peor de esta noche.",
  S("title_bg", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.05)), fx=[FOGL]), pause=0.6)

# ======================================================================== III
B("Don Fermín era el curandero del pueblo. Un viejo amable, de bigote blanco, que curaba el empacho con hierbas y el susto con huevo y copal. Todos en el pueblo le debían algún favor.",
  S("healer_herbs", CANDLE, cam=((0.5, 0.55, 1.2), (0.45, 0.55, 1.4)), fx=["dust"], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO III|La mano vendada", "chapter", 0.6, 5.0)]),
  S("fermin_portrait", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3)), fx=["dust"], grade="warm", tr="xfade", tl=0.6),
  music="calm", amb=["city"])
B("A la mañana siguiente, Tomás bajó a la plaza. Y ahí estaba don Fermín, sentado en su banca de siempre… con la mano derecha envuelta en un trapo manchado.",
  S("plaza_morning", cam=((0.4, 0.5, 1.1), (0.55, 0.55, 1.3)), fx=["dust"], grade="warm"),
  S("bandage_hand", cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.5), "in"), grade="warm", tr="xfade", tl=0.5),
  sfx=[X("bell", 0.5, -14, freq=180)])
B("¿Qué le pasó en la mano, don Fermín?",
  S("tomas_portrait", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.4)), grade="warm"), **TOMAS)
B("Nada, muchacho. Me corté anoche… partiendo leña.",
  S("fermin_portrait", cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.5)), grade="warm"), **FERMIN)
B("Tomás regresó a su casa sin decir nada. Pero esa tarde notó algo que nunca había visto: cuando don Fermín pasaba por la calle, los perros del pueblo se escondían debajo de las carretas, con la cola entre las patas.",
  S("plaza_dogs", cam=((0.35, 0.5, 1.15), (0.6, 0.55, 1.3)), fx=["dust"], grade="warm"), music="mystery")
B("Y entonces el viejo lo miró. Con esos mismos ojos. Cansados. Con párpados. Que parpadeaban… despacio.",
  S("fermin_eyes", cam=((0.5, 0.53, 1.3), (0.5, 0.52, 1.7), "in"), fx=[{"type": "pulse", "bpm": 60, "amp": 0.1}], grade="warm"),
  music="dread", amb=[], sfx=[X("heartbeat", 0.5, -8, dur=6, bpm=60)])
B("Uno debe tener cuidado con lo que corta de noche, Tomás. A veces… el filo se regresa.",
  S("fermin_sinister", tr="flash", tl=0.2, cam=((0.5, 0.52, 1.5), (0.5, 0.52, 1.65)), fx=[SH(0, 0.5, 6)], grade="blood"),
  pause=1.0, sfx=[X("sting", -0.1, -3)], **FERMIN)
B("Para entender a don Fermín hay que ir mucho más atrás. Siglos atrás.",
  S("codex_paper", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25)), fx=["dust"], grade="sepia", tr="fade", tl=0.8), music="mystery", amb=["wind"])
B("La palabra nahual viene del náhuatl, nahualli. Los estudiosos la traducen como disfraz, como lo que está oculto… o como lo que es mi vestidura.",
  S("codex_paper", cam=((0.3, 0.45, 1.5), (0.5, 0.5, 1.4)), fx=["dust"], grade="sepia",
    text=[T("NAHUALLI|disfraz · lo oculto · mi vestidura", "big", 1.5, 6.0)]))
B("Para los pueblos antiguos de Mesoamérica, cada persona nacía con un tonal: un animal compañero que le tocaba según el día de su nacimiento en el calendario sagrado. Su destino iba amarrado al tuyo. Si a él le pasaba algo… a ti también.",
  S("tonal_wheel", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3)), fx=["dust", {"type": "pulse", "bpm": 50, "amp": 0.06}], grade="warm", w=1.3),
  S("baby_animal", CANDLE, cam=((0.5, 0.5, 1.2), (0.5, 0.48, 1.4)), fx=["dust"], grade="candle", tr="xfade", tl=0.6))
B("Pero unos pocos podían hacer algo más: dejar su forma humana y vestirse con la de su animal. Esos eran los nahuales.",
  S("shadow_transform", FIRE, cam=((0.5, 0.5, 1.15), (0.55, 0.45, 1.35)), fx=[FL], grade="candle"))
B("En muchos pueblos se dice que el nahual escoge el animal que mejor le sirve: perro negro, coyote, guajolote, burro… o hasta un gato que camina en dos patas. Y que lo único que nunca puede cambiar… son los ojos.",
  S("animals_row", cam=((0.25, 0.5, 1.3), (0.75, 0.5, 1.3), "linear"), fx=[FOGL], grade="night"))
B("En el siglo dieciséis, el fraile franciscano Bernardino de Sahagún recogió lo que contaban los ancianos nahuas. Había nahuales buenos, que cuidaban y protegían a su pueblo… y otros que usaban su poder para hacer daño.",
  S("sahagun_desk", CANDLE, cam=((0.45, 0.5, 1.15), (0.55, 0.45, 1.35)), fx=["dust", FL], grade="candle",
    text=[T("Nueva España, siglo XVI|fray Bernardino de Sahagún", "date", 0.8, 5.5)]))
B("Y se decía que hasta los dioses tenían nahual. El de Tezcatlipoca, el señor del espejo humeante, era el jaguar: el que camina en la noche sin hacer un solo ruido.",
  S("jaguar_mirror", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.4), "in"), fx=[FOG, "embers"], grade="night"),
  sfx=[X("whisper", 2.0, -14, dur=4)])
B("Con la llegada de los españoles, el nahual se volvió brujo, y el brujo se volvió pacto con el diablo. Pero en los pueblos, la gente nunca dejó de contar lo mismo: hay quien de noche se quita lo humano… y sale.",
  S("church_village", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25)), fx=[FOGL], grade="moon"),
  S("beast_side", cam=((0.6, 0.5, 1.3), (0.45, 0.5, 1.15)), fx=[FOGL], tr="xfade", tl=0.6))

# ======================================================================== IV
B("Tomás le contó todo a Lupe. Y Lupe fue a ver a su abuela Chabela, que pasaba de los noventa años y recordaba las cosas como las contaban los de antes.",
  S("abuela_portrait", CANDLE, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3)), fx=[FL], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|Las cruces de cal", "chapter", 0.6, 5.0)]),
  music="mystery", amb=["fire"])
B("El nahual no se muere con fierro, mija. El nahual se quita la piel junto a la lumbre, da tres maromas y se va de animal. Si le encuentras la piel… échale sal y ceniza. Así ya no se la puede volver a poner.",
  S("abuela_portrait", CANDLE, cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.55)), fx=[FL], grade="candle", w=1.3),
  S("salt_ash", CANDLE, cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.4)), fx=[FL], grade="candle", tr="xfade", tl=0.6), **ABUELA)
B("Esa tarde, todo el pueblo pintó cruces blancas de cal en puertas y ventanas. Colgaron tijeras abiertas en forma de cruz. Dejaron veladoras prendidas toda la noche.",
  S("crosses_doors", cam=((0.6, 0.5, 1.15), (0.35, 0.5, 1.3)), fx=[FOGL], grade="moon"),
  S("scissors_candle", CANDLE, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.45)), fx=[FL], grade="candle", tr="xfade", tl=0.6), amb=["night"])
B("Pero el nahual ya sabía quién lo había herido.",
  S("beast_eyes", cam=((0.5, 0.45, 1.2), (0.5, 0.45, 1.45), "in"), fx=[{"type": "darken", "amount": 0.3}]), music="dread", pause=0.9,
  sfx=[X("howl", 0.8, -9)])
B("A medianoche, Lupe despertó. Algo raspaba la puerta. Despacio. De arriba abajo. Como uñas sobre la madera.",
  S("bedroom_dark", CANDLE, cam=((0.5, 0.5, 1.2), (0.6, 0.5, 1.4)), grade="night"),
  S("door_scratch", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.45), "in"), fx=[{"type": "pulse", "bpm": 90, "amp": 0.1}], grade="night", tr="xfade", tl=0.4),
  sfx=[X("whisper", 2.0, -10, dur=5), X("heartbeat", 2.0, -9, dur=7, bpm=90)])
B("Lupita… ábreme. Soy yo… Tomás.",
  S("door_scratch", tr="flash", tl=0.2, cam=((0.5, 0.5, 1.45), (0.5, 0.5, 1.6)), fx=[SH(0, 0.5, 6)], grade="night",
    text=[T("ÁBREME", "big", 0.3, 2.6)]),
  pause=0.8, sfx=[X("sting", -0.1, -2), X("knock", 2.2, -4, times=3)], **BEAST)
B("Lupe miró a su lado. Tomás estaba ahí, dormido junto a ella, respirando hondo.",
  S("lupe_scared", CANDLE, cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.5), "in"), grade="candle"))
B("La voz siguió. Imitaba perfecto la voz de su marido. Le decía que tenía frío, que lo dejara entrar. Y cuando entendió que nadie le iba a abrir… se rió.",
  S("door_outside", EYES, cam=((0.5, 0.55, 1.2), (0.5, 0.52, 1.4)), fx=[FOGL], grade="night"),
  sfx=[X("whisper", 0.5, -12, dur=6)])
B("En la mañana, sobre la cruz de cal, había cuatro rasguños profundos. Como si algo hubiera querido borrarla… y no hubiera podido.",
  S("cross_scratched", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.55), "in"), fx=[FOGL], grade="cold"), music="mystery", amb=["wind"])
B("Y no creas que esto es cosa del pasado. En Tlaxcala, en las faldas del volcán La Malinche, todavía se habla de nahuales y de tlahuelpuchis, las brujas que vuelan de noche como bolas de lumbre.",
  S("malinche_lights", cam=((0.5, 0.55, 1.05), (0.5, 0.45, 1.3)), fx=[FOGL, "fireflies"], grade="night",
    text=[T("Tlaxcala|faldas de La Malinche", "date", 0.8, 5.0)]))
B("Y en el año dos mil veintidós, en Cocoyoc, Morelos, unos vecinos escucharon ruidos extraños en la madrugada. ¿Y sabes qué hicieron? Pintaron cruces blancas en sus puertas y ventanas. Igual que en el pueblo de Tomás.",
  S("cocoyoc_street", cam=((0.35, 0.5, 1.15), (0.6, 0.5, 1.3)), fx=[FOGL], grade="moon",
    text=[T("Cocoyoc, Morelos, 2022|vecinos pintan cruces en sus puertas", "date", 1.0, 6.0)]))

# ======================================================================== V
B("Tomás entendió que no había otra salida. Antes de salir, Lupe le amarró al cuello una cruz de palma bendita y le habló al oído.",
  S("village_night", cam=((0.5, 0.5, 1.15), (0.5, 0.52, 1.3)), fx=[FOGL], tr="fade", tl=1.0,
    text=[T("CAPÍTULO V|La piel junto al fogón", "chapter", 0.6, 5.0)]),
  S("lupe_window", CANDLE, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), grade="candle", tr="xfade", tl=0.6), music="tension", amb=["fire"])
B("Si te habla, no le contestes. Y si te llama por tu nombre… menos.",
  S("lupe_scared", CANDLE, cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.55)), grade="candle"), **LUPE)
B("La noche siguiente, cuando todos los perros se callaron a la vez, salió de su casa y subió el cerro con un costal de sal y una jícara llena de ceniza.",
  S("path_hill", LANTERN, cam=((0.5, 0.65, 1.2), (0.5, 0.45, 1.3)), fx=[FOGL]),
  S("tomas_climb", cam=((0.45, 0.55, 1.15), (0.55, 0.5, 1.35)), fx=[FOGL], tr="xfade", tl=0.6),
  music="tension", amb=["wind", {"name": "night", "gain": -8}], sfx=[X("footsteps", 1.0, -12, dur=10)])
B("La choza de don Fermín estaba al final de una vereda, entre magueyes. Por las rendijas del carrizo salía una luz roja, como de brasas.",
  S("hut_hill", FIRE, cam=((0.4, 0.55, 1.3), (0.5, 0.5, 1.6), "in"), fx=[FOGL]))
B("Tomás se asomó. El viejo estaba de pie frente al fogón, rezando algo en una lengua muy antigua, una lengua que ya nadie en el pueblo hablaba.",
  S("fermin_ritual", FIRE, cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.4)), fx=[FL, "embers"], grade="candle"),
  sfx=[X("whisper", 0.5, -10, dur=8), X("fire", 0.0, -12, dur=8)])
B("Don Fermín se quitó el sombrero. Luego la camisa. Y luego… siguió quitándose cosas que no son ropa.",
  S("fermin_back", FIRE, cam=((0.5, 0.5, 1.2), (0.5, 0.48, 1.45), "in"), fx=[FL], grade="candle"),
  pause=0.9, music="dread")
B("La sombra en la pared se dobló. Una maroma. Dos. Tres. Y la sombra ya no era de hombre: tenía orejas largas, hocico, y una cola que barría el suelo.",
  S("shadow_transform", FIRE, cam=((0.5, 0.5, 1.2), (0.6, 0.45, 1.4)), fx=[FL, SH(1.5, 2.0, 5), SH(2.6, 3.1, 5)], grade="candle"),
  S("shadow_dog", FIRE, tr="flash", tl=0.2, cam=((0.5, 0.45, 1.25), (0.5, 0.45, 1.45)), fx=[FL, SH(0, 0.6, 10)], grade="blood",
    text=[T("TRES MAROMAS", "big", 0.3, 2.6)]),
  sfx=[X("boom", 1.6, -8), X("boom", 2.7, -7), X("sting", -0.1, -1, at_scene=1)])
B("El perro negro salió por la puerta del fondo, cojeando de la pata derecha… y se perdió en la noche.",
  S("hill_moon", BEAST_WALK, cam=((0.5, 0.55, 1.2), (0.6, 0.5, 1.35)), fx=[FOGL]), sfx=[X("howl", 2.5, -8)])
B("Tomás entró. La lumbre seguía encendida. Y junto a las brasas, doblada con mucho cuidado, como quien deja la ropa antes de dormirse… estaba la piel de don Fermín. Vacía. Todavía tibia.",
  S("hut_inside", FIRE, cam=((0.5, 0.6, 1.15), (0.5, 0.62, 1.4)), fx=[FOG, "embers"], grade="candle"),
  S("skin_by_fire", FIRE, tr="flash", tl=0.2, cam=((0.5, 0.62, 1.3), (0.5, 0.62, 1.55), "in"), fx=[FL, "embers"], grade="candle",
    text=[T("SU PIEL", "big", 0.4, 3.0)]),
  sfx=[X("sting", -0.1, -1, at_scene=1), X("heartbeat", 0.0, -8, dur=12, bpm=96)])
B("Le temblaban las manos. Pero hizo lo que le dijo la abuela: le echó sal. Le echó ceniza. Y salió corriendo cerro abajo, sin voltear.",
  S("salt_ash", FIRE, cam=((0.5, 0.55, 1.3), (0.5, 0.6, 1.5), "in"), fx=[FL], grade="candle", w=1.2),
  S("path_hill", cam=((0.5, 0.45, 1.3), (0.5, 0.7, 1.15)), fx=[FOGL], tr="xfade", tl=0.4),
  sfx=[X("whoosh", 0.2, -10), X("footsteps", 4.5, -8, dur=4)])
B("Antes del amanecer, se escuchó en todo el pueblo un aullido largo, desesperado. Venía de la choza del curandero. Y entre los aullidos… una voz.",
  S("hut_hill", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3)), fx=[FOGL], grade="cold"),
  sfx=[X("howl", 0.6, -4), X("howl", 4.0, -6)])
B("Pellejito… pellejito… ¿qué no me conoces?",
  S("beast_door", tr="flash", tl=0.2, cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.5)), fx=[SH(0, 0.6, 8), FOGL], grade="cold",
    text=[T("¿QUÉ NO ME CONOCES?", "big", 0.4, 3.4)]),
  pause=1.0, sfx=[X("sting", -0.1, -2)], **BEAST)
B("Toda la madrugada se oyó lo mismo. Y cuando el sol por fin salió detrás del cerro, el aullido se apagó.",
  S("dawn_hill", cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.05)), fx=[FOGL], grade="warm", tr="xfade", tl=1.0), music="sad", amb=["wind"])
B("Dicen que nunca encontraron a don Fermín. En la choza solo quedó su ropa, un puño de sal… y un montón de pelo negro junto a la lumbre apagada.",
  S("hut_empty_dawn", cam=((0.5, 0.55, 1.15), (0.5, 0.6, 1.4), "in"), fx=["dust"], grade="cold"))

# ======================================================================== ENDING
B("La choza se vino abajo con las lluvias de ese año. Nadie quiso levantarla. Y dicen que hasta el día de hoy, en ese pedazo de cerro, no crece ni el maguey.",
  S("hut_ruin", cam=((0.5, 0.5, 1.1), (0.5, 0.52, 1.3)), fx=[FOGL, "dust"], grade="cold"))
B("Pero esa no es la última parte de la historia.",
  S("village_night", cam=((0.5, 0.5, 1.25), (0.5, 0.5, 1.1)), fx=[FOGL], tr="fade", tl=0.8), music="dread", amb=["night"], pause=0.8)
B("Años después, Lupe contaba que, algunas noches, un perro negro, cojo de la pata derecha, se sentaba en el camino frente a su casa. No ladraba. No se acercaba a las cruces. Solo miraba. Y parpadeaba despacio.",
  S("road_dog", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.4), "in"), fx=[FOGL]),
  S("lupe_window", CANDLE, cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.45)), grade="candle", tr="xfade", tl=0.6))
B("Porque un nahual que pierde su piel… no se muere. Se queda esperando. Buscando otra.",
  S("beast_eyes", tr="flash", tl=0.2, cam=((0.5, 0.43, 1.5), (0.5, 0.43, 1.8), "in"), fx=[SH(0, 0.5, 8)],
    text=[T("BUSCANDO OTRA", "big", 0.4, 3.0, pos="bottom")]),
  pause=1.0, sfx=[X("sting", -0.1, -1), X("boom", 0.0, -3)])
B("Así que si esta noche, de regreso a casa, ves un perro a la orilla del camino que te mira sin moverse… fíjate bien en sus ojos. Y si te llama por tu nombre… no le contestes.",
  S("road_dog", cam=((0.5, 0.55, 1.4), (0.5, 0.5, 1.7), "in"), fx=[FOGL, {"type": "pulse", "bpm": 60, "amp": 0.1}], out=1.0),
  pause=1.6, music="silence", sfx=[X("heartbeat", 0.0, -9, dur=10, bpm=60), X("whisper", 6.0, -10, dur=3)])
B("¿En tu pueblo también se cuentan historias de nahuales? ¿En qué animal se convierten allá: perro, guajolote, coyote? Te leo en los comentarios.",
  S("village_dawn", cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.2)), fx=[FOGL], grade="warm", tr="fade", tl=0.8), music="mystery", amb=["wind"])
B("En el próximo video viajamos a Yucatán, a la sombra de una ceiba, donde una mujer hermosa se peina el cabello y llama a los hombres que caminan solos de noche. Se llama la Xtabay… y el que la sigue, no regresa igual.",
  S("xtabay_tease", cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.05)), fx=[FOGL, "fireflies"], grade="night",
    text=[T("PRÓXIMO VIDEO|La Xtabay", "big", 2.0, 7.0)], out=2.0),
  pause=1.0, music="dread", sfx=[X("whisper", 3.0, -12, dur=4)])

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

story = {"title": "El Nahual: el curandero que de noche se quitaba la piel", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "D", "seed": 12, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# El Nahual — guion\n",
                  "Narración en español (narrador: em_alex; Lupe y la abuela Chabela: ef_dora; Tomás, don Fermín y el nahual: em_santa).\n"]
WHO = {"ef_dora": "LUPE / ABUELA: ", "em_santa": "PERSONAJE: "}
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
