# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         instrumentLookup.py
# Purpose:      Multi-lingual instrument translation tables
# Authors:      Jose Cabal-Ugaz
#               Mark Gotham
#
# Copyright:    Copyright © 2012, 20 Michael Scott Cuthbert and the music21 Project
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------

import unittest

_DOC_IGNORE_MODULE_OR_PACKAGE = True

# noinspection SpellCheckingInspection
abbreviationToBestName = {
    'a sax': 'alto saxophone',
    'ac b': 'acoustic bass',
    'ac gtr': 'acoustic guitar',
    'acc': 'accordion',
    'accdn': 'accordion',
    'arp': 'harp',
    'b dr': 'bass drum',
    'bcl': 'bass clarinet',
    'b cl': 'bass clarinet',
    'bag': 'bagpipes',
    'bar': 'baritone',
    'bar sax': 'baritone saxophone',
    'bgo dr': 'bongo drums',
    'bj': 'banjo',
    'bjo': 'banjo',
    'bkl': 'bass clarinet',
    'bn': 'bassoon',
    'br': 'viola',
    'bs': 'bassoon',
    'bs cl': 'bass clarinet',
    'bsn': 'bassoon',
    'bssn': 'bassoon',
    'cbsn': 'contrabassoon',
    'c c': 'snare drum',
    'c bsn': 'contrabassoon',
    'cas': 'castanets',
    'casts': 'castanets',
    'cb': 'contrabass',
    'cel': 'celesta',
    'cga dr': 'conga drum',
    'ch': 'choir',
    'cl': 'clarinet',
    'clst': 'celesta',
    'clv': 'clavichord',
    'clvd': 'clavichord',
    'cor': 'horn',
    'cor ang': 'english horn',
    'cr tr': 'bass drum',
    'cwb': 'cowbells',
    'cym': 'crash cymbals',
    'e hn': 'english horn',
    'e gtr': 'electric guitar',
    'e h': 'english horn',
    'elec b': 'electric bass',
    'elec gtr': 'electric guitar',
    'elec org': 'electric organ',
    'eng hn': 'english horn',
    'fag': 'bassoon',
    'fg': 'bassoon',
    'fing cym': 'finger cymbals',
    'fl': 'flute',
    'g c': 'bass drum',
    'glck': 'glockenspiel',
    'glock': 'glockenspiel',
    'glsp': 'glockenspiel',
    'gng': 'gong',
    'gr cassa': 'bass drum',
    'gsp': 'glockenspiel',
    'hb': 'oboe',
    'hmca': 'harmonica',
    'hn': 'horn',
    'hp': 'harp',
    'hpd': 'harpsichord',
    'hpe': 'harp',
    'hpschd': 'harpsichord',
    'hrp': 'harp',
    'k dr': 'timpani',
    'kal': 'kalimba',
    'kas': 'castanets',
    'kl': 'clarinet',
    'mand': 'mandolin',
    'mar': 'marimba',
    'mdln': 'mandolin',
    'mez': 'mezzo-soprano',
    'mezz': 'mezzo-soprano',
    'mz': 'mezzo-soprano',
    'ob': 'oboe',
    'oc': 'ocarina',
    'p fl': 'pan flute',
    'p org': 'pipe organ',
    'pf': 'piano',
    'pfte': 'piano',
    'pic': 'piccolo',
    'picc': 'piccolo',
    'pk': 'timpani',
    'pno': 'piano',
    'rec': 'recorder',
    's': 'soprano',
    's sax': 'soprano saxophone',
    'sand bl': 'sandpaper blocks',
    'sax': 'saxophone',
    'sax a': 'alto saxophone',
    'shk fl': 'shakuhachi',
    'shn': 'shehnai',
    'sit': 'sitar',
    'sn dr': 'snare drum',
    'st dr': 'steel drum',
    't': 'tenor',
    't sax': 'tenor saxophone',
    'tamb': 'tambourine',
    'tamtam': 'gong',
    'tb': 'tuba',
    'tba': 'tuba',
    'tbe': 'trumpet',
    'tbni': 'trombone',
    'temp bl': 'temple block',
    'ten dr': 'tenor drum',
    'tim': 'timbales',
    'timp': 'timpani',
    'tmbn': 'tambourine',
    'tpt': 'trumpet',
    'tr': 'trumpet',
    'trb': 'trombone',
    'trgl': 'triangle',
    'tri': 'triangle',
    'uke': 'ukulele',
    'v': 'voice',
    'va': 'viola',
    'vc': 'violoncello',
    'vcelle': 'violoncello',
    'vcl': 'violoncello',
    'vib': 'vibraphone',
    'vibr': 'vibraphone',
    'vibes': 'vibraphone',
    'vio': 'violin',
    'vl': 'violin',
    'vla': 'viola',
    'vlc': 'violoncello',
    'vln': 'violin',
    'vlon': 'violin',
    'vn': 'violin',
    'vni': 'violin',
    'voc': 'voice',
    'wd bl': 'woodblock',
    'whs': 'whistle',
    'windmachine': 'wind machine',
    'xil': 'xylophone',
    'xyl': 'xylophone'}

