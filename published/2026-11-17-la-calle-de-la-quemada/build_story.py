#!/usr/bin/env python3
"""Builds story.json and script.md for 'La Calle de la Quemada'. Edit BEATS here, then run."""
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
CANDLE = L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 2.0}])
LAMP = L("l_lamp_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.4}])
COALS = L("l_coals_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.25, "speed": 1.1}, {"type": "pulse", "amp": 0.03, "period": 3, "pivot": [0.5, 0.75]}])
FOGLAY = L("l_fog", blend="screen", opacity=[0, 0.8], anim=[{"type": "drift", "dx": -0.06, "ease": "linear"}])
RUNNER = L("l_martin_run", depth=1.1, anim=[{"type": "drift", "dx": 0.0, "dy": -0.02, "ease": "linear"}, {"type": "scale", "from": 0.8, "to": 1.15, "pivot": [0.5, 0.95], "ease": "in"}, {"type": "float", "amp": 0.004, "period": 0.5}])
WATCHER = L("l_watcher", depth=1.05, opacity=[0, 1], fade_in=1.5)
GHOST = L("l_ghost_veil", blend="screen", opacity=[0, 0.85], fade_in=2.0, anim=[{"type": "float", "amp": 0.005, "period": 5}, {"type": "flicker", "amp": 0.15, "speed": 0.7}])
DUEL = L("l_duel", depth=1.08, anim=[{"type": "float", "amp": 0.003, "period": 1.2}])
SERENADE = L("l_serenade", depth=1.06)
COUPLE = L("l_couple_walk", depth=1.08, anim=[{"type": "drift", "dx": 0.05, "ease": "linear"}])

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)


BEA = dict(voice="ef_dora", speed=0.82)
MAR = dict(voice="em_santa", speed=0.82)
GHO = dict(voice="ef_dora", speed=0.72, fx="eco")

# ======================================================================== COLD OPEN
B("Ciudad de México. Una noche sin luna, hace más de cuatrocientos cincuenta años.",
  S("street_night", LAMP, FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=["dust"], tr="fade", tl=1.2),
  pre=0.5, music="dread", amb=["night", {"name": "wind", "gain": -8}])
B("Un hombre corre por el empedrado, con la capa abierta y el corazón en la garganta.",
  S("street_run", RUNNER, LAMP, cam=((0.5, 0.55, 1.15), (0.5, 0.6, 1.35), "in"), fx=[FOGL]),
  sfx=[X("footsteps", 0.0, -6, dur=6), X("heartbeat", 1.0, -10, dur=6, bpm=100)])
B("Sube una escalera. Empuja una puerta. Y ahí, en la penumbra, junto a la ventana… lo espera una mujer cubierta con un velo blanco.",
  S("stairs", CANDLE, cam=((0.45, 0.6, 1.1), (0.55, 0.4, 1.35), "in"), fx=[FL], grade="candle", w=0.8),
  S("veiled_chair", cam=((0.5, 0.5, 1.05), (0.55, 0.45, 1.35), "in"), fx=["dust", FL], tr="xfade", tl=0.6, w=1.2),
  sfx=[X("door", 2.2, -6)])
B("Él estira la mano. Ella no se mueve. Y cuando por fin levanta el velo…",
  S("veil_hand", cam=((0.5, 0.45, 1.2), (0.5, 0.4, 1.55), "in"), fx=[PU(80, 0.08)], w=1.3),
  S("veil_flash", tr="flash", tl=0.12, dur=1.6, cam=((0.5, 0.42, 1.4), (0.5, 0.42, 1.6)), fx=[SH(0, 0.5, 8)]),
  pause=0.6, sfx=[X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("",
  S("title_bg", GHOST, cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("LA CALLE DE LA QUEMADA|la mujer detrás del velo", "title", 0.6, 6.4)]),
  pause=5.2, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Lo que él vio debajo de ese velo le cambió el nombre a una calle para siempre. Y lo que dijo después… todavía divide a quienes cuentan esta historia.",
  S("veiled_eyes", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="cold"), music="tension")
B("Esta es la leyenda de la Calle de la Quemada. Quédate hasta el final: vas a saber qué había detrás del velo… y por qué hay quien jura que ella todavía camina por ahí.",
  S("street_night", GHOST, cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.1)), fx=[FOGL], grade="moon"))

