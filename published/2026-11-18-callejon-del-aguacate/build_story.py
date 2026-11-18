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
VELAC = L("l_vela_close", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 2.2}])
VELA = L("l_vela_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.2, "speed": 2.2}])
LAMP = L("l_lamp_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.4}])
CANDLE = L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 2.0}])
FOGLAY = L("l_fog", blend="screen", opacity=[0, 0.8], anim=[{"type": "drift", "dx": -0.06, "ease": "linear"}])
BRANCH = L("l_branches", depth=1.3, anim=[{"type": "sway", "deg": 1.2, "period": 6, "pivot": [0.5, 0.0]}])
KIDG = L("l_child_ghost", blend="screen", opacity=[0, 0.8], fade_in=1.5, anim=[{"type": "float", "amp": 0.004, "period": 4}, {"type": "flicker", "amp": 0.2, "speed": 0.8}])
SOLG = L("l_soldier_ghost", depth=1.02, opacity=[0, 0.95], fade_in=2.0, anim=[{"type": "flicker", "amp": 0.1, "speed": 0.6}])
TROMPO = L("l_trompo", depth=1.1, anim=[{"type": "shake", "amp": 0.0015}, {"type": "pulse", "amp": 0.01, "period": 0.3, "pivot": [0.5, 0.85]}])
WALKER = L("l_walker", depth=1.2, anim=[{"type": "drift", "dx": 0.0, "dy": -0.015, "ease": "linear"}, {"type": "float", "amp": 0.003, "period": 0.9}])
LANTERNS = L("l_lanterns", depth=1.08, anim=[{"type": "drift", "dx": 0.04, "ease": "linear"}, {"type": "flicker", "amp": 0.1, "speed": 1.2}])
SOLWALK = L("l_soldier_walk", depth=1.08, anim=[{"type": "drift", "dx": 0.08, "ease": "linear"}])
KIDFOLLOW = L("l_child_follow", depth=1.08, anim=[{"type": "drift", "dx": 0.08, "ease": "linear"}, {"type": "float", "amp": 0.004, "period": 0.6}])

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)


KID = dict(voice="ef_dora", speed=0.95)
KIDE = dict(voice="ef_dora", speed=0.9, fx="eco")
SOL = dict(voice="em_santa", speed=0.8)

# ======================================================================== COLD OPEN
B("Coyoacán. Pasada la medianoche.",
  S("alley_night", LAMP, VELA, FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.25), "in"), fx=["dust"], tr="fade", tl=1.2),
  pre=0.6, music="dread", amb=["night", {"name": "wind", "gain": -9}], sfx=[X("bell", 0.4, -14, freq=150)])
B("Imagina un callejón de piedra, tan angosto que casi puedes tocar las dos paredes.",
  S("alley_deep", WALKER, LAMP, cam=((0.5, 0.6, 1.15), (0.5, 0.55, 1.35), "in"), fx=[FOGL]),
  sfx=[X("footsteps", 0.0, -8, dur=7)])
B("A tus espaldas, escuchas una risita. La risa de un niño.",
  S("alley_deep", KIDG, cam=((0.5, 0.55, 1.3), (0.5, 0.55, 1.45)), fx=[FOGL, PU(70, 0.06)], grade="cold"),
  sfx=[X("whisper", 1.6, -12, dur=2.5)], music="tension")
B("¿Juegas conmigo?",
  S("alley_deep", KIDG, cam=((0.5, 0.6, 1.45), (0.5, 0.6, 1.6)), fx=[FOGL], grade="cold"), pause=0.9, **KIDE)
B("Volteas. No hay nadie. Solo un trompo de madera… girando solo.",
  S("cobbles_night", TROMPO, cam=((0.5, 0.65, 1.2), (0.5, 0.7, 1.5), "in"), fx=["dust", FOGL], grade="moon"))
