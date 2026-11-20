#!/usr/bin/env python3
"""Builds story.json and script.md for 'La Monja de La Concepción' (Ciudad de México). Edit BEATS here, then run.
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
MOONG = L("l_moon_glow", blend="screen", anim=[{"type": "pulse", "amp": 0.05, "period": 5, "pivot": [0.48, 0.45]}])
GHOST = L("l_ghost_nun", blend="screen", opacity=[0, 0.95], fade_in=2.0, anim=[{"type": "float", "amp": 0.004, "period": 5}, {"type": "flicker", "amp": 0.1, "speed": 0.8}])
GHOSTF = L("l_ghost_nun_far", blend="screen", opacity=[0, 0.9], fade_in=1.5, anim=[{"type": "float", "amp": 0.003, "period": 5}])
GHOSTQ = L("l_ghost_nun", blend="screen", opacity=[0, 0.95], appear_at=0.5, fade_in=0.4, vanish_at=3.2, fade_out=0.4, anim=[{"type": "float", "amp": 0.004, "period": 5}])

MAR = dict(voice="ef_dora", speed=0.8)
MARG = dict(voice="ef_dora", speed=0.7, fx="eco")
ARR = dict(voice="em_santa", speed=0.86)
ALO = dict(voice="em_santa", speed=0.8)
NIGHT = ["night", {"name": "wind", "gain": -9}]
CHAPEL = ["room", {"name": "drips", "gain": -14}]
FLASH = lambda img="nun_flash": S(img, tr="flash", tl=0.12, dur=1.4, cam=((0.5, 0.45, 1.25), (0.5, 0.45, 1.5)), fx=[SH(0, 0.6, 9)])
SCARE = [X("riser", -3.5, -8, at_scene=1, dur=3.5), X("sting", 0.0, -2, at_scene=1), X("boom", 0.0, -3, at_scene=1)]

# ======================================================================== COLD OPEN
B("Ciudad de México. Huerto del convento de La Concepción. Las tres de la mañana.",
  S("huerto_fog", FOGLAY, cam=((0.5, 0.5, 1.05), (0.48, 0.55, 1.25), "in"), fx=[FOGL], tr="fade", tl=1.2,
    text=[T("Convento de La Concepción|Ciudad de México, siglo dieciséis", "date", 0.6, 5.0)]),
  pre=0.6, music="dread", amb=NIGHT, sfx=[X("bell", 1.5, -14, freq=180), X("bell", 4.5, -16, freq=180), X("bell", 7.5, -18, freq=180)])
B("Imagina que eres una novicia y no puedes dormir. Desde la ventana de tu celda ves el huerto, los surcos de hierbas, el pozo… y el viejo durazno.",
  S("cell_window", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust"], grade="candle"),
  S("huerto", MOONG, cam=((0.3, 0.55, 1.1), (0.5, 0.55, 1.3), "linear"), fx=[FOGL], tr="xfade", tl=0.8))
B("Debajo del durazno hay alguien. Una monja. De pie, inmóvil, con el velo negro moviéndose aunque no corre ni una gota de viento.",
  S("huerto_fog", GHOST, cam=((0.48, 0.6, 1.2), (0.48, 0.62, 1.55), "in"), fx=[FOGL, PU(70, 0.06)], grade="cold"),
  music="tension", sfx=[X("heartbeat", 0.5, -12, dur=8, bpm=80), X("whisper", 3.0, -18, dur=4)])
B("Y entonces levanta la cara hacia tu ventana. Y no tiene ojos. Solo dos huecos negros… que te están mirando.",
  S("huerto_ghost", cam=((0.48, 0.55, 1.4), (0.48, 0.55, 1.7), "in"), fx=[FOGL]),
  FLASH(), pause=0.6, sfx=SCARE)
B("¿Por qué no volviste?",
  S("nun_ghost", cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.5), "in"), fx=[FOG, {"type": "flicker", "amp": 0.1}], grade="cold",
    text=[T("¿Por qué no volviste?|", "whisper", 0.3, 3.5)]), **MARG, pause=0.9)
B("",
  S("title_bg", cam=((0.5, 0.5, 1.0), (0.5, 0.48, 1.12)), fx=[FOG], tr="fade", tl=0.8,
    text=[T("LA MONJA|de La Concepción", "title", 0.6, 6.4)]),
  pause=5.2, music="mystery", sfx=[X("boom", 0.4, -4), X("whoosh", 0.3, -8)])
B("Las monjas de La Concepción la vieron durante años. Sabían quién era. Y sabían a quién seguía esperando.",
  S("nuns_line", cam=((0.4, 0.55, 1.05), (0.6, 0.55, 1.2), "linear"), fx=[FOGL], grade="night"))
B("Lo que encontraron debajo de su almohada, y quién tocó una noche la puerta del convento preguntando por ella… lo vas a saber al final.",
  S("convent_gate", FOGLAY, cam=((0.6, 0.6, 1.15), (0.6, 0.62, 1.4), "in"), fx=[FOGL], grade="night"),
  sfx=[X("knock", 2.5, -8, times=3)])

# ======================================================================== I
B("Cuentan que esta historia ocurrió hacia mil quinientos sesenta, en la Ciudad de México, apenas cuarenta años después de la caída de Tenochtitlan.",
  S("plaza_1560", cam=((0.4, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=["dust"], tr="fade", tl=1.0, grade="warm",
    text=[T("CAPÍTULO I|La hermana de los Ávila", "chapter", 0.6, 5.0)]),
  music="calm", amb=["city", {"name": "wind", "gain": -12}])
B("La ciudad nueva crecía sobre las ruinas de la vieja. Iglesias a medio construir, canales, casas de piedra de los conquistadores y de sus hijos.",
  S("ciudad_noche", cam=((0.3, 0.5, 1.05), (0.6, 0.5, 1.2), "linear"), fx=[FOGL], grade="night"))
B("En una de esas casas, de las más ricas, vivía una muchacha llamada María de Ávila.",
  S("casa_avila", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust"], grade="night"),
  S("maria_lady", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust"], tr="xfade", tl=0.8))
B("Era hermosa, dicen. Y era muy rica. Pero no mandaba en su vida. Porque sus padres habían muerto y quienes decidían por ella eran sus dos hermanos mayores. Alonso y Gil.",
  S("maria_soft", CAND, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle"),
  S("brothers", CAND, cam=((0.5, 0.5, 1.05), (0.5, 0.48, 1.25), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6,
    text=[T("Alonso y Gil de Ávila|", "date", 1.0, 5.0)]))
B("Los Ávila eran hijos de conquistadores. Orgullosos, poderosos, acostumbrados a que nadie les dijera que no. Para ellos, su hermana solo podía casarse con alguien de su misma sangre y de su misma fortuna.",
  S("alonso", CAND, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=[FL], grade="candle"),
  S("gil", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6))
B("Pero el corazón no pregunta apellidos.",
  S("maria_lady", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.45), "in"), fx=["dust"]), pause=0.8, music="hope")
B("María se enamoró de un joven llamado Arrutia. Un mestizo, dicen unas versiones. Un muchacho sin fortuna, dicen otras. Simpático, de buena conversación, con una sonrisa que abría todas las puertas.",
  S("arrutia_smile", CAND, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle"),
  S("arrutia", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.35), "in"), fx=["dust"], tr="xfade", tl=0.6))
B("Se veían a escondidas. Él pasaba de noche bajo su balcón. Ella dejaba caer cartas atadas con un listón. Y se juraron lo que se juran los enamorados. Que nada ni nadie los iba a separar.",
  S("courtship", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOGL], grade="night"),
  S("letter", CAND, cam=((0.4, 0.6, 1.1), (0.45, 0.62, 1.35), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  amb=["night"], sfx=[X("footsteps", 0.5, -16, dur=4)])
B("Yo te espero, Arrutia. Aunque me cueste la vida, yo te espero.",
  S("maria_soft", cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.45), "in"), fx=[FL], grade="candle",
    text=[T("Yo te espero.|María de Ávila", "quote", 0.4, 4.5)]), **MAR, pause=0.9)

# ======================================================================== II
B("Pero en una ciudad tan pequeña, los secretos duran poco. Una criada habló. Y una noche, los hermanos Ávila esperaron a Arrutia en la oscuridad.",
  S("ciudad_noche", FOGLAY, cam=((0.6, 0.55, 1.2), (0.5, 0.55, 1.05), "out"), fx=[FOGL], tr="fade", tl=1.0, grade="night",
    text=[T("CAPÍTULO II|La carta", "chapter", 0.6, 5.0)]),
  music="tension", amb=NIGHT)
B("No lo golpearon. No lo amenazaron. Hicieron algo peor. Pusieron sobre la mesa una bolsa llena de monedas de oro.",
  S("coins", CAND, cam=((0.45, 0.6, 1.1), (0.55, 0.62, 1.35), "in"), fx=[FL], grade="candle"),
  sfx=[X("coins", 4.5, -6)])
B("Toma esto y vete. Vete lejos, y no vuelvas a acercarte a nuestra hermana.",
  S("alonso_red", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.4), "in"), fx=[PU(60, 0.06)], grade="blood",
    text=[T("Vete lejos.|Alonso de Ávila", "quote", 0.4, 4.5)]), **ALO)
B("Arrutia miró el oro mucho tiempo. Pensó en María. Pensó en su pobreza. Y tomó la bolsa.",
  S("arrutia_shock", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="cold"),
  S("coins", cam=((0.6, 0.65, 1.35), (0.6, 0.66, 1.55), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6), pause=0.8)
B("Esa misma semana salió rumbo al puerto de Veracruz. Algunos dicen que se embarcó hacia España. Otros, que se quedó en la costa, haciendo negocios con el dinero de los Ávila.",
  S("veracruz", cam=((0.3, 0.55, 1.05), (0.6, 0.55, 1.2), "linear"), fx=[FOGL], grade="night"),
  amb=["sea", {"name": "wind", "gain": -10}], music="sad")
B("A María solo le dejó una carta. Corta. Fría. Con letra apurada.",
  S("letter_close", CAND, cam=((0.5, 0.45, 1.05), (0.45, 0.4, 1.3), "in"), fx=[FL], grade="candle"),
  amb=["room"])
B("Asuntos de mi oficio me obligan a partir lejos de esta ciudad. No me esperéis. Que Dios os guarde.",
  S("letter_close", cam=((0.4, 0.4, 1.4), (0.45, 0.55, 1.5), "linear"), fx=[FL], grade="candle",
    text=[T("No me esperéis.|", "whisper", 3.5, 7.0)]), **ARR)
B("María leyó la carta una vez. Y otra. Y otra más. No lloró delante de nadie. Pero esa noche, la criada la escuchó hablar sola en su cuarto, hasta el amanecer.",
  S("maria_sad", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="moon"),
  sfx=[X("whisper", 5.0, -18, dur=5)])
B("Va a volver. Sé que va a volver.",
  S("maria_fear", CAND, cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.45), "in"), fx=[FL], grade="candle"), **MAR)
B("Durante semanas, María se asomó al balcón cada noche, a la misma hora, esperando oír sus pasos en la calle empedrada. Los pasos nunca llegaron.",
  S("courtship", cam=((0.5, 0.45, 1.2), (0.5, 0.42, 1.4), "in"), fx=[FOGL], grade="moon"),
  sfx=[X("clock", 0.5, -18, dur=6)])
B("Los hermanos decidieron que eso tenía que terminar. Y para una muchacha de buena familia, en aquel tiempo, solo había dos caminos. El matrimonio… o el convento.",
  S("brothers", cam=((0.5, 0.5, 1.15), (0.5, 0.48, 1.35), "in"), fx=[FL], grade="candle"),
  S("convent_ext", FOGLAY, cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOGL], grade="night", tr="xfade", tl=0.8),
  music="dread", sfx=[X("bell", 6.0, -12, freq=160)])
B("Si te gustan estas historias, suscríbete y activa la campanita. Cada semana traemos una leyenda nueva de algún rincón de México.",
  S("title_bg", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.2)), fx=[FOG], tr="xfade", tl=0.6), music="mystery")

# ======================================================================== III
B("El convento de La Concepción era el más antiguo de la ciudad. Muros altos, rejas en las ventanas, un torno de madera para recibir lo que llegaba de afuera. Quien entraba ahí, entraba para siempre.",
  S("convent_ext", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], tr="fade", tl=1.0, grade="night",
    text=[T("CAPÍTULO III|El durazno", "chapter", 0.6, 5.0)]),
  S("cloister", cam=((0.4, 0.55, 1.1), (0.6, 0.55, 1.2), "linear"), fx=[FOGL], tr="xfade", tl=0.6),
  music="mystery", amb=CHAPEL)
B("A María le cortaron el cabello. Le quitaron sus vestidos de seda y le pusieron el hábito blanco, el manto azul y el velo. Y la puerta se cerró detrás de ella.",
  S("chapel", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=["dust", FL], grade="candle"),
  S("nun_portrait", CAND, cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.8),
  sfx=[X("door", 9.5, -4), X("boom", 9.6, -10)])
B("Las otras monjas la recordaban como una novicia callada, obediente, que cumplía con todo. Rezaba en el coro. Bordaba. Ayudaba en la cocina.",
  S("nuns_line", cam=((0.6, 0.55, 1.1), (0.4, 0.55, 1.2), "linear"), fx=[FOGL], grade="candle"),
  S("nun_pray", CAND, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.3), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6),
  amb=["room"], sfx=[X("bell", 0.5, -18, freq=300)])
B("Pero había algo que todas notaban. Cada tarde, cuando terminaban las labores, María salía sola al huerto y se sentaba debajo del durazno. Mirando hacia la puerta.",
  S("huerto_dawn", cam=((0.3, 0.55, 1.05), (0.5, 0.55, 1.25), "in"), fx=[FOGL], grade="warm"),
  S("durazno_bloom", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25), "in"), fx=["dust"], tr="xfade", tl=0.8),
  music="sad", amb=["crickets"])
B("El durazno era el árbol más viejo del huerto. Las monjas decían que lo habían plantado las primeras hermanas del convento, y que daba los frutos más dulces de toda la ciudad.",
  S("durazno_close", cam=((0.4, 0.5, 1.05), (0.55, 0.45, 1.25), "linear"), fx=["dust"], grade="moon"))
B("Cada vez que sonaba la campana del torno, María levantaba la cabeza. Cada vez que llegaba una carta, preguntaba si era para ella. Nunca lo era.",
  S("bells", cam=((0.5, 0.45, 1.05), (0.5, 0.4, 1.3), "in"), fx=[FOG], grade="night"),
  S("nun_sad", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.6),
  sfx=[X("bell", 0.6, -10, freq=420), X("bell", 1.6, -12, freq=420)])
B("Pasaron los meses. Dejó de comer. Dejó de dormir. Por las noches, las monjas de las celdas vecinas la escuchaban rezar en voz baja. Y a veces, entre los rezos, un nombre.",
  S("cell_nun", CAND, cam=((0.45, 0.6, 1.1), (0.45, 0.6, 1.35), "in"), fx=[FL], grade="candle"),
  amb=["room", {"name": "clock", "gain": -14}], music="dread")
B("Arrutia… Arrutia…",
  S("cell_window", cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.5), "in"), fx=[FL], grade="candle",
    text=[T("Arrutia…|", "whisper", 0.3, 3.5)]), voice="ef_dora", speed=0.7, pause=0.9)
B("La madre abadesa le habló con dulzura. Le dijo que pusiera su pena en manos de Dios. Que el mundo de afuera ya no existía para ella. María bajó la cabeza y no respondió.",
  S("corridor", cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.3), "in"), fx=[FL], grade="candle"),
  S("nun_pray", cam=((0.5, 0.42, 1.3), (0.5, 0.42, 1.45), "in"), fx=[FL], grade="candle", tr="xfade", tl=0.6))
B("Esa noche hubo luna llena. Y a la mañana siguiente, la monja que abría el huerto para sacar agua del pozo encontró a María.",
  S("huerto", MOONG, cam=((0.5, 0.5, 1.05), (0.48, 0.55, 1.3), "in"), fx=[FOGL], grade="night"),
  S("huerto_dawn", cam=((0.6, 0.55, 1.2), (0.48, 0.6, 1.4), "in"), fx=[FOGL], grade="cold", tr="fade", tl=1.0),
  music="silence", amb=["wind"], sfx=[X("bell", 5.5, -14, freq=200)])
B("Al pie del durazno. Sin vida. Con el velo caído sobre la hierba y los duraznos regados a su alrededor.",
  S("fallen_peaches", cam=((0.5, 0.5, 1.05), (0.5, 0.55, 1.3), "in"), fx=["dust"], grade="cold"),
  sfx=[X("sting", 0.3, -10)], pause=1.0, music="sad")
B("Dicen que María, en su desesperación, se quitó la vida. Que pidió perdón a Dios y que en sus últimas palabras volvió a llamar al hombre que la había abandonado.",
  S("durazno_close", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=["ash", FOG], grade="moon"))
B("Nunca supo que Arrutia no se fue por trabajo. Que sus propios hermanos lo habían comprado.",
  S("coins", cam=((0.5, 0.6, 1.3), (0.5, 0.6, 1.5), "in"), fx=[FL], grade="blood"), pause=1.0)

# ======================================================================== IV
B("La enterraron en el convento, en silencio, como se hacía entonces con estas desgracias. Y las monjas creyeron que ahí terminaba todo.",
  S("chapel", cam=((0.5, 0.5, 1.15), (0.5, 0.5, 1.3), "in"), fx=["dust", FL], tr="fade", tl=1.0, grade="candle",
    text=[T("CAPÍTULO IV|La que espera", "chapter", 0.6, 5.0)]),
  music="dread", amb=CHAPEL)
B("Unas semanas después, una novicia que no podía dormir se asomó a la ventana de su celda. Era pasada la medianoche. El huerto estaba blanco de luna.",
  S("cell", cam=((0.6, 0.4, 1.1), (0.65, 0.4, 1.35), "in"), fx=[FL], grade="moon"),
  S("huerto", MOONG, cam=((0.5, 0.5, 1.05), (0.48, 0.55, 1.25), "in"), fx=[FOGL], grade="night", tr="xfade", tl=0.6),
  amb=NIGHT)
B("Y debajo del durazno había una monja de pie. Inmóvil. Mirando hacia la puerta del convento.",
  S("huerto_fog", GHOSTF, cam=((0.48, 0.6, 1.15), (0.48, 0.6, 1.45), "in"), fx=[FOGL, PU(70, 0.06)], grade="cold"),
  sfx=[X("heartbeat", 0.5, -12, dur=6, bpm=85)])
B("La novicia reconoció la forma de sus hombros. La manera de inclinar la cabeza. Era María.",
  S("huerto_ghost", cam=((0.48, 0.55, 1.35), (0.48, 0.55, 1.6), "in"), fx=[FOGL], grade="cold"),
  S("nun_ghost", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=[FOG], grade="cold", tr="xfade", tl=0.6))
B("Corrió a despertar a la abadesa. Cuando volvieron juntas a la ventana, el huerto estaba vacío. Pero en el aire flotaba un olor dulce. A duraznos maduros. Y eso que no era temporada.",
  S("corridor", cam=((0.5, 0.55, 1.1), (0.5, 0.55, 1.4), "in"), fx=[FL], grade="candle"),
  S("huerto_fog", cam=((0.48, 0.55, 1.1), (0.48, 0.55, 1.3), "in"), fx=[FOGL], grade="cold", tr="xfade", tl=0.6),
  sfx=[X("footsteps", 0.3, -10, dur=4)])
B("Desde entonces, la vieron muchas veces. Siempre de noche. Siempre debajo del durazno. A veces caminando entre los arcos del claustro, sin hacer ruido. Y a veces, las que pasaban cerca la escuchaban.",
  S("cloister", L("l_ghost_nun_far", blend="screen", opacity=[0, 0.7], fade_in=2.0, anim=[{"type": "drift", "dx": -0.08, "ease": "linear"}]),
    cam=((0.6, 0.55, 1.1), (0.4, 0.55, 1.2), "linear"), fx=[FOGL], grade="night"),
  S("durazno_close", cam=((0.5, 0.55, 1.2), (0.5, 0.6, 1.4), "in"), fx=[FOG, "ash"], grade="moon", tr="xfade", tl=0.6),
  sfx=[X("whisper", 6.0, -16, dur=5)])
B("¿Por qué no volviste? Yo te esperé… ¿Por qué no volviste?",
  S("nun_ghost", cam=((0.5, 0.42, 1.25), (0.5, 0.42, 1.5), "in"), fx=[FOG, {"type": "flicker", "amp": 0.1}], grade="cold",
    text=[T("¿Por qué no volviste?|", "whisper", 0.3, 4.0)]), **MARG)
B("Las monjas rezaron misas por su alma. Rociaron agua bendita en el huerto. Pero ella siguió ahí. Esperando.",
  S("chapel", cam=((0.5, 0.45, 1.1), (0.5, 0.45, 1.3), "in"), fx=["dust", FL], grade="candle"),
  S("huerto", GHOSTF, cam=((0.5, 0.5, 1.1), (0.48, 0.55, 1.3), "in"), fx=[FOGL], grade="night", tr="xfade", tl=0.8))
B("Y mientras tanto, afuera de los muros, la desgracia alcanzó a los hermanos Ávila.",
  S("huerto_red", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOG], grade="blood"),
  FLASH(), sfx=SCARE)
B("En mil quinientos sesenta y seis, Alonso y Gil fueron acusados de conspirar contra el rey, junto con Martín Cortés, el hijo del conquistador. Los encerraron, los juzgaron en pocos días y los condenaron a muerte.",
  S("palacio" if False else "ciudad_noche", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.25), "in"), fx=[FOGL], grade="night",
    text=[T("Ciudad de México, 1566|la conjura de Martín Cortés", "date", 1.0, 6.0)]),
  S("alonso_red", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=[PU(60, 0.06)], grade="blood", tr="xfade", tl=0.6),
  music="climax")
B("Una mañana de agosto, frente a una multitud, en la Plaza Mayor, los dos hermanos fueron ejecutados. Sus casas fueron derribadas. Y cuentan que en el terreno sembraron sal, para que ahí no volviera a crecer nada.",
  S("scaffold", cam=((0.5, 0.55, 1.05), (0.5, 0.55, 1.25), "in"), fx=["dust", "ash"], grade="sepia"),
  S("solar_sal", cam=((0.4, 0.55, 1.1), (0.6, 0.55, 1.2), "linear"), fx=[FOGL], grade="cold", tr="xfade", tl=0.8),
  sfx=[X("bell", 0.5, -10, freq=140), X("boom", 4.0, -8)])
B("En el convento, dicen, esa noche María no apareció debajo del durazno. Fue la única noche en años.",
  S("huerto_fog", cam=((0.48, 0.55, 1.15), (0.48, 0.55, 1.35), "in"), fx=[FOGL], grade="cold"),
  music="silence", amb=["wind"], pause=1.0)

# ======================================================================== V
B("Pasaron muchos años. Y una noche de lluvia, alguien tocó la puerta del convento de La Concepción.",
  S("convent_gate", cam=((0.6, 0.6, 1.05), (0.62, 0.62, 1.3), "in"), fx=[{"type": "rain", "strength": 0.35}, FOGL], tr="fade", tl=1.0, grade="night",
    text=[T("CAPÍTULO V|El que volvió", "chapter", 0.6, 5.0)]),
  music="mystery", amb=["rain", {"name": "wind", "gain": -10}], sfx=[X("knock", 5.0, -6, times=3)])
B("Era un hombre ya maduro, bien vestido, con el pelo gris en las sienes. Pidió hablar con la hermana María de Ávila.",
  S("arrutia", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.35), "in"), fx=[{"type": "rain", "strength": 0.25}], grade="cold"))
B("La portera contó después que nunca había visto a un hombre tan pálido, ni unas manos que temblaran tanto.",
  S("convent_gate", cam=((0.62, 0.62, 1.3), (0.62, 0.6, 1.5), "in"), fx=[{"type": "rain", "strength": 0.35}], grade="night"))
B("Era Arrutia. Había hecho fortuna. Y al saber que los Ávila estaban muertos, volvió a buscarla. Para cumplir, por fin, lo que le había prometido.",
  S("arrutia_smile", CAND, cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.35), "in"), fx=[FL], grade="candle"),
  music="sad")
B("La monja portera tardó en responder. Luego, del otro lado de la reja, le contó la verdad. La carta. La espera. El durazno.",
  S("reja", cam=((0.5, 0.5, 1.05), (0.55, 0.45, 1.3), "in"), fx=[FL], grade="candle"))
B("Y le entregó lo que habían encontrado debajo de la almohada de María. Su carta. La misma carta fría con la que él se había despedido.",
  S("letter_close", cam=((0.5, 0.5, 1.1), (0.5, 0.5, 1.3), "in"), fx=[FL], grade="candle"),
  sfx=[X("whoosh", 0.5, -16)])
B("Pero al reverso, con la letra temblorosa de María, había tres palabras.",
  S("letter", CAND, cam=((0.4, 0.62, 1.3), (0.4, 0.62, 1.5), "in"), fx=[FL], grade="candle"),
  sfx=[X("heartbeat", 0.5, -14, dur=5, bpm=70)])
B("Yo te esperé.",
  S("letter_close", cam=((0.5, 0.45, 1.3), (0.5, 0.45, 1.45), "in"), fx=[FL], grade="candle",
    text=[T("YO TE ESPERÉ|", "big", 0.2, 3.8)]), voice="ef_dora", speed=0.72, fx="eco", pause=1.0)
B("Arrutia no dijo nada. Pidió, por caridad, que lo dejaran ver el huerto aunque fuera desde la reja. Se lo permitieron.",
  S("arrutia_shock", cam=((0.5, 0.45, 1.15), (0.5, 0.42, 1.4), "in"), fx=["dust"], grade="cold"),
  S("huerto_fog", cam=((0.48, 0.55, 1.05), (0.48, 0.58, 1.25), "in"), fx=[FOGL, {"type": "rain", "strength": 0.25}], grade="cold", tr="xfade", tl=0.6),
  amb=["rain"])
B("Las monjas que estaban en el coro contaron después que, esa noche, escucharon en el huerto la voz de un hombre llorando. Y luego, muy clara, la voz de una mujer.",
  S("chapel", cam=((0.5, 0.45, 1.15), (0.5, 0.45, 1.35), "in"), fx=["dust", FL], grade="candle"),
  sfx=[X("whisper", 4.0, -14, dur=6)], music="dread")
B("Llegaste tarde.",
  S("huerto_ghost", cam=((0.48, 0.55, 1.4), (0.48, 0.55, 1.7), "in"), fx=[FOGL]),
  FLASH(), **MARG, pause=0.8, sfx=SCARE)
B("A la mañana siguiente, la reja estaba abierta. Arrutia no estaba. Nadie lo vio salir. Nunca más se supo de él. Solo encontraron, al pie del durazno, su sombrero empapado… y un durazno maduro, en pleno invierno.",
  S("huerto_dawn", cam=((0.5, 0.55, 1.1), (0.48, 0.6, 1.35), "in"), fx=[FOGL], grade="cold"),
  S("fallen_peaches", cam=((0.5, 0.5, 1.2), (0.5, 0.55, 1.45), "in"), fx=["dust"], grade="cold", tr="xfade", tl=0.8),
  amb=["wind"], sfx=[X("sting", 13.0, -10)], pause=1.0)

# ======================================================================== HISTORIA
B("Ahora, lo que sí es historia.",
  S("book", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2), "in"), fx=["dust"], tr="fade", tl=1.0, grade="sepia",
    text=[T("LO QUE DICE LA HISTORIA|", "chapter", 0.4, 4.0)]),
  music="calm", amb=["room"])
B("El convento de La Concepción existió de verdad. Fue el primer convento de monjas de la Nueva España, un convento de clausura, donde las religiosas hablaban con el mundo solo a través de rejas y del torno. Se fundó a mediados del siglo dieciséis en un terreno que donó el conquistador Andrés de Tapia, con el apoyo del obispo fray Juan de Zumárraga.",
  S("convent_ext", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.25), "in"), fx=["dust"], grade="sepia"),
  S("reja", cam=((0.45, 0.5, 1.1), (0.55, 0.45, 1.3), "linear"), fx=["dust"], grade="sepia", tr="xfade", tl=0.8),
  S("bells", cam=((0.5, 0.45, 1.1), (0.5, 0.4, 1.3), "in"), fx=["dust"], grade="sepia", tr="xfade", tl=0.8))
B("Una inundación en mil seiscientos veintinueve lo dejó casi en ruinas, y fue reconstruido. Las obras terminaron en mil seiscientos cincuenta y cinco. Con las Leyes de Reforma, en mil ochocientos sesenta y uno, las monjas tuvieron que salir y el terreno se dividió.",
  S("cloister", cam=((0.4, 0.55, 1.1), (0.6, 0.55, 1.2), "linear"), fx=["dust"], grade="sepia"))
B("Hoy queda la iglesia, en la calle de Belisario Domínguez, frente a la Plaza de la Concepción, en el Centro Histórico. Del huerto y del durazno no queda nada.",
  S("concepcion_today", cam=((0.5, 0.5, 1.05), (0.45, 0.45, 1.25), "in"), fx=["dust"], grade="night"))
B("Los hermanos Ávila también fueron reales. Alonso de Ávila y su hermano Gil González fueron acusados de conspirar para hacer rey de la Nueva España a Martín Cortés, y fueron decapitados en la Plaza Mayor en agosto de mil quinientos sesenta y seis. Martín Cortés fue enviado preso a España.",
  S("scaffold", cam=((0.5, 0.55, 1.1), (0.5, 0.5, 1.3), "in"), fx=["dust"], grade="sepia",
    text=[T("Alonso y Gil González de Ávila|ejecutados en 1566", "date", 2.0, 8.0)]))
B("Lo de María, en cambio, es leyenda. Los documentos no dicen con claridad que aquella hermana existiera, ni hay registro de Arrutia. La historia pasó de boca en boca y luego a los libros de leyendas de la ciudad, con variantes. En algunas, ella aparece en el huerto. En otras, ronda la esquina de la iglesia… y asusta a las parejas de enamorados.",
  S("book", cam=((0.45, 0.5, 1.15), (0.55, 0.5, 1.35), "linear"), fx=["dust"], grade="sepia"),
  S("nun_sad", cam=((0.5, 0.45, 1.1), (0.5, 0.42, 1.3), "in"), fx=["dust"], grade="moon", tr="xfade", tl=0.8))
B("Una mujer que esperó toda la vida. Y que, según dicen, todavía espera.",
  S("durazno_close", cam=((0.5, 0.45, 1.2), (0.5, 0.5, 1.05), "out"), fx=[FOG], grade="night"), pause=1.0)
B("Y tú, ¿esperarías a alguien toda la vida? ¿Has pasado de noche frente a la iglesia de La Concepción? Te leo en los comentarios.",
  S("title_bg", cam=((0.5, 0.5, 1.05), (0.5, 0.5, 1.2)), fx=[FOG], tr="fade", tl=0.8), music="mystery")
B("En el próximo video entraremos a la Casa de los Azulejos, en el corazón de la Ciudad de México, y conoceremos al hijo al que su padre le dijo que nunca haría casa. Y cómo le respondió.",
  S("casa_avila", cam=((0.5, 0.5, 1.05), (0.5, 0.45, 1.3), "in"), fx=[FOGL], grade="night",
    text=[T("PRÓXIMO VIDEO|La Casa de los Azulejos", "big", 2.0, 7.0)]))
B("Hasta la próxima leyenda. Y si alguna noche pasas por esa calle tomado de la mano de alguien… no le prometas nada que no vayas a cumplir. Ella todavía está escuchando.",
  S("huerto_fog", GHOSTF, cam=((0.48, 0.55, 1.2), (0.48, 0.58, 1.45), "in"), fx=[FOGL], grade="night", out=2.0),
  pause=1.0, music="dread")

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

story = {"title": "La Monja de La Concepción", "voice": "em_alex", "speed": 0.88,
         "sentence_gap": 0.28, "key": "E", "seed": 117, "grade": "night", "vignette": 0.58, "outro": 5.0,
         "music_gain": -15, "amb_gain": -21, "sfx_gain": -9, "beats": BEATS}
json.dump(story, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)

words = 0; out = ["# La Monja de La Concepción — guion\n",
                  "Narración en español (narrador: em_alex; María: ef_dora, con eco cuando es fantasma; Arrutia y Alonso: em_santa).\n"]
WHO = {"ef_dora": "MARÍA: ", "em_santa": "VOZ: "}
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