# ======================================================================== I
B("Corría el año de mil quinientos cincuenta. La Ciudad de México apenas tenía treinta años de haber sido levantada sobre las ruinas de Tenochtitlan.",
  S("plaza_1550", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], grade="warm", tr="fade", tl=1.0,
    text=[T("CAPÍTULO I|La más hermosa", "chapter", 0.6, 5.0)]),
  S("plaza_1550", cam=((0.6, 0.45, 1.25), (0.7, 0.45, 1.45)), fx=["dust"], grade="warm", tr="xfade", tl=0.8,
    text=[T("Ciudad de México, 1550|capital de la Nueva España", "date", 0.4, 4.6)]),
  music="calm", amb=["city"])
B("Era una ciudad de canales y calzadas, de iglesias a medio construir, donde de noche no había más luz que la de algunos faroles y la de la luna. Al anochecer las calles se vaciaban. Y cualquiera que caminara solo… sabía que estaba arriesgando la vida.",
  S("street_night", LAMP, cam=((0.3, 0.5, 1.1), (0.6, 0.5, 1.2), "linear"), fx=[FOG], grade="night"), amb=["night", {"name": "wind", "gain": -10}])
B("Ese mismo año llegó desde España un nuevo virrey, don Luis de Velasco. Y con él, cuentan, llegaron también muchas familias que buscaban fortuna en la Nueva España.",
  S("palacio", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="warm"))
B("Entre ellas venía don Gonzalo Espinosa de Guevara, un hombre rico y severo… con su única hija.",
  S("gonzalo_portrait", CANDLE, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3)), fx=[FL], grade="candle"))
B("Don Gonzalo había hecho fortuna y quería una sola cosa para su hija: un buen matrimonio, con un hombre de nombre y de dinero.",
  S("gonzalo_portrait", CANDLE, cam=((0.5, 0.4, 1.35), (0.5, 0.38, 1.55), "in"), fx=[FL], grade="candle"))
B("Se llamaba Beatriz. Tenía veinte años, el cabello negro como la noche y unos ojos que, decían, nadie podía mirar sin quedarse callado.",
  S("beatriz_portrait", cam=((0.5, 0.42, 1.1), (0.5, 0.38, 1.4), "in"), fx=["dust"], grade="moon"),
  music="sad")
B("Pero no era solo su belleza. Beatriz visitaba hospitales, llevaba comida a los pobres y daba limosna en la puerta de los templos. En toda la ciudad se hablaba de ella como de un ángel.",
  S("charity", cam=((0.45, 0.55, 1.05), (0.55, 0.5, 1.25)), fx=["dust"], grade="warm"),
  S("beatriz_soft", cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.35)), fx=["dust"], grade="warm", tr="xfade", tl=0.8))
B("Su padre compró una casona de cantera, con balcones de hierro, a unas cuadras de la Plaza Mayor. Y desde la primera semana… empezaron a llegar los pretendientes.",
  S("casona", LAMP, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOG], grade="night"))
B("Jóvenes de buena familia se paraban bajo su balcón con guitarras. Le mandaban flores, versos, regalos. Uno tras otro.",
  S("balcony_night", SERENADE, cam=((0.5, 0.55, 1.1), (0.5, 0.45, 1.3)), fx=[FOG], grade="night"),
  sfx=[X("whisper", 1.0, -18, dur=3)])
B("Y ella, con una sonrisa amable, los rechazaba a todos.",
  S("beatriz_balcony", CANDLE, cam=((0.5, 0.4, 1.25), (0.5, 0.38, 1.45), "in"), fx=[FL], grade="candle"))