# noinspection SpellCheckingInspection
bestNameToInstrumentClass = {
    'accordion': 'Accordion',
    'acoustic bass': 'AcousticBass',
    'acoustic guitar': 'AcousticGuitar',
    'agogo': 'Agogo',
    'alto': 'Alto',
    'alto saxophone': 'AltoSaxophone',
    'bagpipes': 'Bagpipes',
    'banjo': 'Banjo',
    'baritone': 'Baritone',
    'baritone saxophone': 'BaritoneSaxophone',
    'bass': 'Bass',
    'bass clarinet': 'BassClarinet',
    'bass trombone': 'BassTrombone',
    'bass drum': 'BassDrum',
    'bassoon': 'Bassoon',
    'bongo drums': 'BongoDrums',
    'castanets': 'Castanets',
    'celesta': 'Celesta',
    'choir': 'Choir',
    'clarinet': 'Clarinet',
    'clavichord': 'Clavichord',
    'conga drum': 'CongaDrum',
    'contrabass': 'Contrabass',
    'cowbells': 'Cowbells',
    'crash cymbals': 'CrashCymbals',
    'dulcimer': 'Dulcimer',
    'electric bass': 'ElectricBass',
    'electric guitar': 'ElectricGuitar',
    'electric piano': 'ElectricPiano',
    'electric organ': 'ElectricOrgan',
    'english horn': 'EnglishHorn',
    'finger cymbals': 'FingerCymbals',
    'flute': 'Flute',
    'fretless bass': 'FretlessBass',
    'glockenspiel': 'Glockenspiel',
    'gong': 'Gong',
    'handbells': 'Handbells',
    'harmonica': 'Harmonica',
    'harp': 'Harp',
    'harpsichord': 'Harpsichord',
    'hi-hat cymbal': 'HiHatCymbal',
    'horn': 'Horn',
    'kalimba': 'Kalimba',
    'koto': 'Koto',
    'mandolin': 'Mandolin',
    'maracas': 'Maracas',
    'marimba': 'Marimba',
    'mezzo-soprano': 'MezzoSoprano',
    'oboe': 'Oboe',
    'ocarina': 'Ocarina',
    'organ': 'Organ',
    'pan flute': 'PanFlute',
    'piano': 'Piano',
    'piccolo': 'Piccolo',
    'pipe organ': 'PipeOrgan',
    'ratchet': 'Ratchet',
    'recorder': 'Recorder',
    'reed organ': 'ReedOrgan',
    'sandpaper blocks': 'SandpaperBlocks',
    'saxophone': 'Saxophone',
    'shakuhachi': 'Shakuhachi',
    'shamisen': 'Shamisen',
    'shehnai': 'Shehnai',
    'siren': 'Siren',
    'sitar': 'Sitar',
    'sizzle cymbal': 'SizzleCymbal',
    'sleigh bells': 'SleighBells',
    'snare drum': 'SnareDrum',
    'soprano': 'Soprano',
    'soprano saxophone': 'SopranoSaxophone',
    'steel drum': 'SteelDrum',
    'suspended cymbal': 'SuspendedCymbal',
    'taiko': 'Taiko',
    'tam-tam': 'TamTam',
    'tambourine': 'Tambourine',
    'temple block': 'TempleBlock',
    'tenor': 'Tenor',
    'tenor drum': 'TenorDrum',
    'tenor saxophone': 'TenorSaxophone',
    'timbales': 'Timbales',
    'timpani': 'Timpani',
    'tom-tom': 'TomTom',
    'triangle': 'Triangle',
    'trombone': 'Trombone',
    'trumpet': 'Trumpet',
    'tuba': 'Tuba',
    'tubular bells': 'TubularBells',
    'ukulele': 'Ukulele',
    'vibraphone': 'Vibraphone',
    'viola': 'Viola',
    'violin': 'Violin',
    'violoncello': 'Violoncello',
    'voice': 'Vocalist',
    'whip': 'Whip',
    'whistle': 'Whistle',
    'wind machine': 'WindMachine',
    'woodblock': 'Woodblock',
    'xylophone': 'Xylophone',
}

# noinspection SpellCheckingInspection
englishToBestName = {
    'accordion': 'accordion',
    'acoustic bass': 'acoustic bass',
    'acoustic guitar': 'acoustic guitar',
    'agogo': 'agogo',
    'alto': 'alto',
    'alto saxophone': 'alto saxophone',
    'bagpipe': 'bagpipes',
    'bagpipes': 'bagpipes',
    'banjo': 'banjo',
    'baritone': 'baritone',
    'baritone saxophone': 'baritone saxophone',
    'bass': 'bass',
    'bass clarinet': 'bass clarinet',
    'bass drum': 'bass drum',
    'bass trombone': 'bass trombone',
    'bassoon': 'bassoon',
    'bell lira': 'glockenspiel',
    'bell lyre': 'glockenspiel',
    'bongo drums': 'bongo drums',
    'bullseye gong': 'tam-tam',
    'castanets': 'castanets',
    'celesta': 'celesta',
    'celeste': 'celesta',
    'cello': 'violoncello',
    'chau gong': 'tam-tam',
    'chimes': 'glockenspiel',
    'clarinet': 'clarinet',
    'clarinets': 'clarinet',
    'clavichord': 'clavichord',
    'conga drum': 'conga drum',
    'contrabass': 'contrabass',
    'cor anglais': 'english horn',
    'cowbells': 'cowbells',
    'crash cymbals': 'crash cymbals',
    'dulcimer': 'dulcimer',
    'electric bass': 'electric bass',
    'electric guitar': 'electric guitar',
    'electric organ': 'electric organ',
    'english horn': 'english horn',
    'english horns': 'english horn',
    'finger cymbals': 'finger cymbals',
    'flute': 'flute',
    'flutes': 'flute',
    'fretless bass': 'fretless bass',
    'glockenspiel': 'glockenspiel',
    'guitar': 'acoustic guitar',
    'gong': 'gong',
    'handbells': 'handbells',
    'harmonica': 'harmonica',
    'harp': 'harp',
    'harpsichord': 'harpsichord',
    'hi-hat cymbal': 'hi-hat cymbal',
    'horn': 'horn',
    'jingle bells': 'sleigh bells',
    'kalimba': 'kalimba',
    'kettle drums': 'timpani',
    'koto': 'koto',
    'mandolin': 'mandolin',
    'maracas': 'maracas',
    'marimba': 'marimba',
    'marine': 'tambourine',
    'mezzo-soprano': 'mezzo-soprano',
    'mouth organ': 'harmonica',
    'oboe': 'oboe',
    'oboes': 'oboe',
    'ocarina': 'ocarina',
    'octave flute': 'piccolo',
    'orchestra bells': 'glockenspiel',
    'pailas criollas': 'timbales',
    'pan': 'steel drum',
    'pan flute': 'pan flute',
    'pan pipe': 'pan flute',
    'panflute': 'pan flute',
    'panpipes': 'pan flute',
    'piano': 'piano',
    'pianoforte': 'piano',
    'piccolo': 'piccolo',
    'pipe organ': 'pipe organ',
    'ratchet': 'ratchet',
    'rattle': 'ratchet',
    'recorder': 'recorder',
    'reed organ': 'reed organ',
    'sandpaper blocks': 'sandpaper blocks',
    'saxophone': 'saxophone',
    'shakuhachi': 'shakuhachi',
    'shamisen': 'shamisen',
    'shehnai': 'shehnai',
    'siren': 'siren',
    'sitar': 'sitar',
    'sizzle cymbal': 'sizzle cymbal',
    'slapstick': 'whip',
    'sleigh bells': 'sleigh bells',
    'snare drum': 'snare drum',
    'soprano': 'soprano',
    'sopranos': 'soprano',
    'soprano saxophone': 'soprano saxophone',
    'steel drums': 'steel drum',
    'steel drum': 'steel drum',
    'steel pan': 'steel drum',
    'suspended cymbal': 'suspended cymbal',
    'taiko': 'taiko',
    'tam-tam': 'tam-tam',
    'tambourine': 'tambourine',
    'temple block': 'temple block',
    'tenor': 'tenor',
    'tenor drum': 'tenor drum',
    'tenor saxophone': 'tenor saxophone',
    'timbales': 'timbales',
    'timpani': 'timpani',
    'tom-tom': 'tom-tom',
    'transverse flute': 'flute',
    'triangle': 'triangle',
    'trombone': 'trombone',
    'trumpet': 'trumpet',
    'tuba': 'tuba',
    'tubular bells': 'tubular bells',
    'tumbadora': 'conga drum',
    'turkish drum': 'bass drum',
    'ukelele': 'ukulele',
    'ukulele': 'ukulele',
    'vibraphone': 'vibraphone',
    'viola': 'viola',
    'violin': 'violin',
    'violoncello': 'violoncello',
    'voice': 'voice',
    'whip': 'whip',
    'whistle': 'whistle',
    'wind machine': 'wind machine',
    'woodblock': 'woodblock',
    'xylophone': 'xylophone',
    'zills': 'finger cymbals',
    'zils': 'finger cymbals',
}

