#!/usr/bin/env python3
"""Builds story.json and script.md for 'La Xtabay'. Edit BEATS here, then run."""
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

XBACK = L("l_xtabay_back", blend="normal", anim=[{"type": "float", "amp": 0.004, "period": 6}])
XFRONT = L("l_xtabay_front", blend="normal", anim=[{"type": "float", "amp": 0.005, "period": 5}], fade_in=1.5)
WALK = L("l_lencho_walk", depth=1.05, anim=[{"type": "drift", "dx": 0.05, "ease": "linear"}])
BRUSH = L("l_brush_fg", depth=1.35, anim=[{"type": "sway", "deg": 1.2, "period": 7, "pivot": [0.5, 1.0]}])
WISP = L("l_wisp", blend="screen", opacity=[0, 0.8], fade_in=2.0, anim=[{"type": "drift", "dx": -0.05, "dy": -0.02}])
TEND = L("l_tendrils", anim=[{"type": "sway", "deg": 3, "period": 3.5, "pivot": [0.5, 0.2]}])
REDEYES = L("l_eyes", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 0.8}])

CAND = dict(voice="ef_dora", speed=0.86)
LENCHO = dict(voice="em_santa", speed=0.88)
ABUELA = dict(voice="ef_dora", speed=0.76)
XTAB = dict(voice="ef_dora", speed=0.74, fx="eco")

# ======================================================================== COLD OPEN
B("La voz sale de entre los árboles. Es suave… es dulce… y dice tu nombre.",
  S("monte_path", BRUSH, cam=((0.5, 0.55, 1.45), (0.5, 0.5, 1.15)), fx=[FOGL, "fireflies"], tr="fade", tl=1.2),
  pre=0.4, music="dread", amb=["night", {"name": "wind", "gain": -8}], sfx=[X("whisper", 2.0, -10, dur=3)])
B("Lencho se detiene en medio del camino blanco. Ya no se oyen los grillos. Ya no se oye nada.",
  S("monte_path", WALK, cam=((0.4, 0.6, 1.25), (0.45, 0.6, 1.4), "in"), fx=[FOGL]),
  amb=["wind"], sfx=[X("footsteps", 0.0, -10, dur=3)])
B("Ahí, bajo la ceiba más grande del monte, hay una mujer de espaldas. Lleva un huipil blanco… y se peina un cabello negro que le llega hasta los tobillos.",
  S("ceiba_night", cam=((0.5, 0.5, 1.0), (0.55, 0.58, 1.3)), fx=[FOGL]),
  S("xtabay_back", cam=((0.45, 0.4, 1.35), (0.45, 0.55, 1.1)), fx=[FOG, "dust"], tr="xfade", tl=0.8, w=1.2),
  sfx=[X("heartbeat", 3.0, -10, dur=8, bpm=70)])
B("Ven… acércate. Te estaba esperando.",
  S("xtabay_profile", cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.55), "in"), fx=[FOG], grade="moon"), **XTAB)
B("Y Lencho, que tenía mujer, que tenía casa, que había jurado no volver a beber… da el primer paso.",
  S("lencho_scared", cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.55), "in"), fx=[FL], w=1.3),
  S("xtabay_scare", tr="flash", tl=0.15, dur=2.0, cam=((0.5, 0.42, 1.4), (0.5, 0.42, 1.65)), fx=[SH(0, 0.6, 9)], grade="night"),
  pause=0.8, sfx=[X("sting", -0.1, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), fx=[FOGL, "fireflies"], tr="fade", tl=0.8,
    text=[T("LA XTABAY|la mujer de la ceiba", "title", 0.6, 6.4)]),
  pause=6.0, music="mystery", amb=["night", {"name": "crickets", "gain": -6}], sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Esta es la leyenda de la Xtabay, la más temida de Yucatán. Y antes de que termine, vas a saber qué tenía Lencho apretado en el puño… cuando por fin lo encontraron.",
  S("fist_closed", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=[FOG], grade="moon"))

