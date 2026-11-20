#!/usr/bin/env python3
"""Builds story.json and script.md for 'El Sombrerón' (Chiapas). Edit BEATS here, then run.
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
LAMP = L("l_lamp_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.12, "speed": 1.4}])
CANDLE = L("l_candle_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.18, "speed": 2.0}])
FOGLAY = L("l_fog", blend="screen", opacity=[0, 0.8], anim=[{"type": "drift", "dx": -0.06, "ease": "linear"}])
WING = L("l_window_glow", blend="screen", anim=[{"type": "flicker", "amp": 0.1, "speed": 0.9}])
SOMB = L("l_sombreron", depth=1.1, anim=[{"type": "sway", "deg": 1.2, "period": 2.6, "pivot": [0.5, 0.95]}])
SOMBG = L("l_sombreron", depth=1.1, opacity=[0, 1.0], fade_in=1.6, anim=[{"type": "sway", "deg": 1.2, "period": 2.6, "pivot": [0.5, 0.95]}])
MULES = L("l_mules", depth=1.2, anim=[{"type": "drift", "dx": 0.05, "ease": "linear"}, {"type": "float", "amp": 0.002, "period": 1.1}])
NOTES = L("l_notes", blend="screen", opacity=[0, 0.8], fade_in=1.2, anim=[{"type": "drift", "dx": 0.03, "dy": -0.05, "ease": "linear"}])
RIDER = L("l_rider", depth=1.15, anim=[{"type": "drift", "dx": 0.12, "ease": "linear"}, {"type": "float", "amp": 0.003, "period": 0.7}])

N = 0
BEATS = []
def B(text, *scenes, **kw):
    global N; N += 1
    b = {"id": f"b{N:03d}", "text": text}; b.update(kw); b["scenes"] = list(scenes)
    BEATS.append(b)


MOM = dict(voice="ef_dora", speed=0.82)
INES = dict(voice="ef_dora", speed=0.95)
ABU = dict(voice="ef_dora", speed=0.76)
SOM = dict(voice="em_santa", speed=0.8, fx="eco")

# ======================================================================== COLD OPEN
B("San Cristóbal de las Casas, en los Altos de Chiapas. Las tres de la mañana.",
  S("valley_night", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.25), "in"), fx=["dust"], tr="fade", tl=1.2),
  pre=0.6, music="dread", amb=["night", {"name": "wind", "gain": -9}], sfx=[X("bell", 0.4, -14, freq=140)])
B("Imagina que te despierta una guitarra. Suena bajito, debajo de la ventana. Una canción dulce, lenta, que nunca habías oído.",
  S("house_window", WING, NOTES, cam=((0.5, 0.5, 1.1), (0.5, 0.48, 1.3), "in"), fx=[FOGL]),
  S("guitar_close", NOTES, cam=((0.5, 0.5, 1.15), (0.55, 0.5, 1.4), "in"), fx=["dust"], tr="xfade", tl=0.8, grade="moon"),
  music="tension")
B("Te levantas. Caminas hasta el cuarto de tu hija. La puerta está entreabierta. Ella duerme… y sonríe.",
  S("room_ines", CANDLE, cam=((0.4, 0.5, 1.1), (0.55, 0.5, 1.35), "in"), fx=[FL], grade="candle"),
  S("ines_sleep", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.8),
  sfx=[X("footsteps", 0.0, -12, dur=4), X("door", 2.5, -12)])
B("Su cabello, que anoche dejó suelto, ahora está trenzado. Decenas de trencitas finas, perfectas. Ninguna mano humana podría hacerlas en una noche.",
  S("braids_pillow", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.4), "in"), fx=["dust", PU(70, 0.05)], grade="moon",
    text=[T("TRENZADO|", "big", 3.0, 6.5)]),
  sfx=[X("heartbeat", 0.5, -10, dur=8, bpm=75)])
B("Y en el suelo, junto a la ventana, hay huellas de lodo. Huellas de unas botas pequeñitas… con espuelas.",
  S("bootprints", cam=((0.5, 0.55, 1.1), (0.5, 0.6, 1.45), "in"), fx=["dust"], grade="cold"),
  S("sombreron_eyes", tr="flash", tl=0.12, dur=1.4, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.5)), fx=[SH(0, 0.5, 9)]),
  pause=0.6, sfx=[X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("EL SOMBRERÓN|el que trenza el cabello", "title", 0.6, 6.4)]),
  pause=5.2, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("En Chiapas dicen que, cuando una muchacha amanece así, ya la escogió alguien. Alguien que no se va a ir solo.",
  S("ines_braids", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.05), "out"), fx=[FOG], grade="moon"))
B("Una madre, hace mucho tiempo, hizo algo para salvar a su hija. Algo que en los Altos todavía se recuerda. Y lo que encontró después… lo vas a saber al final.",
  S("mother_fear", CANDLE, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle"))
B("Esta es la leyenda del Sombrerón.",
  S("sombreron_close", cam=((0.5, 0.45, 1.3), (0.5, 0.5, 1.1)), fx=[FOG], grade="night"))

# ======================================================================== I
B("San Cristóbal se fundó en mil quinientos veintiocho, en un valle alto, rodeado de montañas y de neblina. Los españoles la llamaron Villa Real, y durante siglos fue la capital de Chiapas.",
  S("valley_dawn", cam=((0.4, 0.5, 1.05), (0.6, 0.48, 1.2), "linear"), fx=[FOG], tr="fade", tl=1.0, grade="cold",
    text=[T("CAPÍTULO I|Las crines trenzadas", "chapter", 0.6, 5.0)]),
  S("street_sc", LAMP, cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], tr="xfade", tl=0.8,
    text=[T("San Cristóbal de las Casas|fundada en 1528", "date", 0.5, 4.8)]),
  music="calm", amb=["wind", {"name": "crickets", "gain": -10}])
B("Calles empedradas, casas de adobe con techos de teja, aleros que casi se tocan. De noche, el frío baja de los cerros y la niebla se mete entre las puertas.",
  S("alley_sc", LAMP, FOGLAY, cam=((0.45, 0.55, 1.1), (0.55, 0.5, 1.3), "in"), fx=[FOGL], grade="night"))
B("Y cuentan que, al caer la tarde, por el camino de la sierra baja una recua de mulas cargadas de carbón.",
  S("road_mules", MULES, cam=((0.4, 0.55, 1.05), (0.6, 0.55, 1.2), "linear"), fx=["dust"], grade="warm"),
  sfx=[X("hooves", 0.3, -12, dur=8, distance=0.7), X("bell", 2.0, -20, freq=420)])
B("Nadie ve quién las arrea. Solo se oyen los cascos… y una guitarra que suena detrás.",
  S("road_mules", MULES, cam=((0.6, 0.6, 1.3), (0.7, 0.55, 1.45), "in"), fx=[FOGL], grade="night"), music="mystery")
B("Al otro día, los dueños de los caballos encuentran algo en los establos.",
  S("stable", LAMP, cam=((0.4, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=["dust"], grade="candle"))
B("Abren la puerta y los animales voltean a verlos con los ojos muy abiertos. Tienen espuma en el hocico. Y las patas llenas de lodo de caminos que nadie conoce.",
  S("stable", LAMP, cam=((0.55, 0.5, 1.3), (0.6, 0.48, 1.5), "in"), fx=["dust"], grade="night"),
  sfx=[X("hooves", 0.5, -16, dur=2, distance=0.2)])
B("Las crines y las colas de sus animales están trenzadas. Trencitas diminutas, apretadas, imposibles de deshacer. Los caballos sudan, tiemblan, como si alguien los hubiera montado toda la noche.",
  S("mane_close", cam=((0.45, 0.5, 1.1), (0.55, 0.45, 1.45), "in"), fx=["dust", PU(60, 0.05)], grade="moon",
    text=[T("NUDOS|que nadie puede deshacer", "big", 2.0, 5.5)]),
  S("corral_dawn", cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], grade="cold", tr="xfade", tl=0.8),
  sfx=[X("whisper", 1.0, -18, dur=3)])
B("Entonces la gente sabe que llegó él.",
  S("sombreron_full", SOMBG, cam=((0.5, 0.6, 1.0), (0.5, 0.55, 1.2), "in"), fx=[FOGL], grade="night"),
  music="tension", sfx=[X("boom", 0.2, -8)])
B("Un hombrecito que no le llega a la cintura a un adulto. Vestido de negro, como un charro, con botonadura de plata y unas botas diminutas que brillan.",
  S("sombreron_full", SOMB, cam=((0.5, 0.65, 1.4), (0.5, 0.6, 1.7), "in"), fx=[FOGL], grade="night"),
  sfx=[X("footsteps", 0.5, -14, dur=4)])
B("Y en la cabeza, un sombrero enorme. Tan grande que le cubre toda la cara. Nadie le ha visto los ojos. Bueno… casi nadie.",
  S("hat_brim", cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.4), "in"), fx=["dust"], grade="moon",
    text=[T("EL SOMBRERÓN|", "big", 0.5, 3.6)]),
  S("sombreron_eyes", tr="flash", tl=0.1, dur=1.2, fx=[SH(0, 0.4, 7)], cam=((0.5, 0.45, 1.4), (0.5, 0.45, 1.55))),
  sfx=[X("sting", 0.0, -4, at_scene=1)])
B("Le gustan los caballos. Pero lo que de verdad busca es otra cosa. Busca muchachas jóvenes, de ojos grandes… y de cabello muy largo.",
  S("sombreron_close", cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.35), "in"), fx=[FOG], grade="night"))

# ======================================================================== II
B("Dicen que cuando no encuentra caballos, les trenza la cola a los perros. Y que los perros, al verlo, no ladran. Se esconden debajo de las camas, temblando.",
  S("street_sc", LAMP, cam=((0.5, 0.6, 1.2), (0.5, 0.55, 1.4), "in"), fx=[FOGL], grade="night"),
  sfx=[X("howl", 0.5, -16)])
B("Y cuando escoge a una, hay una señal. Las mulas de carbón amanecen amarradas al poste de su casa. Esa es la advertencia. Después… empiezan las serenatas.",
  S("post_mules", LAMP, cam=((0.45, 0.55, 1.1), (0.5, 0.55, 1.3), "in"), fx=[FOGL], grade="night"))
B("En una de esas casas de adobe, cerca del templo de Santo Domingo, vivía una viuda con su única hija. La muchacha se llamaba Inés.",
  S("church_ext", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25), "in"), fx=[FOG], tr="fade", tl=1.0, grade="warm",
    text=[T("CAPÍTULO II|La serenata", "chapter", 0.6, 5.0)]),
  S("mother_portrait", CANDLE, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8),
  music="hope", amb=["city"], sfx=[X("bell", 0.5, -10, freq=180)])
B("Inés tenía diecisiete años y el cabello negro hasta las rodillas. Su madre se lo cepillaba cada noche, cien veces, a la luz de una vela, como se lo había cepillado a ella su abuela.",
  S("ines_portrait", CANDLE, cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle"),
  amb=["room"], sfx=[X("clock", 0.0, -18, dur=8)])
B("Era alegre, cantaba mientras lavaba la ropa en el patio, y los muchachos del barrio se peleaban por acompañarla a la fuente.",
  S("ines_portrait", cam=((0.45, 0.45, 1.2), (0.55, 0.42, 1.35)), fx=["dust"], grade="warm"))
B("Un domingo, al salir de misa, Inés vio a un hombrecito parado en la esquina de la plaza. No se movía. Solo la miraba desde abajo de su sombrero.",
  S("plaza_sc", cam=((0.4, 0.55, 1.05), (0.6, 0.5, 1.25), "linear"), fx=["dust"], grade="warm"),
  S("plaza_sc", SOMB, cam=((0.62, 0.6, 1.4), (0.66, 0.6, 1.6), "in"), fx=["dust"], grade="warm", tr="xfade", tl=0.6),
  music="tension")
B("Esa misma noche, las mulas de carbón amanecieron amarradas al poste de su casa.",
  S("post_mules", LAMP, cam=((0.5, 0.55, 1.05), (0.55, 0.55, 1.3), "in"), fx=[FOGL], grade="night"),
  amb=["night", {"name": "wind", "gain": -8}], sfx=[X("hooves", 0.0, -14, dur=3, distance=0.4)])
B("Y a la medianoche empezó la serenata.",
  S("house_window", WING, SOMB, NOTES, cam=((0.5, 0.55, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], grade="night"),
  music="mystery")
B("Ay, muchacha de pelo de noche… asómate, que te vengo a cantar.",
  S("sombreron_full", SOMB, NOTES, cam=((0.5, 0.55, 1.3), (0.5, 0.5, 1.45)), fx=[FOGL], grade="moon"),
  pre=0.4, **SOM)
B("La voz era dulce. Demasiado dulce para salir de un cuerpo tan pequeño. Y la guitarra… dicen que era de plata, y que sus cuerdas brillaban en la oscuridad.",
  S("guitar_close", NOTES, cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.35), "in"), fx=["dust"], grade="moon"))
B("Inés se asomó por la ventana. Abajo no vio a nadie. Solo la sombra redonda de un sombrero enorme, sobre el empedrado.",
  S("ines_window", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FOG], grade="moon"),
  S("street_shadow", cam=((0.5, 0.6, 1.1), (0.5, 0.65, 1.35), "in"), fx=[FOGL], grade="cold", tr="xfade", tl=0.6))
B("Volvió a la cama. Y antes de dormirse, sin darse cuenta, empezó a tararear la canción. Una canción que nadie le había enseñado.",
  S("ines_sleep", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.25)), fx=["dust"], grade="moon"),
  sfx=[X("whisper", 1.5, -20, dur=3)])
B("Al otro día, su cabello amaneció trenzado.",
  S("ines_braids", cam=((0.5, 0.42, 1.1), (0.5, 0.4, 1.35), "in"), fx=["dust"], grade="cold"),
  sfx=[X("sting", 0.3, -8)])
B("Si esta historia ya te dio frío, suscríbete y activa la campanita. Cada semana te traigo una leyenda nueva de México.",
  S("valley_night", FOGLAY, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.05), "out"), fx=["dust"], grade="night"))
B("Mamá… ¿tú me trenzaste el pelo anoche?",
  S("ines_braids", CANDLE, cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.5)), fx=[FL], grade="candle"), **INES)
B("Su madre no contestó. Tomó un peine e intentó deshacer las trenzas. No pudo. Estaban tan apretadas que parecían de alambre.",
  S("mother_fear", CANDLE, cam=((0.5, 0.42, 1.2), (0.5, 0.42, 1.4)), fx=[FL], grade="candle"),
  S("braids_pillow", cam=((0.4, 0.5, 1.3), (0.5, 0.5, 1.5), "in"), fx=["dust"], grade="candle", tr="xfade", tl=0.6))

# ======================================================================== III
B("Las serenatas siguieron. Una noche, y otra, y otra.",
  S("house_window", WING, SOMB, NOTES, cam=((0.5, 0.5, 1.2), (0.5, 0.48, 1.35), "in"), fx=[FOGL], tr="fade", tl=1.0, grade="night",
    text=[T("CAPÍTULO III|La tierra en el plato", "chapter", 0.6, 5.0)]),
  music="dread", amb=["night", {"name": "wind", "gain": -8}])
B("Y algo empezó a cambiar en Inés. Ya no salía a la plaza. Pasaba el día junto a la ventana, esperando que oscureciera.",
  S("ines_window", cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.4)), fx=[FOG], grade="cold"))
B("Dejó de comer. Su madre le servía frijoles, tortillas calientes, chocolate. Pero cuando Inés acercaba la cuchara a la boca…",
  S("table_food", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.52, 1.3), "in"), fx=[FL], grade="candle"),
  amb=["room"])
B("en el plato solo había tierra.",
  S("plate_earth", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.5), "in"), fx=[PU(80, 0.06)], grade="cold",
    text=[T("TIERRA|", "big", 0.8, 4.0)]),
  S("red_flash", tr="flash", tl=0.1, dur=0.8, fx=[SH(0, 0.4, 6)], grade="blood"),
  sfx=[X("boom", 0.2, -6), X("sting", 0.0, -5, at_scene=1)])
B("Tierra negra, húmeda, como la de los panteones. Su madre volvía a mirar, y la comida estaba ahí. Pero Inés no podía tragar ni un bocado.",
  S("plate_earth", CANDLE, cam=((0.45, 0.5, 1.4), (0.55, 0.5, 1.6)), fx=[FL], grade="candle"))
B("Pasaron las semanas. Inés se puso pálida, flaca. Las ojeras le hundían los ojos. Y cada mañana, sin falta, amanecía con el cabello trenzado.",
  S("ines_thin", cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FOG], grade="cold"),
  sfx=[X("heartbeat", 0.0, -12, dur=10, bpm=60)])
B("Su madre hizo todo lo que se le ocurrió. Clavó la ventana con tablas. Puso agua bendita en el umbral, una cruz de palma sobre la cama, ruda detrás de la puerta.",
  S("room_window_open", CANDLE, cam=((0.5, 0.5, 1.2), (0.45, 0.5, 1.35)), fx=[FL], grade="candle"),
  sfx=[X("knock", 0.6, -10, times=4)])
B("No sirvió de nada. A la mañana siguiente, las tablas seguían clavadas… y el cabello de Inés estaba trenzado otra vez.",
  S("ines_braids", cam=((0.5, 0.42, 1.2), (0.5, 0.4, 1.4), "in"), fx=[FOG], grade="cold"),
  sfx=[X("sting", 2.5, -8)])
B("Una noche, su madre se quedó despierta detrás de la puerta. Quería verlo con sus propios ojos.",
  S("room_ines", CANDLE, cam=((0.55, 0.5, 1.2), (0.6, 0.5, 1.4), "in"), fx=[FL], grade="candle"),
  amb=["room", {"name": "clock", "gain": -8}], sfx=[X("clock", 0.0, -14, dur=6)])
B("A las tres de la mañana, la vela se apagó sola. Y en la oscuridad oyó una risita. Pequeña. Junto a la cama de su hija.",
  S("candle_out", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.4), "in"), fx=[FL], grade="candle"),
  S("black", dur=2.2),
  sfx=[X("gust", 0.5, -8), X("whisper", 0.0, -10, at_scene=1, dur=2)], music="silence")
B("Y luego, el ruido más suave del mundo. Dedos diminutos, pasando entre el cabello.",
  S("ines_sleep", cam=((0.5, 0.45, 1.3), (0.5, 0.42, 1.55), "in"), fx=[FOG, PU(90, 0.06)], grade="night"),
  music="dread", sfx=[X("whisper", 0.5, -14, dur=5), X("heartbeat", 0.0, -8, dur=8, bpm=95)])
B("La madre encendió un cerillo. Sobre la almohada vio un sombrero inmenso, inclinado sobre la cara de su hija.",
  S("sombreron_bed", cam=((0.5, 0.5, 1.15), (0.5, 0.45, 1.4), "in"), fx=[FL], grade="candle"),
  sfx=[X("fire", 0.0, -12)])
B("Y debajo del ala, por un segundo, dos ojos que brillaban como brasas.",
  S("sombreron_eyes", tr="flash", tl=0.12, cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.6), "in"), fx=[SH(0, 0.6, 10), PU(120, 0.1)]),
  pause=0.8, sfx=[X("sting", 0.0, -2), X("boom", 0.0, -3), X("riser", -3.0, -8, dur=3)])
B("El cerillo se apagó. Cuando encendió otro, ya no había nadie. Solo la ventana abierta, y la guitarra alejándose por la calle.",
  S("room_window_open", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.35), "in"), fx=[FOG], grade="cold"),
  S("street_sc", NOTES, cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.5), "in"), fx=[FOGL], grade="cold", tr="xfade", tl=0.8),
  sfx=[X("gust", 0.0, -10)])

# ======================================================================== IV
B("Al amanecer, la madre corrió a buscar a una anciana del barrio de Mexicanos, que sabía de estas cosas.",
  S("valley_dawn", cam=((0.6, 0.5, 1.2), (0.45, 0.5, 1.05), "out"), fx=[FOG], tr="fade", tl=1.0, grade="cold",
    text=[T("CAPÍTULO IV|Las tijeras", "chapter", 0.6, 5.0)]),
  music="sad", amb=["wind", {"name": "crickets", "gain": -12}])
B("La anciana escuchó todo sin decir nada. Luego le tomó las manos.",
  S("abuela", CANDLE, cam=((0.5, 0.45, 1.05), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle"), amb=["room"])
B("No le sirven los rezos, hija. Lo que él quiere es el cabello. Córtaselo. Todo. Y llévalo al templo para que el padre lo bendiga.",
  S("abuela", CANDLE, cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.5)), fx=[FL], grade="candle"), **ABU)
B("Esa tarde, la madre sentó a Inés frente al espejo. Inés lloraba. No quería. Decía que él se iba a enojar.",
  S("ines_fear", CANDLE, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle"), music="tension")
B("Tomó las tijeras grandes, las de cortar tela. Le temblaban las manos. Afuera, aunque todavía era de día, se oyó a lo lejos una guitarra.",
  S("scissors_cut", CANDLE, cam=((0.45, 0.5, 1.3), (0.55, 0.5, 1.5)), fx=[FL], grade="candle"),
  sfx=[X("whisper", 2.0, -16, dur=3)])
B("Si me lo cortas, ya no va a volver a cantarme.",
  S("ines_fear", CANDLE, cam=((0.5, 0.42, 1.35), (0.5, 0.42, 1.5)), fx=[FL], grade="candle"), **INES)
B("Por eso mismo, hija. Por eso mismo.",
  S("mother_fear", CANDLE, cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.45)), fx=[FL], grade="candle"), **MOM)
B("Las tijeras sonaron una vez. Y otra. Y otra. Las trenzas negras fueron cayendo al suelo, una por una.",
  S("scissors_cut", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.4), "in"), fx=[FL], grade="candle"),
  S("hair_table", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  sfx=[X("knock", 0.3, -14, times=3)])
B("Afuera, en ese momento, todos los caballos de la calle relincharon al mismo tiempo.",
  S("stable", LAMP, cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.4), "in"), fx=["dust", SH(0.5, 2.5, 5)], grade="night"),
  sfx=[X("hooves", 0.0, -6, dur=3, distance=0.2), X("thunder", 0.8, -8)])
B("La madre envolvió el cabello en un rebozo y lo llevó al templo de Santo Domingo. El sacerdote lo roció con agua bendita y rezó por la muchacha.",
  S("church_int", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FL], grade="candle"),
  S("altar_hair", CANDLE, cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.4), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8),
  music="hope", amb=["room"], sfx=[X("bell", 0.5, -10, freq=160), X("splash", 6.0, -14)])
B("Dicen que mientras rezaba, las velas del altar se inclinaron todas hacia la puerta. Como si alguien, desde afuera, estuviera soplando.",
  S("church_int", cam=((0.5, 0.5, 1.3), (0.5, 0.45, 1.5), "in"), fx=[FL, {"type": "flicker", "amp": 0.2}], grade="candle"),
  sfx=[X("gust", 0.5, -10), X("whisper", 1.5, -16, dur=3)])
B("Esa noche, la guitarra volvió. Pero ya no sonaba dulce.",
  S("house_window", SOMB, cam=((0.5, 0.55, 1.15), (0.5, 0.5, 1.35), "in"), fx=[FOGL], grade="night"),
  music="dread", amb=["night", {"name": "wind", "gain": -6}])
B("Sonaba desafinada, rabiosa, como si alguien arrancara las cuerdas con las uñas. Y en medio de la música se oía un llanto. Un llanto de hombre, de niño, de animal.",
  S("sombreron_cry", cam=((0.5, 0.5, 1.1), (0.5, 0.45, 1.4), "in"), fx=[FOG, SH(1.0, 3.0, 4)], grade="cold"),
  sfx=[X("whisper", 0.0, -12, dur=6), X("gust", 3.0, -8)])
B("¿Dónde está su cabello? ¿Dónde está su cabello?",
  S("sombreron_eyes", cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.5)), fx=[PU(110, 0.1)], grade="blood"),
  S("red_flash", tr="flash", tl=0.1, dur=0.8, fx=[SH(0, 0.4, 8)], grade="blood"),
  sfx=[X("boom", 0.0, -4, at_scene=1), X("sting", 0.0, -3, at_scene=1)], **SOM)
B("Golpeó la puerta toda la noche. La madre abrazó a su hija, rezando, hasta que cantó el primer gallo.",
  S("room_ines", CANDLE, cam=((0.5, 0.5, 1.1), (0.45, 0.5, 1.3)), fx=[FL, SH(0.5, 1.5, 4)], grade="candle"),
  sfx=[X("knock", 0.2, -6, times=4), X("knock", 3.5, -8, times=3)])
B("Al amanecer, las mulas ya no estaban. Y desde los cerros se oyó un caballo negro alejándose al galope.",
  S("rider_ridge", RIDER, cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=[FOG], grade="cold"),
  music="calm", sfx=[X("hooves", 0.5, -10, dur=7, distance=0.8)])
B("Inés volvió a comer. Volvió a la plaza. Y su cabello creció otra vez… pero ella nunca volvió a dejarlo largo.",
  S("ines_portrait", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.05), "out"), fx=["dust"], grade="warm"),
  amb=["city"])

# ======================================================================== V
B("Ahora, lo que sí es historia.",
  S("map_chiapas", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.15)), fx=["dust"], tr="fade", tl=1.0, grade="sepia",
    text=[T("CAPÍTULO V|Lo que dice la historia", "chapter", 0.6, 4.6)]),
  pre=0.6, music="mystery", amb=["room"])
B("El Sombrerón es una leyenda que comparten Chiapas y Guatemala. No es casualidad: durante la época colonial, Chiapas formó parte de la Capitanía General de Guatemala, y se unió a México apenas en mil ochocientos veinticuatro.",
  S("map_chiapas", cam=((0.45, 0.5, 1.2), (0.55, 0.5, 1.45), "in"), fx=["dust"], grade="sepia",
    text=[T("1824|Chiapas se une a México", "date", 3.0, 7.5)]))
B("En Guatemala también lo llaman Tzipitío o Duende. Allá, la versión más famosa ocurre en la vieja capital, y la muchacha termina encerrada en un convento.",
  S("chronicle", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="sepia"))
B("En mil novecientos treinta, el escritor guatemalteco Miguel Ángel Asturias, que después ganaría el Premio Nobel de Literatura, incluyó su propia versión del Sombrerón en su libro Leyendas de Guatemala.",
  S("book_1930", CANDLE, cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.3), "in"), fx=[FL], grade="candle",
    text=[T("Leyendas de Guatemala|Miguel Ángel Asturias, 1930", "date", 1.0, 6.0)]))
B("Y del lado mexicano, el poeta Bernardo Ortiz de Montellano escribió una obra de teatro llamada El Sombrerón, que se publicó en mil novecientos cuarenta y seis.",
  S("stage_1946", cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=["dust", FL], grade="candle",
    text=[T("El Sombrerón|Bernardo Ortiz de Montellano, 1946", "date", 1.0, 6.0)]))
B("En mil novecientos cincuenta se estrenó en Guatemala una película llamada El Sombrerón, una de las primeras que se filmaron en ese país. Y en Chiapas, hasta hoy, las abuelas siguen contando la historia en las noches de frío.",
  S("film_1950", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "in"), fx=["dust", {"type": "flicker", "amp": 0.1}], grade="sepia",
    text=[T("El Sombrerón|película, Guatemala, 1950", "date", 1.0, 6.0)]))
B("Las versiones no se ponen de acuerdo en todo. En unas es diminuto. En otras es un hombre alto y elegante, de traje negro con botones de oro. En unas pone tierra en la comida; en otras, solo canta.",
  S("sombreron_full", SOMB, cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.3), "in"), fx=[FOGL], grade="night"),
  S("hat_brim", cam=((0.4, 0.5, 1.2), (0.6, 0.5, 1.35)), fx=["dust"], grade="moon", tr="xfade", tl=0.8))
B("Pero en todas busca lo mismo: muchachas de cabello largo. Y en casi todas, el remedio es cortarlo.",
  S("hair_table", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.4), "in"), fx=["dust"], grade="candle"))
B("Algunos historiadores creen que era una advertencia para las hijas de familia: no le abras la ventana a cualquiera que te cante bonito.",
  S("ines_window", cam=((0.5, 0.42, 1.05), (0.5, 0.42, 1.25), "in"), fx=[FOG], grade="moon"))
B("Y en los pueblos donde hay caballos, todavía hay quien amanece con las crines de sus animales trenzadas… y no sabe explicar por qué.",
  S("corral_dawn", cam=((0.5, 0.55, 1.2), (0.5, 0.5, 1.05), "out"), fx=[FOGL], grade="cold"),
  S("mane_close", cam=((0.5, 0.5, 1.3), (0.5, 0.5, 1.5), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.8))

# ======================================================================== ENDING / payoff
B("¿Y la madre de Inés? Cuentan que, una semana después, abrió la ventana para que entrara el sol.",
  S("room_ines", cam=((0.5, 0.5, 1.1), (0.55, 0.5, 1.3), "in"), fx=["dust"], tr="fade", tl=1.0, grade="warm"),
  music="tension", amb=["wind"])
B("Y sobre el pretil encontró un rebozo. El mismo rebozo en el que había llevado el cabello al templo.",
  S("windowsill", cam=((0.5, 0.5, 1.05), (0.5, 0.52, 1.3), "in"), fx=["dust"], grade="cold"))
B("Adentro estaba el cabello de su hija. Bendito, como lo había dejado. Pero alguien lo había trenzado otra vez. Decenas de trencitas finas, perfectas.",
  S("windowsill_braid", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.55), "in"), fx=["dust", PU(70, 0.06)], grade="cold"),
  music="dread", sfx=[X("heartbeat", 0.0, -9, dur=10, bpm=80)])
B("Y amarrado en la punta, con un listón negro… un pétalo de rosa todavía húmedo.",
  S("rose_close", cam=((0.5, 0.5, 1.2), (0.5, 0.5, 1.6), "in"), fx=[PU(80, 0.08)], grade="cold"),
  S("sombreron_eyes", tr="flash", tl=0.12, dur=1.3, fx=[SH(0, 0.5, 9)], cam=((0.5, 0.45, 1.35), (0.5, 0.45, 1.55))),
  pause=0.8, sfx=[X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)])
B("Porque el Sombrerón no se va. Solo espera.",
  S("sombreron_close", cam=((0.5, 0.5, 1.2), (0.5, 0.45, 1.45), "in"), fx=[FOG], grade="night"), pause=1.0)
B("Y tú, ¿le abrirías la ventana a una serenata a las tres de la mañana? ¿En tu pueblo también cuentan del Sombrerón? Te leo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOG], tr="fade", tl=0.8), music="mystery")
B("En el próximo video conocerás a un perro negro de ojos rojos que sigue a los caminantes de noche por los caminos del sur. Algunos dicen que te protege. Otros, que te lleva. Lo llaman El Cadejo.",
  S("cadejo", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOGL], grade="night",
    text=[T("PRÓXIMO VIDEO|El Cadejo", "big", 2.0, 7.0)]), sfx=[X("howl", 1.0, -12)])
B("Hasta la próxima leyenda. Y si alguna noche oyes una guitarra debajo de tu ventana… no te asomes.",
  S("house_window", WING, SOMB, NOTES, cam=((0.5, 0.5, 1.2), (0.5, 0.48, 1.45), "in"), fx=[FOGL], grade="moon", out=2.0),
  pause=1.0, music="dread")

VARIANTS = {"house_window": ["house_window", "house_window2"], "sombreron_eyes": ["sombreron_eyes", "sombreron_eyes2"],
            "room_ines": ["room_ines", "room_ines2"], "street_sc": ["street_sc", "street_sc2"],
            "ines_braids": ["ines_braids", "ines_braids2"], "mother_fear": ["mother_fear", "mother_dark"],
            "sombreron_full": ["sombreron_full", "sombreron_full2"], "ines_window": ["ines_window", "ines_window2"],
            "valley_night": ["valley_night", "valley_night2"]}
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

story = {"title": "El Sombrerón", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "E", "seed": 81, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# El Sombrerón — guion\n",
                  "Narración en español (narrador: em_alex; la madre, Inés y la anciana: ef_dora; el Sombrerón: em_santa con eco).\n"]
WHO = {"ef_dora": "VOZ FEMENINA: ", "em_santa": "EL SOMBRERÓN: "}
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