B("En la esquina, la veladora de un nicho se apaga. Y bajo el aguacate, alguien de uniforme te está mirando.",
  S("niche_dark", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.4)), fx=[FOG], dur=3.2),
  S("alley_night", SOLG, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.5), "in"), fx=[FOGL, PU(80, 0.08)], grade="cold"),
  S("ghost_flash", tr="flash", tl=0.12, dur=1.5, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.5)), fx=[SH(0, 0.5, 9)]),
  pause=0.6, sfx=[X("riser", -3.5, -8, at_scene=2, dur=3.5), X("sting", 0.0, -2, at_scene=2), X("boom", 0.0, -3, at_scene=2)])
B("",
  S("title_bg", KIDG, cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("EL CALLEJÓN DEL AGUACATE|el niño que quería jugar", "title", 0.6, 6.4)]),
  pause=5.2, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Sobre una barda se asoman las ramas de un aguacate viejo. Y en la esquina, dentro de un nicho, una Virgen te mira a la luz de una sola veladora.",
  S("tree_moon", BRANCH, cam=((0.5, 0.45, 1.05), (0.5, 0.4, 1.25)), fx=["dust"], w=1.0),
  S("niche_close", VELAC, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.4), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.7, w=1.2))
B("El aire huele a tierra mojada y a cera derretida. Tus pasos rebotan entre las paredes.",
  S("cobbles_night", cam=((0.5, 0.6, 1.1), (0.5, 0.65, 1.3), "in"), fx=["dust", FOGL], grade="moon"), sfx=[X("footsteps", 0.0, -9, dur=5)])
B("Lo que pasó en este callejón le dio una fama que los vecinos de Coyoacán todavía cuentan en voz baja. Y quién es ese hombre de uniforme… lo vas a saber al final.",
  S("soldier_shadow", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="cold"))
B("Esta es la leyenda del Callejón del Aguacate.",
  S("alley_night", LAMP, VELA, cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.1)), fx=[FOGL], grade="moon"))

# ======================================================================== I
B("Coyoacán quiere decir, según la explicación más aceptada, lugar de coyotes. Mucho antes de la llegada de los españoles ya era un pueblo importante, a la orilla del gran lago.",
  S("coyotes", cam=((0.4, 0.5, 1.05), (0.55, 0.45, 1.2), "linear"), fx=["dust"], tr="fade", tl=1.0,
    text=[T("CAPÍTULO I|El barrio de Santa Catarina", "chapter", 0.6, 5.0)]),
  S("lake", cam=((0.5, 0.5, 1.05), (0.6, 0.5, 1.25)), fx=["dust"], grade="moon", tr="xfade", tl=0.8),
  music="calm", amb=["crickets"], sfx=[X("howl", 1.5, -10)])
B("En mil quinientos veintiuno, tras la caída de Tenochtitlan, Hernán Cortés instaló aquí su primer gobierno, mientras la vieja capital se levantaba de sus ruinas.",
  S("plaza_coyoacan", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="warm",
    text=[T("Coyoacán, 1521|primer ayuntamiento de la Nueva España", "date", 0.4, 4.8)]))
B("Siglos después, por sus calles caminaron pintores, poetas y viajeros. Pero de noche, cuando se apagaban las pocas lámparas, Coyoacán volvía a ser lo que siempre había sido: un lugar de sombras y de huertas silenciosas.",
  S("plaza_coyoacan", LAMP, cam=((0.6, 0.5, 1.3), (0.4, 0.5, 1.4), "linear"), fx=[FOG], grade="night"))
B("Al sur de la plaza fue creciendo un barrio pequeño, alrededor de una capilla dedicada a Santa Catarina. Calles empedradas, bardas de piedra, huertas llenas de árboles frutales.",
  S("santa_catarina", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="warm"),
  S("alley_day", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=["dust"], tr="xfade", tl=0.8))
B("Entre esas calles hay un callejón de apenas cien metros de largo y unos cuatro de ancho, que nace cerca de la avenida Francisco Sosa. Es tan estrecho que hoy muchos coches no caben.",
  S("alley_day", cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.55), "in"), fx=["dust"]))