# ======================================================================== I
B("Cuentan que esto pasó hace más de cien años, en los tiempos en que Yucatán vivía del henequén, el oro verde. Las haciendas se llenaban de pencas grises, y las chimeneas echaban humo de sol a sol.",
  S("hacienda", cam=((0.5, 0.5, 1.05), (0.45, 0.52, 1.25)), fx=["dust"], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO I|El camino blanco", "chapter", 0.6, 5.0)]),
  S("henequen", cam=((0.4, 0.55, 1.2), (0.6, 0.5, 1.1)), fx=["dust"], grade="warm", tr="xfade", tl=0.8,
    text=[T("Yucatán, hacia 1910|tiempos del henequén", "date", 0.5, 4.5)]), music="calm", amb=["wind"])
B("En un pueblito cerca de Valladolid vivía Lorenzo, al que todos llamaban Lencho. Cortaba pencas desde que salía el sol, con las manos rajadas por las espinas.",
  S("lencho_portrait", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), fx=["dust"], grade="warm"),
  S("henequen", cam=((0.7, 0.6, 1.5), (0.6, 0.6, 1.3)), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("El trabajo era duro y la paga, poca. Los peones vivían endeudados con la tienda de raya, y muchos buscaban en el aguardiente lo que no encontraban en ningún otro lado.",
  S("henequen", cam=((0.3, 0.5, 1.3), (0.45, 0.5, 1.15)), fx=["dust"], grade="sepia"),
  S("cantina", cam=((0.6, 0.5, 1.4), (0.5, 0.5, 1.25)), fx=[FL], grade="candle", tr="xfade", tl=0.6))
B("Su mujer, Candelaria, lo esperaba cada noche en la casita de paja, con la hamaca colgada y una vela encendida frente a la Virgen.",
  S("casa_maya", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.3)), fx=[FOGL, "fireflies"]),
  S("candelaria_portrait", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.4)), fx=[FL], grade="candle", tr="xfade", tl=0.6))
B("Lencho era bueno. Pero los sábados, cuando pagaban la raya, se iba a la cantina del pueblo vecino… y regresaba solo, de madrugada, por el camino del monte.",
  S("cantina", cam=((0.45, 0.5, 1.1), (0.55, 0.5, 1.3)), fx=[FL, "dust"], grade="candle"),
  S("monte_path", WALK, cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.25)), fx=[FOGL], tr="xfade", tl=0.6),
  amb=["room", {"name": "fire", "gain": -10}])
B("No te vayas por el monte, Lencho. Ahí está la ceiba. Ahí está ella.",
  S("candelaria_close", cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.5), "in"), fx=[FL], grade="candle"), amb=["crickets"], **CAND)
B("¿Ella quién, mujer? Esos son cuentos de las abuelas.",
  S("lencho_portrait", cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.5)), grade="candle"), **LENCHO)
B("Candelaria no contestó. Solo apretó el rosario… y miró hacia la oscuridad, como si alguien la estuviera escuchando.",
  S("candelaria_door", cam=((0.5, 0.5, 1.15), (0.6, 0.48, 1.4), "in"), fx=[FOGL, FL]), music="mystery")
B("Porque en ese pueblo todos sabían que, de vez en cuando, un hombre salía de noche… y ya no regresaba.",
  S("ceiba_night", XBACK, cam=((0.5, 0.55, 1.4), (0.5, 0.5, 1.1)), fx=[FOGL]),
  pause=0.9, sfx=[X("sting", 4.0, -6), X("owl", 1.0, -10)])

# ======================================================================== II
B("La abuela Nicolasa, la más vieja del pueblo, se lo contó a Lencho una noche junto al fogón. Hablaba despacio, en maya y en español, mientras las brasas tronaban.",
  S("abuela_fire", FIRE, cam=((0.5, 0.55, 1.1), (0.5, 0.52, 1.3)), fx=["embers"], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|Las dos mujeres", "chapter", 0.6, 5.0)]),
  music="sad", amb=["fire", {"name": "crickets", "gain": -8}])
B("Hace mucho, mucho tiempo, en este mismo pueblo, vivían dos mujeres. Las dos eran hermosas. Pero tenían el corazón al revés de como se veían.",
  S("abuela_portrait", FIRE, cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.4)), fx=["embers"], grade="candle"), **ABUELA)