B("Pero había alguien que la miraba desde lejos. Desde la sombra de un portal, noche tras noche, sin acercarse nunca.",
  S("street_portal", WATCHER, cam=((0.55, 0.5, 1.1), (0.65, 0.5, 1.4), "in"), fx=[FOGL], grade="night"),
  music="mystery", amb=["night", {"name": "wind", "gain": -8}], sfx=[X("owl", 2.0, -14)])
B("Y no era un pretendiente cualquiera.",
  S("watcher_close", cam=((0.5, 0.45, 1.2), (0.5, 0.4, 1.5), "in"), fx=[FOG], grade="night"),
  pause=0.9, sfx=[X("sting", 1.2, -6)])

# ======================================================================== II
B("Una noche, el virrey dio un baile en su palacio. Velas por cientos, música de vihuelas, vestidos de seda llegados de Sevilla.",
  S("ballroom", CANDLE, cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust", FL], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO II|El marqués", "chapter", 0.6, 5.0)]),
  music="calm", amb=["room"])
B("Ahí, entre la gente, Beatriz lo vio por primera vez. Alto, de barba fina, con una espada al cinto y un sombrero de plumas negras.",
  S("ballroom_couple", CANDLE, cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.4), "in"), fx=["dust", FL], grade="candle"),
  S("martin_portrait", CANDLE, cam=((0.5, 0.42, 1.15), (0.5, 0.38, 1.4), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8))
B("Se llamaba don Martín de Scópoli, marqués de Piamonte y Franteschelo. Un noble italiano, rico, elegante… y acostumbrado a obtener todo lo que quería.",
  S("martin_portrait", CANDLE, cam=((0.5, 0.4, 1.4), (0.5, 0.38, 1.6), "in"), fx=[FL], grade="candle",
    text=[T("Don Martín de Scópoli|marqués de Piamonte", "big", 0.8, 5.0)]))
B("Bailaron una sola pieza. Al día siguiente llegó la primera carta. Y después otra. Y otra más.",
  S("letters", CANDLE, cam=((0.45, 0.55, 1.1), (0.55, 0.5, 1.35), "in"), fx=["dust", FL], grade="candle"),
  music="hope")
B("Cuentan que esas cartas hablaban de su belleza. De sus ojos, de su piel, de su cabello. Siempre de su belleza. Y Beatriz, enamorada, no se dio cuenta de que en ninguna carta… Martín hablaba de su alma.",
  S("letters", CANDLE, cam=((0.5, 0.6, 1.4), (0.5, 0.62, 1.65), "in"), fx=["dust", FL], grade="candle"))
B("Por primera vez, Beatriz no rechazó a un pretendiente. Por primera vez… se enamoró.",
  S("beatriz_soft", cam=((0.5, 0.4, 1.15), (0.5, 0.38, 1.4), "in"), fx=["dust"], grade="warm"))
B("Pero muy pronto descubrió algo que la llenó de miedo. Martín no soportaba que nadie más la mirara.",
  S("martin_jealous", cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.5), "in"), fx=[PU(70, 0.08)], grade="night"),
  music="tension")
B("Si un hombre la saludaba en misa, Martín lo seguía con los ojos hasta la puerta. Si alguien le sonreía en la calle, él apretaba la empuñadura de su espada.",
  S("church_mass", CANDLE, cam=((0.5, 0.5, 1.1), (0.45, 0.5, 1.3)), fx=["dust", FL], grade="candle"),
  S("sword_hilt", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.5), "in"), fx=[PU(80, 0.1)], grade="night", tr="xfade", tl=0.6))
B("Y una noche, frente a la casona, le dijo algo que ella nunca pudo olvidar.",
  S("casona", LAMP, cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.45), "in"), fx=[FOG], grade="night"))
B("Ningún hombre volverá a pararse bajo tu balcón, Beatriz. Te lo juro por mi nombre.",
  S("martin_red", cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.6), "in"), fx=[PU(60, 0.12)], grade="blood",
    text=[T("Te lo juro por mi nombre|don Martín", "quote", 1.0, 5.5)]),
  pause=0.9, sfx=[X("sting", 3.8, -6)], **MAR)