B("Su nombre viene de un árbol: un aguacate enorme que de día daba sombra a los vecinos… y que de noche convertía el callejón en un túnel de oscuridad.",
  S("tree_close", BRANCH, cam=((0.5, 0.6, 1.05), (0.5, 0.4, 1.3)), fx=["dust"], grade="warm", w=1.0),
  S("alley_night", BRANCH, LAMP, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=[FOG], tr="xfade", tl=1.0, w=1.0))
B("Mucha gente cree que esta historia es de tiempos de la Colonia. Pero cuentan que ocurrió mucho después: en los años treinta del siglo pasado, cuando gobernaba el presidente Lázaro Cárdenas.",
  S("pueblo_1930", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="sepia",
    text=[T("Coyoacán, años treinta|un pueblo a las afueras de la ciudad", "date", 0.5, 5.0)]))
B("Coyoacán todavía era casi un pueblo, separado de la ciudad por campos y caminos de tierra. Por las tardes se oía a los niños jugando en la calle: canicas, trompos, las escondidas.",
  S("kids_play", cam=((0.4, 0.55, 1.05), (0.6, 0.5, 1.25), "linear"), fx=["dust"], grade="warm"),
  amb=["city"], sfx=[X("whisper", 2.0, -20, dur=3)])
B("Las casas tenían patios con macetas, gallinas y lavaderos de piedra. Y por las noches se encendían veladoras frente a las imágenes de los santos.",
  S("veladoras", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.4)), fx=[FL], grade="candle"))
B("Y en una de esas casas, junto al aguacate, vivía un hombre que no soportaba ese ruido.",
  S("house_soldier", cam=((0.5, 0.5, 1.05), (0.55, 0.45, 1.35), "in"), fx=["dust"], grade="night"),
  music="tension", amb=["night"])

# ======================================================================== II
B("Era un militar retirado. Nadie recuerda su nombre. En el barrio solo lo llamaban así: el soldado.",
  S("soldier_portrait", CANDLE, cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|El soldado", "chapter", 0.6, 4.8, pos="bottom")]), music="mystery")
B("Había peleado, decían, en los años de la Revolución. Volvió con el cabello gris antes de tiempo, con una cicatriz en la mano… y con el pecho lleno de medallas.",
  S("war_memory", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25)), fx=["embers", "ash"], grade="blood", w=1.0),
  S("medals_close", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.4), "in"), fx=["dust"], grade="candle", tr="xfade", tl=0.8, w=1.0),
  sfx=[X("boom", 0.5, -14), X("boom", 2.2, -16)])
B("Nunca hablaba de lo que había visto. Pero a veces, cuando un camión pasaba tronando por la avenida, el soldado se tiraba al suelo y se cubría la cabeza. Luego se levantaba, se sacudía el uniforme… y fingía que no había pasado nada.",
  S("soldier_ruin", cam=((0.5, 0.45, 1.1), (0.5, 0.45, 1.3)), fx=["dust"], grade="sepia", w=1.0),
  S("war_flash", tr="flash", tl=0.1, dur=1.0, fx=[SH(0, 0.4, 6)], grade="blood"),
  S("soldier_portrait", cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.4)), fx=["dust"], grade="sepia", tr="xfade", tl=0.6, w=0.8),
  sfx=[X("boom", 0.0, -6, at_scene=1)])
B("Cada domingo se ponía su uniforme viejo, bien planchado, y caminaba por el callejón muy despacio, con la espalda recta y la mirada fija al frente.",
  S("alley_day", SOLWALK, cam=((0.45, 0.55, 1.15), (0.55, 0.55, 1.3), "linear"), fx=["dust"]),
  sfx=[X("footsteps", 0.3, -10, dur=6)])
B("Las medallas brillaban con el sol. Él quería que todos las vieran. Pero no quería que nadie le hablara.",
  S("medals_close", cam=((0.4, 0.5, 1.4), (0.6, 0.5, 1.5), "linear"), fx=["dust"], grade="warm"))
B("Vivía solo. Sin esposa, sin hijos, sin amigos. Por las noches, los vecinos veían una luz en su ventana hasta muy tarde.",
  S("house_soldier", cam=((0.6, 0.45, 1.3), (0.6, 0.42, 1.5), "in"), fx=[FOG]))
