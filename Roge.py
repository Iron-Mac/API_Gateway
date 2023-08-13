import tensorflow as tf
import tensorflow_text as text


def roge(phrase1, phrase2):
    hypo = []
    ref = []
    phrase11 = phrase1.split(".")
    phrase22 = phrase2.split(".")
    for x in phrase11:
        hypo.append(x.split())
    for y in phrase22:
        ref.append(y.split())
    hypotheses = tf.ragged.constant(hypo)
    references = tf.ragged.constant(ref)
    result = text.metrics.rouge_l(hypotheses, references, alpha=1)
    fmeasure = f'F-Measure (alpha=1): {result.f_measure} '
    pmeasure = f'F-Measure (alpha=1): {result.p_measure} '
    rmeasure = f'F-Measure (alpha=1): {result.r_measure} '
    res = []
    res.append(fmeasure)
    res.append(pmeasure)
    res.append(rmeasure)
    return res 