B("Si te gustan estas historias de la vieja Ciudad de México, suscríbete y activa la campanita. Cada día te traigo una leyenda nueva.",
  S("title_bg", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.2)), fx=[FOG], grade="night"), music="mystery")

# ======================================================================== III
B("La primera vez fue un joven que llevaba semanas cantándole serenatas. Una noche, a media canción, una figura salió de la oscuridad.",
  S("balcony_night", SERENADE, WATCHER, cam=((0.5, 0.55, 1.2), (0.5, 0.6, 1.45), "in"), fx=[FOGL], grade="night", tr="fade", tl=1.0,
    text=[T("CAPÍTULO III|Las noches de los duelos", "chapter", 0.6, 5.0)]),
  music="dread", amb=["night", {"name": "wind", "gain": -6}])
B("Una capa negra. Un sombrero de plumas. Y el brillo de una espada a la luz del farol.",
  S("duel_street", DUEL, LAMP, cam=((0.5, 0.55, 1.15), (0.5, 0.5, 1.4), "in"), fx=[FOGL], grade="night"),
  sfx=[X("whoosh", 2.5, -8)])
B("Se oyó el choque del acero. Un grito. Y después… nada.",
  S("swords", tr="flash", tl=0.12, cam=((0.5, 0.5, 1.25), (0.5, 0.5, 1.5)), fx=[SH(0.0, 0.4, 7), "embers"], grade="night", w=0.8),
  S("street_night", cam=((0.5, 0.55, 1.2), (0.5, 0.55, 1.25)), fx=[FOGL], grade="night", tr="xfade", tl=0.3, w=1.2),
  pause=1.0, sfx=[X("sting", 0.0, -3), X("boom", 0.05, -5), X("whoosh", 1.8, -10)])
B("A la mañana siguiente, los vecinos encontraron en el empedrado una guitarra rota… y un sombrero manchado de rojo.",
  S("fallen", cam=((0.5, 0.55, 1.15), (0.5, 0.6, 1.45), "in"), fx=["dust"], grade="cold"),
  music="sad", amb=["city"])
B("Al joven lo enterraron esa misma semana. Nadie supo decir quién lo había retado.",
  S("church_ext", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25)), fx=[FOG], grade="cold"),
  sfx=[X("bell", 0.5, -8, freq=150), X("bell", 4.5, -10, freq=150)])
B("Pocas semanas después, pasó otra vez. Un caballero que se había quitado el sombrero al ver pasar a Beatriz. Lo encontraron al amanecer, frente a la Plaza Mayor.",
  S("duel_street", DUEL, LAMP, cam=((0.4, 0.5, 1.2), (0.6, 0.5, 1.3), "linear"), fx=[FOGL], grade="night"),
  S("fallen_lantern", cam=((0.5, 0.55, 1.15), (0.5, 0.55, 1.4), "in"), fx=["dust"], grade="cold", tr="xfade", tl=0.6),
  music="dread", amb=["night"])
B("Y luego otro. Y otro más.",
  S("swords", tr="flash", tl=0.1, cam=((0.45, 0.5, 1.4), (0.55, 0.5, 1.55)), fx=[SH(0.0, 0.4, 8)], grade="blood"),
  pause=0.8, sfx=[X("sting", 0.0, -4), X("boom", 0.0, -5)])
B("Cuentan que fueron cinco, quizá más. Hombres que solo habían cometido un error: mirar a Beatriz demasiado tiempo.",
  S("church_ext", cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.4), "in"), fx=[FOG], grade="cold"), sfx=[X("bell", 0.5, -10, freq=140)])
B("La ciudad empezó a murmurar. Que había un duelista que salía de noche. Que siempre peleaba cerca de la casa de los Espinosa. Que todos los muertos… tenían algo que ver con Beatriz.",
  S("street_whispers", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FOG], grade="night"),
  sfx=[X("whisper", 0.5, -10, dur=6)])
B("La justicia buscaba al culpable. Pero nadie se atrevía a señalar a un marqués.",
  S("palacio_night", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.3)), fx=[FOG], grade="night"))
