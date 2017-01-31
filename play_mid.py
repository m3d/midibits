"""
import pygame
pygame.init()

#midi_out = pygame.midi.Output(port, 0) 
pygame.mixer.music.load("music.mid")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
"""


"""
import mido
#mido.set_backend('mido.backends.portmidi')
back = mido.Backend('mido.backends.pygame')
output = back.open_output()
output.send(mido.Message('note_on', note=60, velocity=64))
"""


import pygame.midi  
import time
import midi
import sys

GRAND_PIANO = 0
CHURCH_ORGAN = 19

#    instrument = CHURCH_ORGAN

instrument = GRAND_PIANO 

note = 60
velocity = 480 #120

pygame.midi.init()
port = 3 #1
midi_out = pygame.midi.Output(port, 0)
midi_out.set_instrument(instrument)

#midi_out.note_on(note, velocity)
#time.sleep(0.1)
#midi_out.note_off(note)

midifile = sys.argv[1]
pattern = midi.read_midifile(midifile)
#print(repr(pattern))

pattern.make_ticks_abs()
events = []
for track in pattern:
    for event in track:
        events.append(event)
events.sort()
#seq.start_sequencer()
prev_tick = 0
for event in events:
    print repr(event)
    tick = event.tick
    data = event.data
#    if len(data) == 2:
    if isinstance(event, midi.NoteOnEvent):
        note, vel = data
#        midi_out.note_on(note, vel)
        midi_out.write_short(0x90, note, vel)
    if isinstance(event, midi.ControlChangeEvent):
        midi_out.write_short(0xB0, data[0], data[1])
    if tick > prev_tick:
        time.sleep((1/480.)*(tick-prev_tick))
#        midi_out.note_off(note)
    prev_tick = tick

#    buf = seq.event_write(event, False, False, True)
#    if buf == None:
#        continue
#    if buf < 1000:
#        time.sleep(.5)
#time.sleep(30)

del midi_out
pygame.midi.quit()