# noinspection SpellCheckingInspection
frenchToBestName = {
    'accord\xe9on': 'accordion',
    'alto': 'viola',
    'bariton': 'baritone',
    'baryton': 'baritone',
    'bas-dessus': 'soprano',
    'basse': 'bass',
    'basse acoustique': 'acoustic bass',
    'basse fretless': 'fretless bass',
    'basse \xe9lectrique': 'electric bass',
    'basson': 'bassoon',
    'bloc de bois': 'woodblock',
    'blocs de papier de verre': 'sandpaper blocks',
    'bongos': 'bongo drums',
    'caisse claire': 'snare drum',
    'caisse roulante': 'tenor drum',
    'castagnettes': 'castanets',
    'chant': 'voice',
    'chanteur': 'voice',
    'chanteuse': 'voice',
    'claquebois': 'xylophone',
    'clarinette': 'clarinet',
    'clarinette basse': 'bass clarinet',
    'clavecin': 'harpsichord',
    'clavessin': 'harpsichord',
    'clave\xe7in': 'harpsichord',
    'clavicorde': 'clavichord',
    'cloches': 'tubular bells',
    'cloches de vache': 'cowbells',
    'cloches tubolaires': 'tubular bells',
    'cloches tubulaires': 'tubular bells',
    'cloches \xe0 vache': 'cowbells',
    'clochettes': 'handbells',
    'clochettes \u2021 main': 'handbells',
    'conga': 'conga drum',
    'contralto': 'alto',
    'contrebasse': 'contrabass',
    'cor': 'horn',
    'cor anglais': 'english horn',
    'corne': 'horn',
    'cornemuse': 'bagpipes',
    'crash': 'crash cymbals',
    'cr\xe9celle': 'ratchet',
    'cymbale sur tiges': 'sizzle cymbal',
    'cymbale suspendue': 'suspended cymbal',
    'cymbales': 'crash cymbals',
    'cymbales digitales': 'finger cymbals',
    'c\xe9lesta': 'celesta',
    'droite': 'recorder',
    'enregistreur': 'recorder',
    'eoliphone': 'wind machine',
    'fl\xfbte': 'flute',
    'fl\xfbte de pan': 'pan flute',
    'fl\xfbte douce': 'recorder',
    'fl\xfbte droite': 'recorder',
    'fl\xfbte piccolo': 'piccolo',
    'fl\xfbte traversi\xe8re': 'flute',
    'fl\xfbte \xe0 bec': 'recorder',
    'fouet': 'whip',
    'gencerros': 'cowbells',
    'grande fl\xfbte': 'flute',
    'grelots': 'sleigh bells',
    'grosse caisse': 'bass drum',
    'gr\xe9sillement cymbale': 'sizzle cymbal',
    'guitare': 'acoustic guitar',
    'guitarre': 'acoustic guitar',
    'guitare acoustique': 'acoustic guitar',
    'guitare \xe9lectrique': 'electric guitar',
    'guitarre \xe9lectrique': 'electric guitar',
    'harmonica de bois': 'xylophone',
    'harpe': 'harp',
    'hautbois': 'oboe',
    'jeu de timbres': 'glockenspiel',
    'machine \xe0 vent': 'wind machine',
    'mandoline': 'mandolin',
    'orgue \xe0 tuyaux': 'pipe organ',
    'orgue \xe9lectrique': 'electric organ',
    'papier de verre': 'sandpaper blocks',
    'petite fl\xfbte': 'piccolo',
    'pianoforte': 'piano',
    'rochet': 'ratchet',
    'roseau organe': 'reed organ',
    'sagates': 'finger cymbals',
    'sagattes': 'finger cymbals',
    'salut-chapeau cymbale': 'hi-hat cymbal',
    'saxophon alto': 'alto saxophone',
    'saxophone alto': 'alto saxophone',
    'saxophone baryton': 'baritone saxophone',
    'saxophone soprano': 'soprano saxophone',
    'saxophone t\xe9nor': 'tenor saxophone',
    'siffler': 'whistle',
    'sir\xe8ne': 'siren',
    'sonnailles': 'cowbells',
    'syrinx': 'pan flute',
    'taille': 'tenor',
    'tambour': 'snare drum',
    'tambour bata': 'bass drum',
    'tambour congo': 'conga drum',
    "tambour d'acier": 'steel drum',
    'tambour de basque': 'tambourine',
    'tambour en acier': 'steel drum',
    'tambourin': 'tenor drum',
    'tambours bongo': 'bongo drums',
    'temple bloc': 'temple block',
    'timbale': 'timpani',
    'timbales': 'timpani',
    'timbales cr\xe9oles': 'timbales',
    'timbales cubaines': 'timbales',
    'timbales latines': 'timbales',
    'tom': 'tom-tom',
    'trompette': 'trumpet',
    'trombone': 'trombone',
    'trombone basse': 'bass trombone',
    'tumbadora': 'conga drum',
    'tympanon': 'dulcimer',
    'ténor': 'tenor',
    'ténor tambour': 'tenor drum',
    'ukulélé': 'ukulele',
    'violon': 'violin',
    'violoncelle': 'violoncello',
    'voix': 'voice',
    'wood-bloc': 'woodblock',
    'zill': 'finger cymbals',
    '\xc8chelettes': 'xylophone',
    '\xe9oliphone': 'wind machine',
}