B("Beatriz escuchaba las campanas de los entierros desde su ventana. Y cada vez que sonaban, sabía, en el fondo de su alma, quién había empuñado esa espada.",
  S("beatriz_window", cam=((0.5, 0.5, 1.1), (0.55, 0.45, 1.35), "in"), fx=["dust"], grade="moon"),
  S("beatriz_sad", cam=((0.5, 0.42, 1.25), (0.5, 0.4, 1.45), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.8),
  music="sad", sfx=[X("bell", 0.4, -12, freq=140)])
B("Una tarde, lo enfrentó.",
  S("confront", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3), "in"), fx=[FL], grade="candle"), music="tension")
B("Martín, por Dios, ya basta. Están muriendo por mí. Esos hombres tenían madre, tenían nombre.",
  S("beatriz_fear", CANDLE, cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.45), "in"), fx=[FL], grade="candle"), **BEA)
B("Él la miró sin parpadear. Y le contestó con una calma que le heló la sangre.",
  S("martin_portrait", CANDLE, cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.55), "in"), fx=[FL], grade="candle"))
B("Mientras seas así de hermosa, Beatriz… siempre habrá alguien a quien tenga que matar.",
  S("martin_red", cam=((0.5, 0.4, 1.45), (0.5, 0.38, 1.75), "in"), fx=[PU(60, 0.14)], grade="blood",
    text=[T("Siempre habrá alguien|a quien tenga que matar", "big", 1.2, 6.0)]),
  pause=1.2, sfx=[X("sting", 0.2, -4), X("heartbeat", 0.5, -8, dur=6, bpm=70)], **MAR)

# ======================================================================== IV
B("Esa noche, Beatriz no durmió. Se sentó frente al espejo, con una vela encendida, y se miró como nunca antes se había mirado.",
  S("mirror", CANDLE, cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FL, "dust"], grade="candle", tr="fade", tl=1.0,
    text=[T("CAPÍTULO IV|El brasero", "chapter", 0.6, 5.0)]),
  music="dread", amb=["room", {"name": "clock", "gain": -8}])
B("Esa cara que todos admiraban… era la misma que estaba llenando de cruces el cementerio.",
  S("mirror_close", CANDLE, cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.6), "in"), fx=[FL], grade="candle"),
  sfx=[X("whisper", 1.0, -12, dur=4)])
B("Pensó en entrar a un convento. Pensó en huir. Pero sabía que Martín la buscaría donde fuera. Y que mientras existiera esa cara… siempre habría alguien más.",
  S("beatriz_window", cam=((0.55, 0.45, 1.3), (0.6, 0.42, 1.5), "in"), fx=["dust"], grade="moon"))
B("Mi cara… mi cara es la que los mata.",
  S("beatriz_sad", cam=((0.5, 0.4, 1.4), (0.5, 0.38, 1.65), "in"), fx=["dust"], grade="cold"), pause=1.0, **BEA)
B("Pasaron los días. Don Gonzalo salió de viaje. Y una noche, Beatriz mandó a dormir a todos los criados. Se quedó sola en la casona.",
  S("casona", cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.35)), fx=[FOG], grade="night"),
  S("corridor", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.4), "in"), fx=[FL, "dust"], grade="candle", tr="xfade", tl=0.6),
  amb=["room", {"name": "wind", "gain": -10}])
B("En su cuarto pidió que le dejaran un brasero de carbón, como los que se usaban en las noches frías. Lo encendió. Y se quedó mirando cómo las brasas se ponían rojas.",
  S("brasero_room", COALS, cam=((0.5, 0.55, 1.05), (0.5, 0.6, 1.3), "in"), fx=["embers", FL], grade="candle"),
  S("coals", COALS, cam=((0.5, 0.55, 1.2), (0.5, 0.6, 1.5), "in"), fx=["embers"], grade="candle", tr="xfade", tl=0.8),
  sfx=[X("fire", 0.0, -8, dur=14)])
