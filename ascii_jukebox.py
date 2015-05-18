#!/usr/bin/env python
""" ascii_jukebox.py - make a lot of noise

Usage:
    ascii_jukebox.py [-m=INT] [-d=CNT] [-b=BPMS ...] [-o=DIR] [SONGS ...]
    ascii_jukebox.py [-l|--list]

Options:
    -b, --bpm=<BPMS>        [multiple] bpm values
    -o, --output=<DIR>      write songs to DIR [default: out]
    -m, --metronome=<INT>   insert metronome with INT ticks
    -d, --dondokos=<CNT>    insert backbeat dondokos
    -l, --list              list available songs
"""

from pydub import AudioSegment
from ascii_drumming import play
from ascii_drummer import read_pattern
from glob import glob
import os

def get_song_list():
    lst = glob(os.sep.join(['songs', '*','*.song']))
    lst = sorted(set([x.split(os.sep)[1] for x in lst]))
    return lst

song_list = get_song_list()

def list_songs():
    global song_list
    for cnt, name in enumerate(song_list):
        print('Song Nr. %d - %s' % (cnt, name))

def read_song(stream):
    for line in stream.readlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        yield line.replace(' ', '')

PADDING = 8

def interpret(file, bpm, metronome, dondokos):
    dirstack = file.split(os.sep)[:-1]
    song = []
    now = 0

    def play_voice(name, bpm, metronome, dondokos):
        global PADDING
        drum_file = os.sep.join(dirstack + [name]) + '.drum'
        pattern = read_pattern(open(drum_file))
        voice = play(pattern, bpm, metronome, dondokos)
        beats = (((len(pattern) + PADDING - 1) / PADDING) * PADDING) / 4
        beats = len(pattern) / 4
        return voice, beats

    for line in read_song(open(file)):

        if ':' in line:
            key, value = line.split(':')
            if key == 'bpm':
                bpm += int(value)
            elif key == 'metronome':
                try:
                    metronome = int(value)
                except:
                    metronome = None
            elif key == 'dondokos':
                try:
                    dondokos = int(value)
                except:
                    dondokos = None
            else:
                print('bad key/value pair:', [key, value])
            continue

        if '|' in line:
            voices = []
            beats = 0
            for name in [n.strip() for n in line.split('|')]:
                print(name, end='', flush=True)
                v, b = play_voice(name, bpm, metronome, dondokos)
                voices.append(v)
                beats = max(beats, b)
            voice = AudioSegment.silent(duration=(60000.0 / bpm)*beats+2000)
            for v in voices:
                voice = voice.overlay(v)

        else:
            voice, beats = play_voice(line, bpm, metronome, dondokos)

        song.append((now, voice))
        time = beats * (60000.0 / bpm)
        now += time


    master_mix = AudioSegment.silent(duration=now+2000)
    for when, voice in song:
        master_mix = master_mix.overlay(voice, position=when)

    return master_mix

def do_song(name, bpm, metronome, dondokos):

    song_file = glob(os.sep.join(['songs', name, '*.song']))[0]
    print(song_file)
    song = interpret(song_file, bpm, metronome, dondokos)

    metro = '' if not metronome else '_metronome'
    ddks = '' if not dondokos else '_%dddks' % dondokos

    out_file = os.sep.join([args['--output'], name, '%s_-_%sbpm%s%s.ogg' % (name, bpm, metro, ddks)])
    print('Delivering: %s' % out_file)
    song.export(out_file, 'ogg')


if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)

    if args['--list']:
        list_songs()
        import sys
        sys.exit()

    print(args)

    if args['--metronome'] is not None:
        metronome = int(args['--metronome'])
    else:
        metronome = None

    if args['--dondokos'] is not None:
        dondokos = int(args['--dondokos'])
    else:
        dondokos = None

    bpms = [ int(x) for x in args['--bpm'] ]
    songs = [ int(x) for x in args['SONGS']]

    print('Songs to play:', ', '.join(args['SONGS']))

    for bpm in bpms:
        for number in songs:
            song_name = song_list[number]
            try:
                os.mkdir(args['--output'] + os.sep + song_name)
            except:
                pass

            do_song(song_name, bpm, metronome, dondokos)

            if metronome:
                do_song(song_name, bpm, None, dondokos)
            if dondokos:
                do_song(song_name, bpm, metronome, None)
            if metronome and dondokos:
                do_song(song_name, bpm, None, None)