# noinspection SpellCheckingInspection
germanToBestName = {
    'aeolophon': 'wind machine',
    'akkordeon': 'accordion',
    'akustik-bass': 'acoustic bass',
    'akustikgitarre': 'acoustic guitar',
    'alt': 'alto',
    'alt-saxophon': 'alto saxophone',
    'altgeige': 'viola',
    'altsaxophon': 'alto saxophone',
    'arpicordo': 'harpsichord',
    'bariton': 'baritone',
    'baritonsaxophon': 'baritone saxophone',
    'bass-drum': 'bass drum',
    'bass-klarinette': 'bass clarinet',
    'bassklarinette': 'bass clarinet',
    'bass-posaune': 'bass trombone',
    'bassposaune': 'bass trombone',
    'becken freih\xe4ngend': 'suspended cymbal',
    'becken gewönlich': 'crash cymbals',
    'becken-paar': 'crash cymbals',
    'beckflöte': 'recorder',
    'blockflöte': 'recorder',
    'bongo-trommeln': 'bongo drums',
    'bongos': 'bongo drums',
    'bratsche': 'viola',
    'cello': 'violoncello',
    'cembalo': 'harpsichord',
    'clavicembalo': 'harpsichord',
    'clavicimbel': 'harpsichord',
    'conga': 'conga drum',
    'conga-trommel': 'conga drum',
    'crash-becken': 'crash cymbals',
    'crashbecken': 'crash cymbals',
    'dreieck': 'triangle',
    'dudelsack': 'bagpipes',
    'e-bass': 'electric bass',
    'e-gitarre': 'electric guitar',
    'elektrische gitarre': 'electric guitar',
    'elektrische orgel': 'electric organ',
    'englisch-horn': 'english horn',
    'englischhorn': 'english horn',
    'fagott': 'bassoon',
    'fagotten': 'bassoon',
    'fingerzimbeln': 'finger cymbals',
    'fl\xf6te': 'flute',
    'geige': 'violin',
    'gitarre': 'acoustic guitar',
    'glocken': 'tubular bells',
    'grosse trommel': 'bass drum',
    'guitarre': 'acoustic guitar',
    'hackbrett': 'dulcimer',
    'hallo-hat-becken': 'hi-hat cymbal',
    'handglocken': 'handbells',
    'handharmonika': 'accordion',
    'harfe': 'harp',
    'harmonium': 'reed organ',
    'herdenglocken': 'cowbells',
    'hirtenfl\xf6te': 'pan flute',
    'hoboe': 'oboe',
    'holzblock': 'woodblock',
    'holzklapper': 'whip',
    'holzschnitt': 'woodblock',
    'h\xe4ngebecken': 'suspended cymbal',
    'h\xe4ngendes becken': 'suspended cymbal',
    'kastagnetten': 'castanets',
    'kesselpauke': 'timpani',
    'kesseltrommel': 'timpani',
    'kielfl\xfcgel': 'harpsichord',
    'klarinette': 'clarinet',
    'klarinetten': 'clarinet',
    'klavichord': 'clavichord',
    'klavier': 'piano',
    'kleine fl\xf6te': 'piccolo',
    'kleine trommel': 'snare drum',
    'knarre': 'ratchet',
    'kontrabass': 'contrabass',
    'kuba-pauken': 'timbales',
    'kuhglocken': 'cowbells',
    'leinentrommel': 'snare drum',
    'lyra': 'glockenspiel',
    'mandoline': 'mandolin',
    'marimbaphon': 'marimba',
    'marschtrommel': 'snare drum',
    'mezzosopran': 'mezzo-soprano',
    'mundharmonika': 'harmonica',
    'nietenbecken': 'sizzle cymbal',
    'oboen': 'oboe',
    'octavfl\xf6te': 'piccolo',
    'okarina': 'ocarina',
    'panfl\xf6te': 'pan flute',
    'papagenopfeife': 'pan flute',
    'pauke': 'timpani',
    'pauken': 'timpani',
    'peitsche': 'whip',
    'pfeifen': 'whistle',
    'pfeifenorgel': 'pipe organ',
    'pferdeschlittenglocken': 'sleigh bells',
    'pianoforte': 'piano',
    'pickelfl\xf6te': 'piccolo',
    'pikkolo': 'piccolo',
    'pikkolofl\xf6te': 'piccolo',
    'posaune': 'trombone',
    'querfl\xf6te': 'flute',
    'ratsche': 'ratchet',
    'rohrenglocke': 'tubular bells',
    'rollschellen': 'sleigh bells',
    'r\xf6hrenglocken': 'tubular bells',
    'r\xfchrtrommel': 'tenor drum',
    'sandbl\xf6cke': 'sandpaper blocks',
    'sandpapier': 'sandpaper blocks',
    'sandpapier bl\xf6cke': 'sandpaper blocks',
    'saxophon': 'saxophone',
    'schellen': 'sleigh bells',
    'schellentrommel': 'tambourine',
    'schnabelfl\xf6te': 'recorder',
    'schnarre': 'ratchet',
    'schnarrtrommel': 'snare drum',
    'sirene': 'siren',
    'snare-drum': 'snare drum',
    'sopran': 'soprano',
    'sopran-saxophon': 'soprano saxophone',
    'sopransaxophon': 'soprano saxophone',
    'stahltrommel': 'steel drum',
    'steeldrum': 'steel drum',
    'singstimme': 'voice',
    'stimme': 'voice',
    'strohfiedel': 'xylophone',
    'syrinx': 'pan flute',
    'tambourin': 'tambourine',
    'tamburin': 'tambourine',
    'tamtam': 'tam-tam',
    'tempel-block': 'temple block',
    'tenor-saxophon': 'tenor saxophone',
    'tenorsaxophon': 'tenor saxophone',
    'tenortrommel': 'tenor drum',
    'tom': 'tom-tom',
    'tom tom': 'tom-tom',
    'triangel': 'triangle',
    'trompete': 'trumpet',
    'tumba': 'conga drum',
    't\xfcrkisches h\xe4ngebecken': 'suspended cymbal',
    'ventilhorn': 'horn',
    'viehschellen': 'cowbells',
    'viole': 'viola',
    'violine': 'violin',
    'violoncell': 'violoncello',
    'windmaschine': 'wind machine',
    'wirbeltrommel': 'tenor drum',
    'xylophon': 'xylophone',
    'ziehharmonika': 'accordion',
}

