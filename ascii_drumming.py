from pydub import AudioSegment, effects
import os, glob

def my_sample(name, fmt=None):
    #print('Searching: %s' % name)

    if fmt is None:
        fmt = name.split('.')[-1]

    def find_samples(name):
        return glob.glob(name) + glob.glob('my_set'+os.sep+name)

    restore = os.getcwd()
    samples = find_samples(name)
    lastdir = None
    rel_pos = ''

    while (not samples) and os.getcwd() != lastdir:
        lastdir = os.getcwd()
        os.chdir('..')
        rel_pos += '..' + os.sep
        #print('Moving: %s -> %s' % (lastdir, os.getcwd()))
        samples = find_samples(name)

    #print('Got:', samples)

    os.chdir(restore)

    return AudioSegment.from_file(rel_pos + samples[0], fmt)

do =  my_sample('taiko4.wav') - 2
ko =  my_sample('taiko2.wav') - 2
don = my_sample('taiko3.wav') + 2
kon = my_sample('taiko5.wav') + 2
rim = my_sample('rim.wav') - 12
sa = effects.speedup(my_sample('sa.wav')[307:], playback_speed=4.5) - 12
#sa = effects.speedup(my_sample('sa.wav')[310:800], playback_speed=3.5) - 12

shime_do = my_sample('shime1.wav') - 8
shime_ko = my_sample('shime2.wav') - 8
shime_don = my_sample('shime3.wav')

Don = my_sample('taiko1.wav')
#Don = don.overlay(kon)

click = my_sample('click.wav') - 12

char_map = {
    'd': do,
    'k': ko,
    'D': don,
    'K': kon,
    'B': Don,
    'r': rim,
    's': shime_do,
    'z': shime_ko,
    'S': shime_don,
    ':': sa,
}

pause = AudioSegment.silent(duration=0.1)

def play(pattern, bpm=80, metronome=None, dondokos=None):

    tick = 1000 * 60 / float(bpm * 4) # dokodoko = 1 beat = 4 ticks
    print('BPM: %s, tick: %s' % (bpm, tick))

    beats = (len(pattern)+3) // 4

    METRONOME_EARLY = 4
    if metronome is not None:
        beats += METRONOME_EARLY

    if dondokos is not None:
        DONDOKOS_EARLY = dondokos
        beats += DONDOKOS_EARLY

    ticks = beats * 4
    print('Beats: %d, ticks: %d' % (beats, ticks))

    tick_times = [ x * tick for x in range(ticks) ]

    song = AudioSegment.silent(duration=ticks*tick+2)

    # add Metronome
    if metronome is not None:
        print('Inserting metronome clicks every %s ticks.' % metronome)
        for cnt, t in enumerate(tick_times):
            if not (cnt % metronome):
                song = song.overlay(click, position=t)
        tick_times = tick_times[METRONOME_EARLY*metronome:]


    # add dondokos
    if dondokos is not None:
        print('Inserting dondokos (%s before start of pattern).' % DONDOKOS_EARLY)
        dondoko = AudioSegment.silent(duration=4*tick+2)
        dondoko = dondoko.overlay(my_sample('shime1.wav'), position=0)
        dondoko = dondoko.overlay(my_sample('shime2.wav') - 6, position=2*tick)
        dondoko = dondoko.overlay(my_sample('shime3.wav') - 6, position=3*tick)
        dondoko = dondoko - 16

        for cnt, t in enumerate(tick_times):
            if not (cnt % 4):
                song = song.overlay(dondoko, position=t)
        tick_times = tick_times[DONDOKOS_EARLY*4:]

    if not 'implemented':
        dokodoko = AudioSegment.silent(duration=4*tick+2)
        dokodoko = dokodoko.overlay(do, position=0)
        dokodoko = dokodoko.overlay(ko, position=tick)
        dokodoko = dokodoko.overlay(do, position=2*tick)
        dokodoko = dokodoko.overlay(ko, position=3*tick)
        dokodoko = dokodoko - 16

        dokonko = AudioSegment.silent(duration=4*tick+2)
        dokonko = dokonko.overlay(do, position=0)
        dokonko = dokonko.overlay(ko, position=tick)
        dokonko = dokonko.overlay(ko, position=3*tick)
        dokonko = dokonko - 16


    print('Playing song:')

    char_accu = ''
    for cnt, tup in enumerate(zip(tick_times, pattern)):

        t, char = tup
        song = song.overlay(char_map.get(char, pause), position=t)

        char_accu += char
        if not (cnt+1) % 8:
            print(char_accu)
            char_accu = ''

    if char_accu:
        print(char_accu)

    return effects.normalize(song)