B("La primera se llamaba Xkeban. La gente la señalaba en la calle. Decían que era una mujer de mala vida, que se entregaba al amor sin casarse, y las señoras se persignaban al verla pasar.",
  S("xkeban_portrait", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), fx=["dust"], grade="warm",
    text=[T("XKEBAN|la mujer señalada", "big", 0.6, 3.6, pos="bottom")]),
  S("village_old", cam=((0.5, 0.5, 1.1), (0.55, 0.5, 1.25)), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("Pero Xkeban tenía un corazón enorme. Lo poco que le regalaban se lo daba a los pobres. Curaba a los enfermos que nadie quería tocar. Y recogía a los perros heridos del camino.",
  S("xkeban_kind", cam=((0.45, 0.5, 1.1), (0.55, 0.5, 1.3)), fx=["dust", "fireflies"], grade="warm"), music="hope")
B("Y cuando los hombres del pueblo se burlaban de ella, Xkeban no les contestaba. Solo sonreía, y seguía su camino con sus perros detrás.",
  S("xkeban_portrait", cam=((0.45, 0.4, 1.4), (0.5, 0.4, 1.55)), fx=["dust"], grade="warm"))
B("La segunda se llamaba Utz Colel. Era decente, decían. Nunca había tenido novio. Caminaba muy derecha, con el cabello bien recogido… y todo el pueblo la admiraba.",
  S("utz_portrait", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), grade="cold",
    text=[T("UTZ COLEL|la mujer decente", "big", 0.6, 3.6, pos="bottom")]), music="mystery")
B("Pero Utz Colel era fría como el agua del cenote. Despreciaba a los pobres. Si un enfermo le pedía ayuda, le daba la espalda. Y por dentro… la envidia se la estaba comiendo.",
  S("utz_disdain", cam=((0.5, 0.5, 1.1), (0.6, 0.48, 1.3)), fx=[FOGL], grade="cold"),
  S("utz_portrait", cam=((0.48, 0.4, 1.5), (0.48, 0.38, 1.7), "in"), grade="cold", tr="xfade", tl=0.5, w=0.6))
B("Un día, Xkeban dejó de salir de su casa. Pasaron los días y nadie preguntó por ella. Hasta que un perfume dulce, delicioso, empezó a llenar todo el pueblo.",
  S("village_old", WISP, cam=((0.5, 0.5, 1.25), (0.5, 0.5, 1.1)), fx=["dust"], grade="sepia"), music="sad")
B("La encontraron dormida para siempre en su hamaca. Pero su cuerpo no olía a muerte. Olía a flores. Y sus perros la estaban cuidando, echados alrededor, sin dejar que nadie se acercara.",
  S("xkeban_hammock", WISP, cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.3)), fx=["dust"], grade="candle"))
B("Solo los pobres la enterraron. Y al día siguiente, sobre su tumba, había brotado una enredadera de flores blancas que nadie había sembrado: el xtabentún.",
  S("xkeban_grave", cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3)), fx=["fireflies"], grade="moon"),
  S("xtabentun_flower", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.35), "in"), fx=["dust"], tr="xfade", tl=0.8,
    text=[T("XTABENTÚN|la flor de Xkeban", "big", 0.5, 4.0, pos="bottom")]), music="hope")
B("Poco después murió Utz Colel. El pueblo entero fue a su entierro, con cantos y con velas. Pero de su cuerpo salía un olor tan podrido que nadie aguantaba estar cerca.",
  S("utz_funeral", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=[FOGL, FL], grade="candle"), music="tension", amb=["wind"])
B("Le llevaron flores. Al amanecer, las flores habían desaparecido. Y en su lugar creció el tzacam: un cactus lleno de espinas, con una flor que huele mal.",
  S("utz_grave", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.3)), fx=[FOGL], grade="cold"),
  S("tzacam", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.45), "in"), tr="xfade", tl=0.6, grade="cold",
    text=[T("TZACAM|la flor de Utz Colel", "big", 0.5, 4.0, pos="bottom")]))
B("Y entonces Utz Colel, desde la tumba, se llenó de rabia. Ella había sido buena, decía. ¿Por qué a la otra le tocaban las flores?",
  S("abuela_portrait", FIRE, cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.55), "in"), fx=["embers"], grade="candle"), **ABUELA)
B("Cuentan que llamó a los espíritus malos del monte, y les pidió volver. Volver a ser mujer. Para hacer con el amor lo mismo que había hecho Xkeban…",
  S("utz_pact", REDEYES, cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.35), "in"), fx=[FOGL, {"type": "pulse", "bpm": 60, "amp": 0.1}], grade="night"),
  music="dread", sfx=[X("whisper", 2.0, -8, dur=5), X("riser", 3.0, -10, dur=5)])
