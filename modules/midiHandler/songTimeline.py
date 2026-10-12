import bisect
import mido

# Notes at or above middle C go to the right hand when a song has no per-hand tracks
SPLIT_NOTE = 60
# Track/channel groups whose average pitch differs by less than this are not treated as separate hands
MIN_HAND_GAP = 5

class Song:
    def __init__(self, midiFile):
        mid = mido.MidiFile(midiFile, clip=True)

        merged = []
        for trackIndex, track in enumerate(mid.tracks):
            tick = 0
            for order, msg in enumerate(track):
                tick += msg.time
                merged.append((tick, trackIndex, order, msg))
        merged.sort(key=lambda e: (e[0], e[1], e[2]))

        groupHands = classifyGroups(merged)

        self.events = []
        tempo = 500000
        lastTick = 0
        seconds = 0.0
        for tick, trackIndex, _, msg in merged:
            seconds += mido.tick2second(tick - lastTick, mid.ticks_per_beat, tempo)
            lastTick = tick
            if msg.type == "set_tempo":
                tempo = msg.tempo
            hand = None
            if msg.type in ("note_on", "note_off"):
                if groupHands is not None:
                    hand = groupHands.get((trackIndex, msg.channel), "right")
                else:
                    hand = "right" if msg.note >= SPLIT_NOTE else "left"
            self.events.append((seconds, msg.copy(time=0), hand))

        self.times = [e[0] for e in self.events]
        self.length = self.times[-1] if self.times else 0.0
        self.handMode = "tracks" if groupHands is not None else "pitch"

    def indexAt(self, seconds):
        return bisect.bisect_left(self.times, seconds)

def classifyGroups(merged):
    notes = {}
    for _, trackIndex, _, msg in merged:
        if msg.type == "note_on" and msg.velocity > 0 and msg.channel != 9:
            notes.setdefault((trackIndex, msg.channel), []).append(msg.note)
    if len(notes) < 2:
        return None

    averages = {group: sum(n) / len(n) for group, n in notes.items()}
    low, high = min(averages.values()), max(averages.values())
    if high - low < MIN_HAND_GAP:
        return None

    threshold = (low + high) / 2
    return {group: ("right" if avg >= threshold else "left") for group, avg in averages.items()}

def handAllowed(hand, selected):
    return selected == "both" or hand is None or hand == selected

def isNoteStart(msg):
    return msg.type == "note_on" and msg.velocity > 0