B("Algunos decían que no podía dormir. Que, en cuanto cerraba los ojos… volvía a la guerra.",
  S("room_soldier", CANDLE, cam=((0.5, 0.5, 1.05), (0.45, 0.5, 1.3), "in"), fx=[FL], grade="candle", w=1.2),
  S("war_flash", tr="flash", tl=0.1, dur=1.2, fx=[SH(0, 0.5, 8)], grade="blood"),
  sfx=[X("boom", 0.0, -4, at_scene=1), X("sting", 0.0, -5, at_scene=1)])
B("Las señoras del barrio les advertían a sus hijos: no molesten al soldado. Déjenlo en paz.",
  S("kids_play", cam=((0.6, 0.55, 1.3), (0.5, 0.55, 1.45)), fx=["dust"], grade="sepia"))
B("Una noche, un vecino que volvía tarde lo encontró parado bajo el aguacate, en posición de firmes, hablando solo.",
  S("alley_night", SOLG, BRANCH, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FOGL], grade="moon"),
  sfx=[X("whisper", 1.0, -14, dur=4)])
B("Cuando el vecino le dio las buenas noches, el soldado volteó muy despacio… y lo miró como si no supiera quién era.",
  S("soldier_cold", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.6), "in"), fx=[PU(70, 0.06)], grade="cold"),
  sfx=[X("heartbeat", 0.5, -10, dur=6, bpm=70)])

# ======================================================================== III
B("Si te gustan estas historias, suscríbete al canal: aquí contamos las leyendas de todo México.",
  S("santa_catarina", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.3)), fx=["dust"], grade="night", tr="fade", tl=0.8), music="calm")
B("Pero hubo un niño que no hizo caso.",
  S("child_portrait", cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.25), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.8,
    text=[T("CAPÍTULO III|El niño", "chapter", 0.6, 4.6, pos="bottom")]))
B("Tenía unos siete años y vivía al otro lado del callejón con su mamá. Era flaco, inquieto, con las rodillas raspadas y un trompo de madera siempre en la bolsa del pantalón.",
  S("child_portrait", cam=((0.5, 0.4, 1.3), (0.5, 0.45, 1.5), "in"), fx=["dust"], grade="warm", w=1.2),
  S("trompo_day", cam=((0.5, 0.6, 1.1), (0.5, 0.6, 1.35), "in"), fx=["dust"], tr="xfade", tl=0.8, w=1.0))
B("Desde la primera vez que vio pasar al soldado con su uniforme, se quedó con la boca abierta.",
  S("child_look", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="warm"))
B("Lo seguía a distancia. Se paraba frente a su puerta. Miraba las medallas como quien mira un tesoro.",
  S("alley_day", SOLWALK, KIDFOLLOW, cam=((0.45, 0.55, 1.2), (0.55, 0.55, 1.35), "linear"), fx=["dust"]),
  sfx=[X("footsteps", 0.0, -12, dur=5)])
B("Señor… ¿esa medalla se la dieron por valiente?",
  S("child_look", cam=((0.5, 0.42, 1.45), (0.5, 0.42, 1.6)), fx=["dust"], grade="warm"), **KID)
B("El soldado no contestó. Entró a su casa y cerró la puerta.",
  S("door_closed", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="sepia"),
  sfx=[X("door", 1.6, -4)])
B("Al día siguiente el niño volvió. Y al otro. Y al otro.",
  S("door_closed", cam=((0.3, 0.55, 1.25), (0.5, 0.55, 1.4)), fx=["dust"], grade="warm"),
  sfx=[X("knock", 0.8, -8, times=3)])
B("Su mamá le pedía que no fuera. Que el señor estaba enfermo de tristeza. Pero un niño de siete años no entiende de tristezas. Solo entiende que alguien está solo… y que nadie debería jugar solo.",
  S("child_portrait", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.35)), fx=["dust"], grade="sepia"), music="sad")
B("¿Juega conmigo? Nomás un ratito.",
  S("child_portrait", cam=((0.5, 0.42, 1.5), (0.5, 0.42, 1.65)), fx=["dust"], grade="warm"), **KID)