B("Se arrodilló frente a una imagen de Santa Lucía, la santa de los ojos. Rezó en voz baja. Pidió perdón… y pidió valor.",
  S("altar", CANDLE, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.4), "in"), fx=[FL], grade="candle"),
  sfx=[X("whisper", 1.5, -14, dur=5)])
B("Lo que pasó después, nadie lo vio. Cuentan que decidió que su belleza tenía que desaparecer… para que nadie más muriera por ella.",
  S("shadow_wall", COALS, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=["embers", PU(60, 0.1)], grade="candle"))
B("Y que se acercó al fuego.",
  S("coals", COALS, cam=((0.5, 0.55, 1.5), (0.5, 0.58, 1.8), "in"), fx=["embers"], grade="blood", out=0.6),
  pause=0.4, sfx=[X("riser", -2.5, -8, dur=3)])
B("",
  S("black", tr="flash", tl=0.1, dur=2.4, fx=[SH(0, 0.5, 10)]),
  pause=2.0, music="silence", sfx=[X("boom", 0.0, -2), X("sting", 0.0, -3)])
B("Esa noche, un grito despertó a toda la calle.",
  S("street_night", cam=((0.5, 0.5, 1.2), (0.5, 0.48, 1.35)), fx=[FOGL], grade="cold", tr="fade", tl=0.6),
  music="dread", amb=["night", {"name": "wind", "gain": -6}])
B("Los criados subieron corriendo. Encontraron el brasero volcado, el cuarto lleno de humo… y a Beatriz en el suelo, con las manos sobre la cara, rezando todavía.",
  S("door_burst", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.4), "in"), fx=["dust", "embers"], grade="candle"),
  sfx=[X("door", 0.0, -4), X("footsteps", 0.0, -8, dur=3)])
B("Llamaron a los médicos. Pasaron días de fiebre. Beatriz sobrevivió. Pero su rostro… ya no era el mismo.",
  S("sickbed", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FL], grade="candle"),
  music="sad")
B("Cuando pudo levantarse, pidió un velo blanco. Se lo puso sobre la cabeza, se sentó junto a la ventana… y pidió una sola cosa: que llamaran a Martín.",
  S("veiled_chair", cam=((0.5, 0.5, 1.1), (0.55, 0.45, 1.4), "in"), fx=["dust"], grade="moon"))

# ======================================================================== V
B("Y aquí regresamos al principio. Al hombre que corre por el empedrado, con la capa abierta.",
  S("street_run", RUNNER, LAMP, cam=((0.5, 0.55, 1.1), (0.5, 0.6, 1.35), "in"), fx=[FOGL], grade="night", tr="fade", tl=1.0,
    text=[T("CAPÍTULO V|Detrás del velo", "chapter", 0.6, 5.0)]),
  music="tension", sfx=[X("footsteps", 0.0, -6, dur=6), X("heartbeat", 1.0, -10, dur=6, bpm=110)])
B("Martín había escuchado lo que se decía en toda la ciudad. Que la hermosa Beatriz… se había quemado la cara.",
  S("martin_portrait", LAMP, cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.5), "in"), fx=[FOG], grade="night"))
B("Subió la escalera. Empujó la puerta. Y la encontró ahí, junto a la ventana, cubierta con el velo blanco.",
  S("stairs", CANDLE, cam=((0.5, 0.55, 1.15), (0.55, 0.4, 1.4), "in"), fx=[FL], grade="candle", w=0.8),
  S("veiled_chair", cam=((0.55, 0.45, 1.2), (0.55, 0.42, 1.45), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.6, w=1.2),
  sfx=[X("door", 2.0, -6)])
B("Ella habló primero. Con una voz tranquila, casi dulce.",
  S("veil_hand", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35)), fx=["dust"], grade="moon"))
B("Ya no hay nada que mirar, Martín. Ya nadie tiene que morir por mí.",
  S("veiled_eyes", cam=((0.5, 0.45, 1.25), (0.5, 0.42, 1.5), "in"), fx=["dust"], grade="moon",
    text=[T("Ya nadie tiene que morir por mí|Beatriz", "quote", 1.0, 5.5)]), pause=1.0, **BEA)