B("Pero ella no sabía amar. Así que volvió para otra cosa. Para atraer a los hombres que caminan solos… y llevárselos.",
  S("utz_pact", REDEYES, cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.55)), fx=[FOGL]),
  S("xtabay_bust", tr="flash", tl=0.2, cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.4)), fx=[SH(0, 0.5, 7)], grade="moon",
    text=[T("LA XTABAY", "big", 0.3, 3.0, pos="bottom")]),
  pause=0.8, sfx=[X("sting", -0.1, -2, at_scene=1), X("boom", 0.0, -4, at_scene=1)])
B("Por eso, mijo, si oyes que una mujer te llama desde la ceiba… no la mires. No le contestes. Y sobre todo… no la sigas.",
  S("abuela_portrait", FIRE, cam=((0.5, 0.4, 1.5), (0.5, 0.38, 1.7), "in"), fx=["embers"], grade="candle"), music="mystery", **ABUELA)
B("Y si a ti también te contaron esta historia de niño, suscríbete y activa la campanita, porque aquí seguimos contando las leyendas que México no quiere olvidar.",
  S("title_bg", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.2)), fx=[FOGL, "fireflies"], tr="xfade", tl=0.6))

# ======================================================================== III
B("Lencho se rió de la abuela. Y el sábado siguiente, como siempre, se fue a la cantina.",
  S("cantina", cam=((0.4, 0.5, 1.2), (0.55, 0.5, 1.1)), fx=[FL, "dust"], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO III|La ceiba", "chapter", 0.6, 5.0)]), music="calm", amb=["room", {"name": "fire", "gain": -10}])
B("Esa noche bebió más que nunca. Bebió por las espinas, por la raya que no alcanzaba, por el patrón de la hacienda. Y cuando salió, ya pasaba de la medianoche.",
  S("lencho_drunk", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), fx=[FL], grade="candle"),
  S("cantina_out", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.25)), fx=[FOGL], tr="xfade", tl=0.6), sfx=[X("bell", 9.0, -10, freq=180)])
B("El camino blanco brillaba bajo la luna. A los lados, el monte bajo, los chacás de tronco rojo, los zapotes… y el silencio.",
  S("monte_path", WALK, BRUSH, cam=((0.45, 0.55, 1.15), (0.55, 0.55, 1.3)), fx=[FOGL, "fireflies"]),
  music="mystery", amb=["night", {"name": "crickets", "gain": -6}], sfx=[X("footsteps", 0.5, -12, dur=6)])
B("Entonces lo olió. Un perfume dulce, como de flores blancas. Como de xtabentún.",
  S("xtabentun_night", WISP, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=["fireflies"]), amb=["wind"])
B("Y la vio.",
  S("ceiba_night", XBACK, cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=[FOGL]), pre=0.8, pause=1.2, music="dread",
  sfx=[X("sting", 0.2, -6)])
B("Estaba bajo la ceiba, en el claro, con la luna encima. Se peinaba despacio, mechón por mechón, con un peine hecho de espinas.",
  S("xtabay_back", cam=((0.45, 0.55, 1.05), (0.45, 0.5, 1.25)), fx=[FOG, "dust"]),
  S("comb_spines", cam=((0.5, 0.5, 1.15), (0.5, 0.6, 1.35)), tr="xfade", tl=0.6, grade="moon"))
B("Lorenzo… ¿por qué caminas solo? Ven conmigo. Aquí no hace frío.",
  S("xtabay_profile", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.4)), fx=[FOG], grade="moon"), **XTAB)
B("Lencho nunca le había dicho su nombre. Nadie en ese monte sabía su nombre. Pero las piernas ya no le obedecían.",
  S("lencho_scared", cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.45), "in"), fx=[FL]), sfx=[X("heartbeat", 0.0, -9, dur=8, bpm=90)])
B("La mujer se volteó. Era la más hermosa que había visto en su vida. Los ojos grandes, negros, brillantes como el agua de un cenote de noche.",
  S("xtabay_bust", cam=((0.5, 0.4, 1.15), (0.5, 0.36, 1.5), "in"), fx=["dust"], grade="moon"), music="mystery")