B("Le ofrecía su trompo. Le enseñaba a enredar el cordel. Le contaba que, de grande, él también iba a ser soldado.",
  S("trompo_day", cam=((0.45, 0.55, 1.3), (0.55, 0.55, 1.5)), fx=["dust"], grade="warm"),
  S("kids_play", cam=((0.5, 0.55, 1.2), (0.45, 0.55, 1.35)), fx=["dust"], grade="warm", tr="xfade", tl=0.8))
B("Y cada vez, el hombre se ponía más rígido. Más callado. Más pálido.",
  S("soldier_cold", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3)), fx=["dust"], grade="cold"), music="tension")
B("Vete a tu casa, niño. No me hables.",
  S("soldier_cold", cam=((0.5, 0.42, 1.5), (0.5, 0.42, 1.7), "in"), fx=[PU(80, 0.06)], grade="cold"), **SOL)
B("Los vecinos notaban cómo le temblaban las manos cuando el niño se acercaba. Nadie sabía si era enojo… o algo peor. Algo que había traído de la guerra y que nunca se fue.",
  S("hands_shake", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=[SH(0, 99, 2)], grade="candle", w=1.2),
  S("war_memory", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.35)), fx=["embers"], grade="blood", tr="xfade", tl=0.8, w=1.0),
  sfx=[X("heartbeat", 0.0, -12, dur=8, bpm=80)])
B("Hasta que llegó una tarde gris, al final de un día muy largo.",
  S("alley_dusk", cam=((0.5, 0.5, 1.05), (0.5, 0.52, 1.25), "in"), fx=[FOG], grade="cold", out=0.8), amb=["wind"])

# ======================================================================== IV
B("El niño lo esperaba, como siempre, junto al aguacate. Tenía el trompo en la mano.",
  S("alley_dusk", KIDFOLLOW, cam=((0.5, 0.55, 1.15), (0.5, 0.55, 1.3)), fx=[FOG], grade="cold", tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|La tarde gris", "chapter", 0.6, 4.8)]), music="dread")
B("¿Ahora sí juega conmigo?",
  S("child_look", cam=((0.5, 0.42, 1.4), (0.5, 0.42, 1.55)), fx=["dust"], grade="cold"), **KID)
B("Cuentan que el soldado se detuvo. Que lo miró durante un largo rato, sin decir nada. Y que, de pronto, sin aviso… levantó la mano.",
  S("soldier_cold", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.55), "in"), fx=[PU(90, 0.08)], grade="cold", w=1.4),
  S("hand_raise", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FOG], grade="blood", w=0.8),
  sfx=[X("heartbeat", 0.0, -8, dur=9, bpm=110), X("riser", 4.0, -10, dur=4)])
B("Fue un solo golpe. Uno solo.",
  S("red_flash", tr="flash", tl=0.1, dur=1.2, fx=[SH(0, 0.6, 12)], grade="blood"),
  S("cobbles_dusk", TROMPO, cam=((0.5, 0.65, 1.3), (0.55, 0.7, 1.45)), fx=[FOG], grade="cold"),
  pre=0.3, sfx=[X("boom", 0.0, -2), X("sting", 0.0, -4)])
B("El trompo rodó por el empedrado hasta detenerse junto a la pared. Y el niño… ya no se levantó.",
  S("trompo_still", cam=((0.5, 0.65, 1.2), (0.5, 0.65, 1.5), "in"), fx=[FOG], grade="cold",
    text=[T("SILENCIO", "big", 3.5, 7.0)]), music="sad", pause=1.2)
B("Una vecina contaría, años después, que esa tarde escuchó un silencio extraño. Ni pájaros, ni perros, ni viento. Como si todo el barrio hubiera contenido la respiración.",
  S("alley_dusk", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.45)), fx=[FOG], grade="cold"))
B("Dicen que el soldado no entendió lo que había hecho. Que no sabía lo frágil que puede ser un niño.",
  S("soldier_ruin", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="cold"))
B("El miedo lo paralizó. Miró a un lado y al otro. El callejón estaba vacío. Nadie había visto nada.",
  S("alley_dusk", cam=((0.3, 0.5, 1.3), (0.7, 0.5, 1.3), "linear"), fx=[FOG], grade="cold"), music="dread")