B("Y entonces se quitó el velo.",
  S("veil_lift", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.5), "in"), fx=[PU(70, 0.1)], grade="moon"),
  pause=1.0, sfx=[X("riser", -1.0, -10, dur=2.5), X("sting", 2.0, -6)])
B("Lo que Martín vio fue un rostro marcado por el fuego. La piel que todos habían admirado… ya no estaba. Pero los ojos… los ojos eran los mismos.",
  S("veiled_eyes", cam=((0.5, 0.42, 1.5), (0.5, 0.4, 1.8), "in"), fx=["dust"], grade="cold"),
  music="sad")
B("Y el marqués, el hombre que había llenado de sangre las calles de la ciudad… cayó de rodillas.",
  S("kneel", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="moon"))
B("Lloró como un niño. Le tomó las manos. Y le dijo las palabras que todavía se repiten en el centro de la ciudad.",
  S("hands_hold", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=["dust"], grade="moon"))
B("Beatriz… yo no te amaba por tu cara. Te amo por tu alma.",
  S("kneel", cam=((0.5, 0.5, 1.35), (0.5, 0.45, 1.6), "in"), fx=["dust"], grade="moon",
    text=[T("Te amo por tu alma|don Martín", "quote", 1.0, 5.5)]),
  pause=1.0, music="hope", **MAR)
B("Unos dicen que esas palabras fueron la prueba de un amor verdadero. Otros dicen que llegaron demasiado tarde.",
  S("hands_hold", cam=((0.5, 0.5, 1.4), (0.5, 0.5, 1.6), "in"), fx=["dust"], grade="moon"))
B("Cuentan que se casaron poco después, en una boda sencilla, sin músicos y sin baile. Y que desde ese día, Beatriz nunca volvió a salir a la calle sin un velo negro sobre el rostro.",
  S("wedding", CANDLE, cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust", FL], grade="candle"),
  S("veil_black", cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.45), "in"), fx=["dust"], grade="night", tr="xfade", tl=0.8))
B("Los vecinos la veían pasar del brazo del marqués, despacio, por la misma calle donde habían caído tantos hombres. Y empezaron a llamarla de una sola forma.",
  S("street_day", COUPLE, cam=((0.4, 0.55, 1.1), (0.55, 0.5, 1.25), "linear"), fx=["dust"], grade="warm"))
B("La Quemada. Y la calle donde vivía… se convirtió en la Calle de la Quemada.",
  S("street_sign", LAMP, cam=((0.5, 0.5, 1.15), (0.5, 0.48, 1.45), "in"), fx=[FOG], grade="night",
    text=[T("LA QUEMADA|así la llamó la ciudad", "big", 0.8, 5.5)]),
  sfx=[X("boom", 0.6, -6)])
B("Pero ahora piensa en esto. Martín nunca pagó por los hombres que mató. Nadie lo juzgó. Nadie lo castigó. La única que pagó… fue ella.",
  S("martin_jealous", cam=((0.5, 0.42, 1.3), (0.5, 0.4, 1.5), "in"), fx=[PU(60, 0.08)], grade="night"),
  S("veil_black", cam=((0.5, 0.42, 1.35), (0.5, 0.4, 1.55), "in"), fx=["dust"], grade="cold", tr="xfade", tl=0.8),
  music="dread")
B("Por eso hoy, muchos ya no la cuentan como una historia de amor. La cuentan como una advertencia: sobre los celos, sobre la violencia que se disfraza de pasión… y sobre todo lo que una mujer tuvo que cargar por culpa de otro.",
  S("street_night", GHOST, cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3)), fx=[FOGL], grade="moon"))

# ======================================================================== HISTORY
B("Lo que sí es historia es esto. Don Luis de Velasco existió: gobernó la Nueva España de mil quinientos cincuenta a mil quinientos sesenta y cuatro, y murió en la Ciudad de México siendo virrey.",
  S("chronicle", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=[FL, "dust"], grade="candle", tr="fade", tl=1.0,
    text=[T("LO QUE DICE LA HISTORIA|", "chapter", 0.6, 4.5), T("1550 – 1564|el virrey Luis de Velasco", "date", 5.0, 9.5)]),
  music="calm", amb=["room"])
