import mido

REMOVE_CHANNELS = set()
SOURCE = "placeholder.mid"
TARGET = "player/raw.h"
TIMESCALE = 100
MAXSIZE = 5400
CODE = "const int len=%i;const Sound music[len]PROGMEM=%s;"

mid = mido.MidiFile(SOURCE)
tempo = []
time = 0
for msg in mid.tracks[0]:
    time += msg.time
    if msg.type == "set_tempo":
        tempo.append((time, msg.tempo))
tempo.sort(key=lambda x: x[0])

events = []
active = {}
maxpoly = 0
for i, track in enumerate(mid.tracks[1:]):
    if i in {0, 1}:
        time = 0
        real = 0
        tempoidx = 0
        for msg in track:
            time += msg.time
            if tempoidx < len(tempo) - 1 and tempo[tempoidx + 1][0] <= time:
                    tempoidx += 1
            real += mido.tick2second(msg.time, mid.ticks_per_beat, tempo[tempoidx][1])
            scaled = int(real * TIMESCALE)
            if (msg.type == "note_on") and (not msg.channel in REMOVE_CHANNELS) and (msg.velocity > 0) and (not (msg.note, msg.channel) in active):
                active[(msg.note, msg.channel)] = scaled
                if len(active) > maxpoly:
                    maxpoly = len(active)
            elif (msg.type == "note_off") or ((msg.type == "note_on") and (msg.velocity == 0)):
                if (msg.note, msg.channel) in active:
                    events.append((active[(msg.note, msg.channel)], scaled, msg.note))
                active.pop((msg.note, msg.channel))
events.sort(key=lambda x: x[0])

size = min(MAXSIZE, len(events))
array = "{%s}" % ",".join(["{%i, %i, %i}" % event for event in events[:size]])
text = CODE % (size, array)
with open(TARGET, "w") as f:
    f.write(text)

print("%i sound events parsed, %i stored" % (len(events), size))
print("Maximum polyphony: %i" % maxpoly)