B("Ella empezó a caminar hacia adentro del monte. Y él la siguió.",
  S("monte_dense", XFRONT, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3), "in"), fx=[FOGL]),
  sfx=[X("whisper", 1.0, -12, dur=3)])
B("Detrás de él, el camino blanco se fue quedando lejos. La luz de la luna ya no alcanzaba a entrar entre las ramas. Y el perfume se hacía cada vez más fuerte, tan dulce que mareaba.",
  S("monte_path", WISP, cam=((0.5, 0.5, 1.4), (0.5, 0.5, 1.1), "out"), fx=[FOGL]),
  S("xtabentun_night", WISP, cam=((0.5, 0.5, 1.3), (0.45, 0.5, 1.5)), tr="xfade", tl=0.6))
B("Las ramas le rasgaban la camisa. Las espinas le abrían la piel. Pero él no sentía nada. Solo oía su risa, cada vez más cerca… y cada vez más lejos.",
  S("monte_dense", BRUSH, cam=((0.3, 0.55, 1.3), (0.7, 0.5, 1.3), "linear"), fx=[FOGL, {"type": "shake", "amp": 3, "at": [0, 20]}]),
  S("lencho_scared", cam=((0.5, 0.4, 1.5), (0.5, 0.4, 1.3)), fx=[FL], tr="xfade", tl=0.4, w=0.6),
  music="tension", sfx=[X("whisper", 3.0, -9, dur=4, pan=-0.6), X("whisper", 7.0, -9, dur=4, pan=0.6)])
B("Hasta que llegaron otra vez a la ceiba. La misma ceiba. Habían caminado en círculo toda la noche.",
  S("ceiba_night", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.0), "out"), fx=[FOGL]), sfx=[X("boom", 3.5, -6)])
B("Ella se detuvo entre las raíces enormes, que salían de la tierra como paredes. Le tendió los brazos. Y Lencho, temblando, se acercó.",
  S("roots", XFRONT, cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.35), "in"), fx=[FOGL]), sfx=[X("heartbeat", 0.0, -8, dur=9, bpm=110)])
B("Entonces notó algo. El cabello de la mujer se movía solo. No había viento. Y el cabello se movía… como se mueven las serpientes.",
  S("hair_snakes", TEND, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=[FOG], grade="night"),
  music="dread", sfx=[X("whisper", 2.0, -8, dur=5), X("riser", 4.0, -8, dur=5)])
B("Ella abrió la boca para besarlo. Y su boca siguió abriéndose…",
  S("xtabay_bust", cam=((0.5, 0.42, 1.4), (0.5, 0.45, 1.6), "in"), grade="moon"),
  S("xtabay_scare", tr="flash", tl=0.15, dur=2.6, cam=((0.5, 0.45, 1.5), (0.5, 0.45, 1.8)), fx=[SH(0, 0.8, 10)],
    text=[T("NO LA SIGAS", "big", 0.3, 2.4, pos="bottom")]),
  pause=1.0, sfx=[X("sting", -0.1, -1, at_scene=1), X("boom", 0.0, -2, at_scene=1)])
B("En el pueblo, Candelaria despertó de golpe. La vela frente a la Virgen se había apagado sola.",
  S("house_inside_dark", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.35)), fx=[FOG], grade="night"),
  music="silence", amb=["wind"], sfx=[X("gust", 3.0, -8)])

