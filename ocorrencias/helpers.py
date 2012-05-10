#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Se você quiser "desacentuar" strings em ISO 8859-1, basta trocar a
# linha acima por "coding: iso-8859-1" e salvar o código-fonte com o
# encoding citado.
from django.db import connection


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


_table = {
    "á": "a", "à": "a", "â": "a", "ä": "a", "ã": "a", "å": "a",
    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "í": "i", "ì": "i", "î": "i", "ï": "i",
    "ó": "o", "ò": "o", "ô": "o", "ö": "o", "õ": "o", "ø": "o",
    "ú": "u", "ù": "u", "û": "u", "ü": "u",
    "ñ": "n", "ç": "c",
    "Á": "A", "À": "A", "Â": "A", "Ä": "A", "Ã": "A", "Å": "A",
    "É": "E", "È": "E", "Ê": "E", "Ë": "E",
    "Í": "I", "Ì": "I", "Î": "I", "Ï": "I",
    "Ó": "O", "Ò": "O", "Ô": "O", "Ö": "O", "Õ": "O", "Ø": "O",
    "Ú": "U", "Ù": "U", "Û": "U", "Ü": "U",
    "Ñ": "N", "Ç": "C",
    "ß": "ss", "Þ": "d", "æ": "ae"
}


def asciize(text):
    substitute = [
        (u'ç', 'c'),
        (u'ã', 'a'),
        (u'á', 'a'),
        (u'à', 'a'),
        (u'â', 'a'),
        (u'ä', 'a'),
        (u'é', 'e'),
        (u'è', 'e'),
        (u'ê', 'e'),
        (u'ë', 'e'),
        (u'ó', 'o'),
        (u'ò', 'o'),
        (u'ô', 'o'),
        (u'õ', 'o'),
        (u'ö', 'o'),
        (u'í', 'i'),
        (u'ì', 'i'),
        (u'î', 'i'),
        (u'ï', 'i'),
        (u'ú', 'u'),
        (u'ù', 'u'),
        (u'û', 'u'),
        (u'ü', 'u'),
    ]

    for t, f in substitute:
        text = text.replace(t, f)
        text = text.replace(t.upper(), f.upper())

    return text