B("De Beatriz y del marqués, en cambio, no hay documentos que prueben que vivieron. Su historia pasó de boca en boca durante siglos, hasta que los cronistas de la ciudad la escribieron, a finales del siglo diecinueve y principios del veinte.",
  S("chronicle_page", CANDLE, cam=((0.45, 0.5, 1.15), (0.55, 0.5, 1.35)), fx=[FL, "dust"], grade="candle"))
B("En mil novecientos diez, un escritor estadounidense la incluyó en un libro de leyendas de la Ciudad de México, y así la conocieron lectores de todo el mundo. Algunas versiones dicen que la boda fue en el templo de la Profesa… aunque ese templo se levantó mucho después.",
  S("chronicle", CANDLE, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.5), "in"), fx=[FL, "dust"], grade="candle"))
B("La calle sí existe. Durante mucho tiempo se llamó así, la Calle de la Quemada. Hoy forma parte de la calle de Jesús María, en el Centro Histórico, a unas cuadras al oriente del Zócalo.",
  S("street_today", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="none",
    text=[T("Calle de Jesús María|Centro Histórico, Ciudad de México", "date", 1.0, 6.0)]),
  amb=["city"])
B("Y hay vecinos que dicen que, en noches sin luna, una mujer con velo negro camina despacio por esa calle. Que no hace ruido al pisar. Y que si alguien la sigue… ella se detiene.",
  S("street_night", GHOST, FOGLAY, cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.4), "in"), fx=[FOGL], grade="moon"),
  music="dread", amb=["night", {"name": "wind", "gain": -6}], sfx=[X("whisper", 2.0, -10, dur=5)])
B("Y empieza a levantar el velo.",
  S("ghost_close", cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.6), "in"), fx=[FOG, PU(70, 0.1)], grade="cold", w=1.0),
  S("ghost_flash", tr="flash", tl=0.1, dur=1.4, cam=((0.5, 0.42, 1.5), (0.5, 0.42, 1.7)), fx=[SH(0, 0.5, 8)], grade="cold"),
  pause=0.8, sfx=[X("riser", -2.0, -8, at_scene=1, dur=2.0), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("No mires lo que hay debajo… mira sus ojos.",
  S("veiled_eyes", cam=((0.5, 0.42, 1.6), (0.5, 0.4, 1.85), "in"), fx=["dust"], grade="cold"), pause=1.0, **GHO)
B("Y tú, ¿qué crees? ¿Fue una historia de amor… o una historia de miedo? ¿Martín merecía el perdón de Beatriz? Te leo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOG], tr="fade", tl=0.8), music="mystery")
B("En el próximo video nos vamos a Coyoacán, a un callejón angosto donde un viejo árbol de aguacate guarda un secreto… y donde, dicen, pasada la medianoche, alguien te pregunta la hora. Es la leyenda del Callejón del Aguacate.",
  S("aguacate", LAMP, cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.05)), fx=[FOG], grade="night",
    text=[T("PRÓXIMO VIDEO|El Callejón del Aguacate", "big", 2.0, 7.0)]), sfx=[X("whisper", 3.0, -12, dur=4)])
B("Hasta la próxima leyenda. Y si una noche alguien con velo te pide que te acerques… no le pidas que se lo quite.",
  S("street_night", GHOST, cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.45), "in"), fx=[FOGL], grade="moon", out=2.0), pause=1.0, music="dread")

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

story = {"title": "La Calle de la Quemada", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "D", "seed": 52, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# La Calle de la Quemada — guion\n",
                  "Narración en español (narrador: em_alex; Beatriz: ef_dora; don Martín: em_santa).\n"]
WHO = {"ef_dora": "BEATRIZ: ", "em_santa": "DON MARTÍN: "}
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