B("Y entonces hizo lo que el barrio nunca le perdonaría. Esa noche, en la oscuridad, llevó al pequeño hasta el aguacate… y lo dejó ahí, como si el árbol pudiera guardar su secreto.",
  S("tree_moon", BRANCH, cam=((0.5, 0.5, 1.1), (0.5, 0.35, 1.35), "in"), fx=[FOG, PU(60, 0.06)], grade="night"),
  sfx=[X("owl", 3.0, -10), X("gust", 5.0, -10)])
B("Esa misma noche, la mamá del niño salió a buscarlo con una lámpara. Gritaba su nombre de puerta en puerta.",
  S("search_night", LANTERNS, cam=((0.4, 0.55, 1.1), (0.6, 0.5, 1.25), "linear"), fx=[FOG]),
  sfx=[X("whisper", 1.0, -12, dur=5)], amb=["night", {"name": "wind", "gain": -8}])
B("Los vecinos salieron con faroles. Recorrieron el barrio, la plaza, los campos. Y el soldado salió también: caminaba detrás de todos, en silencio, con los ojos clavados en el suelo.",
  S("search_night", LANTERNS, cam=((0.6, 0.5, 1.3), (0.4, 0.55, 1.45), "linear"), fx=[FOG], w=1.0),
  S("soldier_shadow", cam=((0.5, 0.45, 1.2), (0.5, 0.45, 1.4)), fx=[FOG], grade="cold", tr="xfade", tl=0.8, w=1.0),
  sfx=[X("footsteps", 0.0, -12, dur=8)])
B("Buscaron la noche entera. En las zanjas, en las huertas, a la orilla de los canales. Y a nadie se le ocurrió mirar hacia arriba.",
  S("search_night", LANTERNS, cam=((0.5, 0.55, 1.15), (0.5, 0.4, 1.35), "in"), fx=[FOG], grade="night"))
B("Al amanecer, alguien levantó la vista hacia el aguacate.",
  S("alley_dawn", cam=((0.5, 0.6, 1.1), (0.5, 0.4, 1.35), "in"), fx=[FOG], grade="cold"), pre=0.4)
B("Y el grito se escuchó hasta la capilla de Santa Catarina.",
  S("dawn_flash", tr="flash", tl=0.1, dur=1.4, fx=[SH(0, 0.5, 10)]),
  S("santa_catarina_dawn", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.2)), fx=[FOG], grade="cold"),
  sfx=[X("sting", 0.0, -2), X("boom", 0.0, -4), X("bell", 1.6, -8, freq=150)])
B("Lo que pasó después con el soldado, nadie lo cuenta igual. Unos dicen que lo descubrieron. Otros, que nunca pudieron probarle nada. Pero todos coinciden en lo que vino luego.",
  S("crowd_dawn", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=[FOG], grade="cold"), music="tension")

# ======================================================================== V
B("El soldado nunca volvió a ponerse el uniforme. Dejó de comer. Dejó de dormir. Por las noches, los vecinos lo escuchaban llorar.",
  S("room_dark", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FL], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO V|El nicho", "chapter", 0.6, 4.8)]), music="sad")
B("Y decía que, cuando apagaba la luz, alguien tocaba su puerta muy despacito. Tres veces. Como tocan los niños.",
  S("door_night", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.45), "in"), fx=[FOG, PU(60, 0.05)], grade="cold"),
  sfx=[X("knock", 4.2, -4, times=3)], music="dread")
B("Una mañana, mandó hacer un nicho en la esquina del callejón. Puso adentro una imagen de la Virgen… y le encendió una veladora.",
  S("niche_close", VELAC, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FL], grade="candle"), music="hope")
B("Todas las noches se arrodillaba frente a ella para pedir perdón. Durante años.",
  S("kneel_niche", VELAC, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3)), fx=[FL, FOGL], grade="candle"),
  S("veladoras", cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.35), "in"), fx=[FL], grade="candle", tr="xfade", tl=1.0),
  sfx=[X("whisper", 0.8, -16, dur=5)])