# noinspection SpellCheckingInspection
italianToBestName = {
    'a becco': 'recorder',
    'armonica': 'harmonica',
    'armonica a bocca': 'harmonica',
    'arpa': 'harp',
    'arpe': 'harp',
    'arpicordo': 'harpsichord',
    'baritono': 'baritone',
    'basso': 'bass',
    'basso elettrico': 'electric bass',
    'blocchi di carta vetrata': 'sandpaper blocks',
    'blocco di legno': 'woodblock',
    'blocco di legno cinese': 'woodblock',
    'bonghi': 'bongo drums',
    'bongos': 'bongo drums',
    'campanacci': 'cowbells',
    'campane': 'tubular bells',
    'campane tubolari': 'tubular bells',
    'campane tubulari': 'tubular bells',
    'campanelli': 'glockenspiel',
    'campanelli a mano': 'handbells',
    'campanelli da mucca': 'cowbells',
    'campanelli di vacca': 'cowbells',
    "canna d'organo": 'reed organ',
    'canna d&#39;organo': 'reed organ',
    'canto': 'voice',
    'carta vetrata': 'sandpaper blocks',
    'cassa': 'bass drum',
    'cassa chiara': 'snare drum',
    'cassa rullante': 'tenor drum',
    'cassetina': 'woodblock',
    'castagnette': 'castanets',
    'celeste': 'celesta',
    'cello': 'violoncello',
    'cembalo': 'harpsichord',
    'ceppi di carta vetro': 'sandpaper blocks',
    'cestello in acciaio': 'steel drum',
    'chitarra': 'acoustic guitar',
    'chitarra acustica': 'acoustic guitar',
    'chitarra elettrica': 'electric guitar',
    'cimbalini': 'finger cymbals',
    'cimbalo': 'harpsichord',
    'cinelli': 'crash cymbals',
    'clarinetti': 'clarinet',
    'clarinetti bassi': 'clarinet',
    'clarinetto': 'clarinet',
    'clarinetto basso': 'bass clarinet',
    'clarino': 'trumpet',
    'clavicembalo': 'harpsichord',
    'clavicordo': 'clavichord',
    'conga': 'conga drum',
    'contrabbasso': 'contrabass',
    'contralto': 'alto',
    'cornamuse': 'bagpipes',
    'corno': 'horn',
    'corno inglese': 'english horn',
    'cricchetto': 'ratchet',
    'dita piatti': 'finger cymbals',
    'dritto': 'recorder',
    'eolifono': 'wind machine',
    'fagotto': 'bassoon',
    'fisarmonica': 'accordion',
    'fischio': 'whistle',
    'flauto': 'flute',
    'flauto a becco': 'recorder',
    'flauto di pan': 'pan flute',
    'flauto diritto': 'recorder',
    'flauto dolce': 'recorder',
    'flauto dritto': 'recorder',
    'flauto piccolo': 'piccolo',
    'flauto traverso': 'flute',
    'frusta': 'whip',
    'gigelira': 'xylophone',
    'gran cassa': 'bass drum',
    'grancassa': 'bass drum',
    'hi-hat piatto': 'hi-hat cymbal',
    'macchina del vento': 'wind machine',
    'machina a venti': 'wind machine',
    'mandolino': 'mandolin',
    'metallofono': 'glockenspiel',
    'mezzosoprano': 'mezzo-soprano',
    'nacchere': 'castanets',
    'organi': 'organ',
    'organo': 'pipe organ',
    'organo a canne': 'pipe organ',
    'organo elettrico': 'electric organ',
    'ottavino': 'piccolo',
    'pianoforte': 'piano',
    'piatti': 'crash cymbals',
    'piatti di crash': 'crash cymbals',
    'piatto chiodati': 'sizzle cymbal',
    'piatto sospeso': 'suspended cymbal',
    'raganella': 'ratchet',
    'registratore': 'recorder',
    'rullante': 'snare drum',
    'salterio': 'dulcimer',
    'sassofono': 'saxophone',
    'sassofono alto': 'alto saxophone',
    'sassofono baritono': 'baritone saxophone',
    'sassofono contralto': 'alto saxophone',
    'sassofono soprano': 'soprano saxophone',
    'sassofono tenore': 'tenor saxophone',
    'sax': 'saxophone',
    'saxofono': 'saxophone',
    'saxofono alto': 'alto saxophone',
    'saxofono baritono': 'baritone saxophone',
    'saxofono contralto': 'alto saxophone',
    'saxofono soprano': 'soprano saxophone',
    'saxofono tenore': 'tenor saxophone',
    'sfrigolio piatto': 'sizzle cymbal',
    'silofono': 'xylophone',
    'sirena': 'siren',
    'sirena a mano': 'siren',
    'siringa': 'pan flute',
    'sonagli': 'sleigh bells',
    'sonagliera': 'sleigh bells',
    'tamborone': 'bass drum',
    'tamburello': 'tambourine',
    'tamburi bongo': 'bongo drums',
    'tamburino': 'tambourine',
    'tamburo basco': 'tambourine',
    "tamburo d'acciaio": 'steel drum',
    'tamburo grande': 'bass drum',
    'tamburo grosso': 'bass drum',
    'tamburo militare': 'snare drum',
    'tamburo rullante': 'tenor drum',
    'tamtam': 'tom-tom',
    'tempio di blocco': 'temple block',
    'tenore': 'tenor',
    'timbales latinoamericani': 'timbales',
    'timballi': 'timpani',
    'timballo': 'timpani',
    'timpanetti': 'timbales',
    'timpano': 'timpani',
    'triangolo': 'triangle',
    'tromba': 'trumpet',
    'trombone': 'trombone',
    'trombone basso': 'bass trombone',
    'tumba': 'conga drum',
    'tympani': 'timpani',
    'violino': 'violin',
    'voca': 'voice',
    'voce': 'voice',
    'xilifono': 'xylophone',
    'xilofono': 'xylophone',
    'xilografia': 'woodblock',
}

