# Fix: NoDoubles mode breaks legato when adjacent keys share a keyboard key

## Problem
When **NoDoubles** mode is enabled, playing legato with adjacent keys where:
- First note = key (e.g., `z` for MIDI note 60)
- Second note = Shift + same key (e.g., `Z` = Shift+`z` for MIDI note 61)

Releasing the first note incorrectly stops the second note from sounding.

## Root Cause
The NoDoubles logic released a keyboard key when a new note was pressed, but didn't track **which MIDI note "owned" which keyboard key**. 

Sequence:
1. Note 60 pressed → presses `z`
2. Note 61 pressed → NoDoubles releases `z` (thinking it's a double), then presses Shift+`z`
3. Note 60 released → blindly releases `z` **again** (but `z` was already released in step 2!)
4. This interferes with Shift+`z` held for note 61, cutting it off

## Solution
Added `noteToKeyMap` dictionary tracking MIDI note → set of keyboard keys it owns.

### Changes in 6 files:
| File | Purpose |
|------|---------|
| `modules/midiHandler/midiToQWERTYWindows.py` | Live MIDI input → VK (Windows) |
| `modules/midiHandler/midiToQWERTYLinux.py` | Live MIDI input → VK (Linux) |
| `modules/midiHandler/midiToQWERTYDarwin.py` | Live MIDI input → VK (macOS) |
| `modules/midiHandler/midiWindows.py` | MIDI file playback → VK (Windows) |
| `modules/midiHandler/midiLinux.py` | MIDI file playback → VK (Linux) |
| `modules/midiHandler/midiDarwin.py` | MIDI file playback → VK (macOS) |

### Logic changes:
- **note_on (NoDoubles)**: When stealing a key, find previous owner via `noteToKeyMap`, release key properly, transfer ownership to new note
- **note_off**: Only release keys owned by that specific MIDI note (via `noteToKeyMap`)

## Testing
- Legato with adjacent keys (normal + Shift variant) no longer cuts off second note
- Single notes still release correctly
- NoDoubles still prevents actual double-triggering of same key