B("Pero cuentan que el perdón nunca llegó. Que la veladora se apagaba sola, aunque no hubiera viento.",
  S("niche_close", VELAC, cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.55)), fx=[FL], grade="candle", w=1.2),
  S("niche_dark", cam=((0.5, 0.45, 1.55), (0.5, 0.45, 1.65)), fx=[FOG], grade="cold", dur=2.0),
  sfx=[X("gust", 3.8, -6)], music="dread")
B("El soldado murió solo, años después, en esa misma casa junto al aguacate. Y el nicho se quedó ahí, en la esquina, como una disculpa que nadie aceptó.",
  S("house_soldier", cam=((0.5, 0.45, 1.3), (0.5, 0.5, 1.05), "out"), fx=[FOG], grade="cold", w=1.0),
  S("alley_night", VELA, cam=((0.75, 0.45, 1.4), (0.72, 0.45, 1.6)), fx=[FOG], grade="moon", tr="xfade", tl=1.0, w=1.0))
B("Desde entonces, los vecinos cuentan cosas. Que de noche, entre las ramas del aguacate, se oyen risas de niño. Pasitos que corren sobre el empedrado.",
  S("tree_shadow", BRANCH, KIDG, cam=((0.5, 0.45, 1.1), (0.5, 0.4, 1.35), "in"), fx=[FOG], grade="moon"),
  sfx=[X("footsteps", 2.5, -14, dur=3), X("whisper", 1.0, -14, dur=3)])
B("Y una vocecita que pregunta, una y otra vez, si alguien quiere jugar.",
  S("alley_deep", KIDG, cam=((0.5, 0.55, 1.3), (0.5, 0.55, 1.5), "in"), fx=[FOGL], grade="cold",
    text=[T("¿JUEGAS CONMIGO?|", "big", 1.0, 4.5)]))
B("Otros han visto una sombra pequeña cruzar el callejón y desaparecer en la pared. Y los que pasan muy tarde aseguran haber visto a un hombre de uniforme, parado junto al nicho… con la cabeza agachada.",
  S("alley_night", KIDG, cam=((0.4, 0.5, 1.2), (0.6, 0.5, 1.3), "linear"), fx=[FOGL], grade="moon", w=1.0),
  S("niche_soldier", VELAC, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.4), "in"), fx=[FOG], grade="cold", w=1.2),
  S("soldier_flash", tr="flash", tl=0.1, dur=1.3, fx=[SH(0, 0.5, 9)]),
  sfx=[X("sting", 0.0, -3, at_scene=2), X("boom", 0.0, -4, at_scene=2)])

# ======================================================================== HISTORIA
B("Cuentan también que, si dejas un dulce o un juguete junto al nicho, la risa se calma por un tiempo. Y que en esa esquina, de vez en cuando, aparecen canicas y trompos pequeños… que nadie sabe quién deja.",
  S("niche_toys", VELAC, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FL], grade="candle"), music="mystery")
B("Hay más versiones. Una habla de una niña que murió atropellada y que se aparece entre las dos y las tres de la mañana.",
  S("girl_ghost", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOG], grade="cold", tr="fade", tl=1.0,
    text=[T("LO QUE DICE LA HISTORIA|", "chapter", 0.6, 4.6)]), music="mystery")
B("Otra, más antigua, dice que en las noches más oscuras es el mismísimo diablo quien espera aquí a los distraídos. Y no falta quien jure haber visto al Charro Negro asomarse a medianoche.",
  S("devil_wall", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FOG, FL], grade="blood"))
B("Ahora, lo que sí sabemos. El callejón existe. Está en el barrio de Santa Catarina, en Coyoacán, a unos pasos de la avenida Francisco Sosa. Y el nicho con la Virgen sigue en su esquina.",
  S("alley_today", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="none",
    text=[T("Barrio de Santa Catarina|Coyoacán, Ciudad de México", "date", 0.5, 5.0)]))