pitchFullNameToName = {
    'a': 'a',
    'a-double-flat': 'a--',
    'a-double-sharp': 'a##',
    'a-flat': 'a-',
    'a-sharp': 'a#',
    'ab': 'a-',
    'abb': 'a--',
    'b': 'b',
    'b-double-flat': 'b--',
    'b-double-sharp': 'b##',
    'b-flat': 'b-',
    'b-sharp': 'b#',
    'bb': 'b-',
    'bbb': 'b--',
    'c': 'c',
    'c-double-flat': 'c--',
    'c-double-sharp': 'c##',
    'c-flat': 'c-',
    'c-sharp': 'c#',
    'cb': 'c-',
    'cbb': 'c--',
    'd': 'd',
    'd-double-flat': 'd--',
    'd-double-sharp': 'd##',
    'd-flat': 'd-',
    'd-sharp': 'd#',
    'db': 'd-',
    'dbb': 'd--',
    'e': 'e',
    'e-double-flat': 'e--',
    'e-double-sharp': 'e##',
    'e-flat': 'e-',
    'e-sharp': 'e#',
    'eb': 'e-',
    'ebb': 'e--',
    'f': 'f',
    'f-double-flat': 'f--',
    'f-double-sharp': 'f##',
    'f-flat': 'f-',
    'f-sharp': 'f#',
    'fb': 'f-',
    'fbb': 'f--',
    'g': 'g',
    'g-double-flat': 'g--',
    'g-double-sharp': 'g##',
    'g-flat': 'g-',
    'g-sharp': 'g#',
    'gb': 'g-',
    'gbb': 'g--',
}

# noinspection SpellCheckingInspection
# TODO: Russian expert to add Cyrillic names
russianToBestName = {
    "al't": 'alto',
    'angliiskii rozhok': 'english horn',
    'arfa': 'harp',
    'bariton': 'baritone',
    'bas': 'bass',
    'bass-klarnet': 'bass clarinet',
    'blokfleita': 'recorder',
    "bol'shoi baraban": 'bass drum',
    'chelesta': 'celesta',
    'chembalo': 'harpsichord',
    'fagot': 'bassoon',
    'fleita': 'flute',
    'fleita pikkolo': 'piccolo',
    "fortep'iano": 'piano',
    'frantsuzskii baraban': 'snare drum',
    'goboi': 'oboe',
    'golos': 'voice',
    'gorn': 'horn',
    'klarnet': 'clarinet',
    'klavesin': 'harpsichord',
    'klavikord': 'clavichord',
    "kolokol'chiki": 'glockenspiel',
    "kontral'to": 'alto',
    'ksilofon': 'xylophone',
    'litavra': 'timpani',
    'malaia fleita': 'piccolo',
    'mandolina': 'mandolin',
    'pikkolo': 'piccolo',
    'rog': 'horn',
    'rozhok': 'horn',
    'saksofon': 'saxophone',
    'skripka': 'violin',
    'trombon': 'trombone',
    'truba': 'trumpet',
    'tsilindricheskii baraban': 'tenor drum',
    'tsimbaly': 'dulcimer',
    "violonchel'": 'violoncello',
}