# ======================================================================== IV
B("Hasta aquí, la leyenda. Pero, ¿de dónde viene la Xtabay?",
  S("codex", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=["dust", {"type": "darken", "amount": 0.55}], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|Lo que dice la historia", "chapter", 0.6, 5.0)]), music="mystery", amb=["room"])
B("Su nombre recuerda a Ixtab, una diosa maya que aparece en un texto atribuido a fray Diego de Landa, escrito hacia mil quinientos sesenta y seis. Durante mucho tiempo se le relacionó con la muerte. Hoy, algunos investigadores proponen que era una diosa de la caza: la señora del lazo, la que atrapa.",
  S("landa_book", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=[FL, "dust"], grade="candle",
    text=[T("Relación de las cosas de Yucatán|atribuida a fray Diego de Landa, hacia 1566", "date", 0.5, 5.0)]),
  S("codex", cam=((0.4, 0.5, 1.4), (0.6, 0.5, 1.4), "linear"), fx=["dust"], grade="warm", tr="xfade", tl=0.6))
B("Y está la ceiba, el yaxché, el árbol sagrado de los mayas. Para ellos, sus raíces bajaban al inframundo, su tronco estaba en la tierra de los vivos y sus ramas tocaban el cielo. Todavía hoy, en muchos pueblos de Yucatán, nadie se atreve a cortar una ceiba vieja.",
  S("ceiba_sacred", cam=((0.5, 0.75, 1.3), (0.5, 0.3, 1.3)), fx=["dust", "fireflies"]))
B("Por eso la Xtabay espera ahí. En el árbol que une a los vivos con los muertos. Dicen que sus víctimas se quedan atrapadas bajo esas raíces, en lo más hondo de la tierra.",
  S("roots", cam=((0.5, 0.6, 1.2), (0.5, 0.7, 1.45), "in"), fx=[FOGL]))
B("Antonio Mediz Bolio escribió sobre la Xtabay en mil novecientos veintidós, en su libro La tierra del faisán y del venado. Y la versión de las dos mujeres, con sus dos flores, parece haber tomado forma a principios del siglo veinte. Hoy es la que se cuenta en casi todas las casas de Yucatán.",
  S("old_book", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.3)), fx=[FL], grade="candle",
    text=[T("La tierra del faisán y del venado|Antonio Mediz Bolio, 1922", "date", 0.5, 5.5)]))
B("Las flores son reales. El xtabentún es una enredadera de flores blancas. Con la miel de las abejas que la visitan, y con anís, se hace un licor dulce que todavía se vende en Yucatán… y que lleva su nombre.",
  S("xtabentun_flower", cam=((0.4, 0.5, 1.3), (0.55, 0.5, 1.15)), fx=["dust"]),
  S("bottle", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.3)), fx=["dust"], grade="candle", tr="xfade", tl=0.6), music="calm")
B("El tzacam también existe: un cactus pequeño, redondo, cubierto de espinas. Y dicen que con esas espinas se peina la Xtabay.",
  S("tzacam", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), grade="cold"),
  S("comb_spines", cam=((0.5, 0.5, 1.3), (0.5, 0.45, 1.5)), grade="moon", tr="xfade", tl=0.6, w=0.6))
B("En Quintana Roo se cuenta que la Xtabay no castiga a cualquiera, sino a los borrachos, a los ladrones y a los hombres violentos. Por eso las abuelas todavía la usan para advertir a los muchachos: no andes solo de noche… y no vuelvas tomado.",
  S("abuela_fire", FIRE, cam=((0.5, 0.55, 1.15), (0.5, 0.5, 1.3)), fx=["embers"], grade="candle"))
B("Y algunos estudiosos dicen algo más: que antes de la Colonia, la Xtabay era un espíritu del monte, guardiana de los árboles y de los animales. Que fueron los siglos los que la convirtieron en demonio.",
  S("xtabay_guardian", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25)), fx=["fireflies", FOGL], grade="moon"), music="mystery")

# ======================================================================== V
B("Pero volvamos a Lencho. Al amanecer, Candelaria salió con los hombres del pueblo a buscarlo por el camino blanco.",
  S("search_dawn", cam=((0.5, 0.5, 1.1), (0.55, 0.52, 1.3)), fx=[FOGL], grade="cold", tr="fade", tl=1.0,
    text=[T("CAPÍTULO V|Lo que tenía en el puño", "chapter", 0.6, 5.0)]), music="sad", amb=["wind"])
B("Gritaban su nombre entre los árboles. Lorenzo. Lorenzo. Y el monte no contestaba. Solo, a veces, algo se movía entre las ramas… algo blanco, que desaparecía en cuanto volteaban.",
  S("monte_dense", cam=((0.4, 0.5, 1.2), (0.6, 0.5, 1.2), "linear"), fx=[FOGL], grade="cold"),
  S("monte_dense", XFRONT, cam=((0.55, 0.5, 1.4), (0.55, 0.5, 1.5)), fx=[FOGL], grade="cold", dur=1.6, tr="cut"),
  S("monte_dense", cam=((0.55, 0.5, 1.5), (0.55, 0.5, 1.55)), fx=[FOGL], grade="cold", dur=1.6))