B("El barrio conserva casas muy antiguas, de muros gruesos y portones de madera, y la capilla de Santa Catarina, a unos metros, es una de las más queridas de Coyoacán.",
  S("santa_catarina", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="warm"))
B("Pero no hay ningún registro que confirme la muerte del niño ni el nombre del soldado. La leyenda creció con los años, de boca en boca, entre vecinos, estudiantes y paseantes.",
  S("chronicle", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FL], grade="candle"))
B("Incluso hay quien dice que fueron los alumnos de las escuelas cercanas quienes la hicieron famosa, contándola para asustarse unos a otros.",
  S("students", cam=((0.4, 0.55, 1.1), (0.6, 0.55, 1.25), "linear"), fx=[FOGL], grade="night"))
B("Hoy es una calle tranquila donde vive gente. Si lo visitas, hazlo de día, en silencio y con respeto.",
  S("alley_today", cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.5), "in"), fx=["dust"], grade="none"), music="calm")

# ======================================================================== PAYOFF
B("Pero si algún día pasas por ahí después de la medianoche… y escuchas una risita a tus espaldas… no le tengas miedo al niño. El niño solo quiere jugar.",
  S("alley_deep", WALKER, KIDG, cam=((0.5, 0.6, 1.15), (0.5, 0.55, 1.4), "in"), fx=[FOGL], grade="moon", tr="fade", tl=1.0),
  music="dread", amb=["night", {"name": "wind", "gain": -8}])
B("Si sientes una mano pequeña que jala tu ropa, no voltees de inmediato. Primero mira hacia el nicho. Si la veladora está encendida, estás a salvo. Si está apagada…",
  S("niche_close", VELAC, cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.45), "in"), fx=[FL], grade="candle", w=1.2),
  S("niche_dark", cam=((0.5, 0.45, 1.45), (0.5, 0.45, 1.55)), fx=[FOG], grade="cold", dur=2.2),
  sfx=[X("gust", -0.5, -6, at_scene=1)])
B("Del que tienes que cuidarte es del hombre de uniforme. Porque dicen que todavía lo busca, para pedirle perdón…",
  S("alley_night", SOLG, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.55), "in"), fx=[FOGL, PU(80, 0.08)], grade="cold"),
  sfx=[X("heartbeat", 0.0, -9, dur=8, bpm=90)])
B("Y cuando no lo encuentra… se conforma con quien esté más cerca.",
  S("soldier_ghost_close", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.5), "in"), fx=[FOG], grade="cold", w=1.4),
  S("ghost_flash", tr="flash", tl=0.1, dur=1.4, fx=[SH(0, 0.5, 10)]),
  sfx=[X("riser", -3.0, -8, at_scene=1, dur=3), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -2, at_scene=1)],
  pause=0.8)
B("¿Juegas conmigo?",
  S("niche_dark", cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.45)), fx=[FOG], grade="cold"), pause=1.2, **KIDE)
B("Y tú, ¿pasarías de noche por el Callejón del Aguacate? ¿Crees que el soldado merece el perdón? Te leo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOG], tr="fade", tl=0.8), music="mystery")
B("En el próximo video nos vamos a Chihuahua, a una tienda de vestidos de novia donde, desde hace casi cien años, una maniquí mira a los que pasan. Dicen que no es una maniquí. Su nombre es La Pascualita.",
  S("pascualita", cam=((0.5, 0.5, 1.05), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="night",
    text=[T("PRÓXIMO VIDEO|La Pascualita", "big", 2.0, 7.0)]), sfx=[X("whisper", 3.0, -12, dur=4)])
B("Hasta la próxima leyenda. Y si alguna noche alguien te pide que juegues con él… no le contestes.",
  S("alley_night", KIDG, VELA, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.45), "in"), fx=[FOGL], grade="moon", out=2.0), pause=1.0, music="dread")
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

story = {"title": "El Callejón del Aguacate", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "E", "seed": 61, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# El Callejón del Aguacate — guion\n",
                  "Narración en español (narrador: em_alex; el niño: ef_dora; el soldado: em_santa).\n"]
WHO = {"ef_dora": "EL NIÑO: ", "em_santa": "EL SOLDADO: "}
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