spanishToBestName = {
    'acorde\xf3n': 'accordion',
    'arm\xf3nica de boca': 'harmonica',
    'arpa': 'harp',
    'atabal': 'timpani',
    'bajo': 'bass',
    'bajo ac\xfastico': 'acoustic bass',
    'bajo el\xe9ctrico': 'electric bass',
    'bar\xedtono': 'baritone',
    'bloques de madera': 'woodblock',
    'bloques de papel de lija': 'sandpaper blocks',
    'bombo': 'bass drum',
    'bongo tambores': 'bongo drums',
    'bongos': 'bongo drums',
    'caja china': 'woodblock',
    'caja clara': 'snare drum',
    'caja redoblante': 'tenor drum',
    'caja rodante': 'tenor drum',
    'campanas': 'tubular bells',
    'campanas de mano': 'handbells',
    'campanas tubulares': 'tubular bells',
    'campanos': 'cowbells',
    'campan\xf3logo': 'glockenspiel',
    'carraca': 'ratchet',
    'cascabels': 'sleigh bells',
    'casta\xf1uelas': 'castanets',
    'ca\xf1a de \xf3rganos': 'reed organ',
    'cello': 'violoncello',
    'cencerros': 'cowbells',
    'chelo': 'violoncello',
    'chinchines': 'finger cymbals',
    'chisporroteo de platillos': 'sizzle cymbal',
    'clarinete': 'clarinet',
    'clarinete bajo': 'bass clarinet',
    'clave': 'harpsichord',
    'clavec\xe9mbalo': 'harpsichord',
    'clavec\xedn': 'harpsichord',
    'clavicordio': 'clavichord',
    'clavic\xe9mbalo': 'harpsichord',
    'clavic\xedmbalo': 'harpsichord',
    'con tensores': 'snare drum',
    'conga': 'conga drum',
    'congas': 'conga drum',
    'contrabajo': 'contrabass',
    'contralto': 'alto',
    'corneta inglesa': 'english horn',
    'corno': 'english horn',
    'corno franc\xe9s': 'horn',
    'corno ingl\xe9s': 'english horn',
    'cr\xf3talos': 'finger cymbals',
    'cuerno': 'horn',
    'cuerno ingl\xe9s': 'english horn',
    'c\xe9mbalo': 'harpsichord',
    'de pico': 'recorder',
    'de timbres': 'glockenspiel',
    'dulce': 'recorder',
    'dulcema': 'dulcimer',
    'el tenor del tambor': 'tenor drum',
    'el viento de la m\xe1quina': 'wind machine',
    'fagot': 'bassoon',
    'flauta': 'flute',
    'flauta de boehm': 'flute',
    'flauta de concierto': 'flute',
    'flauta de pan': 'pan flute',
    'flauta de pico': 'recorder',
    'flauta dulce': 'recorder',
    'flauta piccolo': 'piccolo',
    'flauta recta': 'recorder',
    'flauta traversa': 'flute',
    'flauta travesera': 'flute',
    'flautas de pan': 'pan flute',
    'flaut\xedn': 'piccolo',
    'fretless': 'fretless bass',
    'gaita': 'bagpipes',
    'grabadora': 'recorder',
    'gran caja': 'bass drum',
    'gravic\xe9mbalo': 'harpsichord',
    'guitarra': 'acoustic guitar',
    'guitarra ac\xfastica': 'acoustic guitar',
    'guitarra el\xe9ctrica': 'electric guitar',
    'harm\xf3nica': 'harmonica',
    'juego': 'glockenspiel',
    'juego de timbres': 'glockenspiel',
    'liro': 'glockenspiel',
    'l\xe1tigo': 'whip',
    'mandolina': 'mandolin',
    'matraca': 'ratchet',
    'mezzosoprano': 'mezzo-soprano',
    'm\xe1quina de viento': 'wind machine',
    'octavillo': 'piccolo',
    'ottavino': 'piccolo',
    'pailas criollas': 'timbales',
    'pandereta': 'tambourine',
    'papel de lija': 'sandpaper blocks',
    'platillo hi-hat': 'hi-hat cymbal',
    'platillo sizzle': 'sizzle cymbal',
    'platillo suspendido': 'suspended cymbal',
    'platillos crash': 'crash cymbals',
    'platillos de choque': 'crash cymbals',
    'platillos suspendidos': 'suspended cymbal',
    'redoblante': 'snare drum',
    'saxo soprano': 'soprano saxophone',
    'saxo tenor': 'tenor saxophone',
    'saxof\xf3n': 'saxophone',
    'saxof\xf3n alto': 'alto saxophone',
    'saxof\xf3n del bar\xedtono': 'baritone saxophone',
    'saxof\xf3no': 'saxophone',
    'saxof\xf3no alto': 'alto saxophone',
    'saxof\xf3no bar\xedtono': 'baritone saxophone',
    'saxof\xf3no soprano': 'soprano saxophone',
    'saxof\xf3no tenor': 'tenor saxophone',
    'sax\xf3fono': 'saxophone',
    'silbar': 'whistle',
    'sirena': 'siren',
    'siringa': 'pan flute',
    'tambor afinable': 'snare drum',
    'tambor de acero': 'steel drum',
    'tambor de mano': 'tambourine',
    'tambor mayor': 'tenor drum',
    'tambor met\xe1lico de trinidad y tobago': 'steel drum',
    'tambor militar peque\xf1o': 'snare drum',
    'templo de bloque': 'temple block',
    'timbal': 'timpani',
    'timbales': 'timpani',
    'timbals': 'timpani',
    'tomtom': 'tom-tom',
    'trinquete': 'ratchet',
    'tri\xe1ngulo': 'triangle',
    'tromb\xf3n': 'trombone',
    'trompa': 'horn',
    'trompeta': 'trumpet',
    'tumbadora': 'conga drum',
    't\xedmpanos': 'timpani',
    'ukelele': 'ukulele',
    'violoncelo': 'violoncello',
    'violonchelo': 'violoncello',
    'viol\xedn': 'violin',
    'voz': 'voice',
    'xilof\xf3n': 'xylophone',
    'xilof\xf3no': 'xylophone',
    'xil\xf3fono': 'xylophone',
    'zampo\xf1as': 'pan flute',
    '\xf3rgano de': 'glockenspiel',
    '\xf3rgano de campanas': 'glockenspiel',
    '\xf3rgano de tubos': 'pipe organ',
    '\xf3rgano el\xe9ctrico': 'electric organ'}

