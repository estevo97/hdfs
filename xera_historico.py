# -*- coding: utf-8 -*-
"""Xera o histórico de reservas da rede de albergues (E5).

Cada liña: identificador, data da noite, albergue, peregrino, camiño e prezo.
O ficheiro ten que ser grande para que HDFS o parta en varios bloques.

Funciona con Python 2.7 e con Python 3, e xera exactamente o mesmo ficheiro
nas dúas versións (usa o seu propio xerador de números pseudoaleatorios).

Uso:  python xera_historico.py --mb 64 --saida reservas_historico.csv
"""
from __future__ import print_function, unicode_literals, division
import argparse
import io
from datetime import date, timedelta


class Aleatorio(object):
    """Xerador congruencial: a mesma semente dá a mesma secuencia en Python 2 e 3."""

    def __init__(self, semente):
        self.estado = semente

    def enteiro(self, minimo, maximo):
        self.estado = (self.estado * 6364136223846793005 + 1442695040888963407) % (2 ** 64)
        return minimo + (self.estado >> 33) % (maximo - minimo + 1)

    def escoller(self, lista):
        return lista[self.enteiro(0, len(lista) - 1)]


p = argparse.ArgumentParser()
p.add_argument("--mb", type=int, default=64, help="tamaño aproximado en MB")
p.add_argument("--saida", default="reservas_historico.csv")
p.add_argument("--semente", type=int, default=5)
a = p.parse_args()

r = Aleatorio(a.semente)
caminos = ["Francés", "Portugués", "Norte", "Primitivo", "Inglés", "Fisterra"]
prezos = [0, 8, 10, 12, 15, 18]
inicio = date(2020, 1, 1)
obxectivo = a.mb * 1024 * 1024
escritos = 0
n = 0
with io.open(a.saida, "w", encoding="utf-8", newline="\n") as f:
    f.write("reserva_id,noite,albergue_id,peregrino_id,camino,prezo\n")
    while escritos < obxectivo:
        n += 1
        noite = inicio + timedelta(days=r.enteiro(0, 2555))
        rexistro = "{0},{1},{2},{3},{4},{5}\n".format(
            n, noite.isoformat(), r.enteiro(1, 400), r.enteiro(1, 900000),
            r.escoller(caminos), r.escoller(prezos))
        f.write(rexistro)
        escritos += len(rexistro.encode("utf-8"))
print("{0}: {1:.1f} MB, {2} reservas".format(a.saida, escritos / 1024 / 1024, n))