B("Lo buscaron un día entero. Y otro. Y otro. Al tercer día, uno de los muchachos sintió un perfume dulce… y siguió el olor hasta la ceiba.",
  S("monte_path_day", WISP, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL], grade="cold"), music="tension")
B("Ahí, entre las raíces, estaba el sombrero de Lencho. Y más adentro, donde las raíces se juntan y no entra la luz… estaba él.",
  S("roots_hat", cam=((0.5, 0.6, 1.1), (0.5, 0.55, 1.45), "in"), fx=[FOGL], grade="cold"), sfx=[X("sting", 6.5, -5)])
B("Tenía los ojos abiertos y la camisa rota, con la piel llena de rasguños finos, como de espinas. Y en la cara, una sonrisa que nadie quiso volver a mirar.",
  S("roots_dark", cam=((0.5, 0.55, 1.3), (0.5, 0.55, 1.5), "in"), fx=[FOG, {"type": "pulse", "bpm": 50, "amp": 0.1}], grade="cold"),
  music="dread", sfx=[X("heartbeat", 0.0, -10, dur=8, bpm=56)])
B("Candelaria le abrió la mano, que tenía apretada con todas sus fuerzas.",
  S("fist_closed", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.55), "in"), grade="cold"))
B("Adentro había una espina de tzacam. Y enredado en ella… un cabello negro, larguísimo. Tan largo que, al jalarlo, parecía no terminar nunca.",
  S("fist_open", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), grade="cold",
    text=[T("UN CABELLO NEGRO", "big", 3.0, 6.0, pos="bottom")]), sfx=[X("sting", 3.0, -4)])
B("Dicen que Candelaria quemó ese cabello en el fogón. Y que esa noche, desde el monte, se oyó una risa de mujer.",
  S("candelaria_fire", FIRE, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), fx=["embers"], grade="candle"),
  amb=["fire", {"name": "night", "gain": -6}], sfx=[X("whisper", 5.0, -6, dur=3)])
B("Desde entonces, en ese pueblo nadie regresa solo de la cantina. Y cuando un hombre siente, de noche, un perfume dulce en el camino… se persigna, baja la mirada y camina más rápido.",
  S("monte_path", WALK, BRUSH, cam=((0.5, 0.5, 1.1), (0.5, 0.55, 1.3)), fx=[FOGL, "fireflies"]), music="mystery", amb=["night"])
B("Porque la Xtabay sigue ahí. Bajo la ceiba. Peinándose.",
  S("xtabay_back", cam=((0.5, 0.6, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FOG, "dust"], grade="moon"), pause=0.6)
B("¿Por qué caminas solo?",
  S("xtabay_scare", tr="flash", tl=0.15, cam=((0.5, 0.45, 1.5), (0.5, 0.45, 1.75)), fx=[SH(0, 0.6, 8)], grade="night", out=0.8),
  pause=1.4, music="silence", sfx=[X("sting", -0.1, -2), X("boom", 0.0, -3)], **XTAB)
B("Y ahora dime tú: ¿en tu familia se cuenta la leyenda de la Xtabay? ¿O alguien que conoces dice que la vio? Cuéntamelo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOGL, "fireflies"], tr="fade", tl=0.8), music="mystery", amb=["crickets"])
B("En el próximo video nos quedamos en Yucatán. Porque en la milpa, de noche, alguien avienta piedritas, esconde las herramientas y se ríe como niño. Son los aluxes… y no les gusta que te olvides de ellos.",
  S("aluxes_tease", cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.05)), fx=[FOGL, "fireflies"], grade="night",
    text=[T("PRÓXIMO VIDEO|Los Aluxes", "big", 2.0, 7.0)]), sfx=[X("whisper", 3.0, -12, dur=4)])
B("Hasta la próxima leyenda. Y si hueles flores en la oscuridad… no voltees.",
  S("ceiba_night", XBACK, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.0), "out"), fx=[FOGL], out=2.0), pause=1.0, music="dread")
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

story = {"title": "La Xtabay: la mujer de la ceiba que llama a los hombres que caminan solos", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "E", "seed": 21, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# La Xtabay — guion\n",
                  "Narración en español (narrador: em_alex; Candelaria, la abuela Nicolasa y la Xtabay: ef_dora; Lencho: em_santa).\n"]
WHO = {"ef_dora": "CANDELARIA / ABUELA / XTABAY: ", "em_santa": "PERSONAJE: "}
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