transliteration = {
    'accordeon': 'accord\xe9on',
    'acordeon': 'acorde\xf3n',
    'armonica de boca': 'arm\xf3nica de boca',
    'bajo acustico': 'bajo ac\xfastico',
    'bajo electrico': 'bajo el\xe9ctrico',
    'baritono': 'bar\xedtono',
    'basse electrique': 'basse \xe9lectrique',
    'becken freihangend': 'becken freih\xe4ngend',
    'becken gewonlich': 'becken gew\xf6nlich',
    'beckflote': 'beckfl\xf6te',
    'blockflote': 'blockfl\xf6te',
    'campanologo': 'campan\xf3logo',
    'cana de organos': 'ca\xf1a de \xf3rganos',
    'castanuelas': 'casta\xf1uelas',
    'celesta': 'c\xe9lesta',
    'cembalo': 'c\xe9mbalo',
    'clavecembalo': 'clavec\xe9mbalo',
    'clavecin': 'clavec\xedn',
    'clavicembalo': 'clavic\xe9mbalo',
    'clavicimbalo': 'clavic\xedmbalo',
    'cloches a vache': 'cloches \xe0 vache',
    'clochettes ++ main': 'clochettes \u2021 main',
    'corno frances': 'corno franc\xe9s',
    'corno ingles': 'corno ingl\xe9s',
    'crecelle': 'cr\xe9celle',
    'crotalos': 'cr\xf3talos',
    'cuerno ingles': 'cuerno ingl\xe9s',
    'echelettes': '\xc8chelettes',
    'el viento de la maquina': 'el viento de la m\xe1quina',
    'eoliphone': '\xe9oliphone',
    'flautin': 'flaut\xedn',
    'flote': 'fl\xf6te',
    'flute': 'fl\xfbte',
    'flute a bec': 'fl\xfbte \xe0 bec',
    'flute de pan': 'fl\xfbte de pan',
    'flute douce': 'fl\xfbte douce',
    'flute droite': 'fl\xfbte droite',
    'flute piccolo': 'fl\xfbte piccolo',
    'flute traversiere': 'fl\xfbte traversi\xe8re',
    'grande flute': 'grande fl\xfbte',
    'gravicembalo': 'gravic\xe9mbalo',
    'gresillement cymbale': 'gr\xe9sillement cymbale',
    'guitare electrique': 'guitare \xe9lectrique',
    'guitarra acustica': 'guitarra ac\xfastica',
    'guitarra electrica': 'guitarra el\xe9ctrica',
    'guitarre electrique': 'guitarre \xe9lectrique',
    'hangebecken': 'h\xe4ngebecken',
    'hangendes becken': 'h\xe4ngendes becken',
    'harmonica': 'harm\xf3nica',
    'hirtenflote': 'hirtenfl\xf6te',
    'kielflugel': 'kielfl\xfcgel',
    'kleine flote': 'kleine fl\xf6te',
    'latigo': 'l\xe1tigo',
    'machine a vent': 'machine \xe0 vent',
    'maquina de viento': 'm\xe1quina de viento',
    'octavflote': 'octavfl\xf6te',
    'organo de': '\xf3rgano de',
    'organo de campanas': '\xf3rgano de campanas',
    'organo de tubos': '\xf3rgano de tubos',
    'organo electrico': '\xf3rgano el\xe9ctrico',
    'orgue a tuyaux': 'orgue \xe0 tuyaux',
    'orgue electrique': 'orgue \xe9lectrique',
    'panflote': 'panfl\xf6te',
    'petite flute': 'petite fl\xfbte',
    'pickelflote': 'pickelfl\xf6te',
    'pikkoloflote': 'pikkolofl\xf6te',
    'querflote': 'querfl\xf6te',
    'rohrenglocken': 'r\xf6hrenglocken',
    'ruhrtrommel': 'r\xfchrtrommel',
    'sandblocke': 'sandbl\xf6cke',
    'sandpapier blocke': 'sandpapier bl\xf6cke',
    'saxofon': 'saxof\xf3n',
    'saxofon alto': 'saxof\xf3n alto',
    'saxofon del baritono': 'saxof\xf3n del bar\xedtono',
    'saxofono': 'saxof\xf3no',
    'saxofono alto': 'saxof\xf3no alto',
    'saxofono baritono': 'saxof\xf3no bar\xedtono',
    'saxofono soprano': 'saxof\xf3no soprano',
    'saxofono tenor': 'saxof\xf3no tenor',
    'saxophone tenor': 'saxophone t\xe9nor',
    'schnabelflote': 'schnabelfl\xf6te',
    'sirene': 'sir\xe8ne',
    'tambor metalico de trinidad y tobago': 'tambor met\xe1lico de trinidad y tobago',
    'tambor militar pequeno': 'tambor militar peque\xf1o',
    'tenor': 't\xe9nor',
    'tenor tambour': 't\xe9nor tambour',
    'timbales creoles': 'timbales cr\xe9oles',
    'timpanos': 't\xedmpanos',
    'triangulo': 'tri\xe1ngulo',
    'trombon': 'tromb\xf3n',
    'turkisches hangebecken': 't\xfcrkisches h\xe4ngebecken',
    'ukulele': 'ukul\xe9l\xe9',
    'violin': 'viol\xedn',
    'xilofon': 'xilof\xf3n',
    'xilofono': 'xil\xf3fono',
    'zamponas': 'zampo\xf1as',
}

transposition = {
    'clarinet': {'a': 'm-3',
                 'alto': 'M-6',
                 'b': 'M-2',  # German, much more common than b-natural
                 'b-': 'M-2',
                 'b- bass': 'M-9',
                 'b- contrabass': 'M-16',
                 'bass': 'M-9',
                 'd': 'M2',
                 'e-': 'm3',
                 'e- alto': 'M-6',
                 'e- contrabass': 'M-13',
                 'a-': 'm7',
                 'h': 'm-2',
                 'b-natural': 'm-2',
                 },
    'horn': {'a': 'm-3',
             'c': 'P-8',
             'd': 'm-7',
             'e': 'm-6',
             'e-': 'M-6',
             'english': 'P-5',  # this is how it works...
             'f': 'P-5',
             'g': 'P-4',
             },
    'trumpet': {'a': 'm-3',
                'b': 'M-2',  # German, much more common than b-natural
                'b-': 'M-2',
                'b- bass': 'M-9',
                'c': 'P1',
                'c bass': 'P-8',
                'cornet': 'M-2',
                'd': 'M2',
                'd bass': 'm-7',
                'e-': 'm3',
                'e- bass': 'M-6',
                'h': 'm-2',
                'b-natural': 'm-2',
                'f': 'P4',
                'flugelhorn': 'M-2',
                }
}

# ------------------------------------------------------------------------------

# Make allToBestName dict anew to ensure consistency with constituent parts

allToBestName = {
    **frenchToBestName,
    **germanToBestName,
    **italianToBestName,
    **russianToBestName,
    **spanishToBestName,
    **abbreviationToBestName,
    **englishToBestName,  # leave at end since should overwrite any others.
}

# Special case of transliteration via the relevant language
for _key in transliteration:
    allToBestName[_key] = allToBestName[transliteration[_key]]

del _key

# ------------------------------------------------------------------------------

class Test(unittest.TestCase):

    def testAllToBestNamePopulated(self):
        '''
        Test that the allToBestName dict includes all of the keys from the constituent dicts.

        Note: No length test due to duplicate entries
        (i.e. allToBestName is smaller than the sum of its parts).
        '''
        for eachDict in [abbreviationToBestName,
                         englishToBestName,
                         frenchToBestName,
                         germanToBestName,
                         italianToBestName,
                         russianToBestName,
                         spanishToBestName,
                         transliteration]:

            for key in eachDict:
                self.assertIn(key, allToBestName)

    def testAllToBestNameExamples(self):
        '''
        Test an example from each constituent dict that makes up allToBestName.
        '''
        abbreviationTest = 'a sax'
        self.assertEqual(allToBestName[abbreviationTest], abbreviationToBestName[abbreviationTest])

        englishTest = 'accordion'
        self.assertEqual(allToBestName[englishTest], englishToBestName[englishTest])

        frenchTest = 'accord\xe9on'
        self.assertEqual(allToBestName[frenchTest], frenchToBestName[frenchTest])

        germanTest = 'aeolophon'
        self.assertEqual(allToBestName[germanTest], germanToBestName[germanTest])

        italianTest = 'a becco'
        self.assertEqual(allToBestName[italianTest], italianToBestName[italianTest])

        russianTest = "al't"
        self.assertEqual(allToBestName[russianTest], russianToBestName[russianTest])

        spanishTest = 'acorde\xf3n'
        self.assertEqual(allToBestName[spanishTest], spanishToBestName[spanishTest])


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    import music21

    music21.mainTest(Test)