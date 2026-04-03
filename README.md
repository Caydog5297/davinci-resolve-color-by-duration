# DaVinci Resolve Color by Duration

Color timeline video clips on the DaVinci Resolve Edit page based on clip duration. This script is designed for editors who want to quickly visualize pacing in the cut-heavy sequences.

## What it does

The script scans **all video tracks** in the current timeline and colors clips using these rules by default:

| Duration             | Color  |
| -------------------- | ------ |
| Under 3 seconds      | Pink   |
| 3 to under 4 seconds | Orange |
| 4 to under 5 seconds | Yellow |
| 5 seconds and up     | Navy   |

Only video clips are targeted. Audio tracks are not modified.

## Requirements
- Windows
- DaVinci Resolve installed
- A project and timeline open in Resolve
- Access to your Resolve user scripts folder

Users should:
1. Download `ColorByDuration.py`
2. Copy it into Resolve's Edit scripts folder
3. Restart Resolve
4. Run it from `Workspace > Scripts`

---

## Install

### 1. Download the script

Download `ColorByDuration.py` from this repository.

### 2. Copy it into the Resolve Edit scripts folder

Place the file here:

```
C:\Users\<YOUR-USERNAME>\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\
```

Example:

```
C:\Users\Cayden Drake\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\
```

> **Tip:** To get to AppData quickly, press `Win + R`, type `%appdata%`, and press Enter. Then navigate to `Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\`.

### 3. Restart DaVinci Resolve

Resolve may not detect newly added scripts until it is restarted.

## How to use

1. Open DaVinci Resolve
2. Open the target project and timeline
3. Go to the Edit page
4. Run **Workspace > Scripts > ColorByDuration**

The script will scan every video track in the current timeline, color the clips, and print a summary in Resolve's console output.

## Customizing the duration buckets

Edit this function in `ColorByDuration.py`:

```python
def get_color_for_duration_seconds(duration_seconds: float) -> str:
    if duration_seconds < 3.0:
        return "Pink"
    elif duration_seconds < 4.0:
        return "Orange"
    elif duration_seconds < 5.0:
        return "Yellow"
    else:
        return "Navy"
```

Example with different thresholds:

```python
def get_color_for_duration_seconds(duration_seconds: float) -> str:
    if duration_seconds < 2.0:
        return "Pink"
    elif duration_seconds < 3.5:
        return "Orange"
    elif duration_seconds < 6.0:
        return "Yellow"
    else:
        return "Navy"
```

## Example output

After running, the script prints a summary like this in Resolve's console output:

```
Starting clip coloring across all video tracks...
Timeline FPS: 24.0
Video tracks found: 3

Track V1 done.
  Pink (<3s): 79
  Orange (3s to <4s): 29
  Yellow (4s to <5s): 33
  Navy (>=5s): 143
  Failed: 0

Track V2 done.
  Pink (<3s): 12
  Orange (3s to <4s): 8
  Yellow (4s to <5s): 4
  Navy (>=5s): 20
  Failed: 0

Track V3: no clips found.

Done.
Tracks scanned: 3
Total clips colored: 328
Pink (<3s): 91
Orange (3s to <4s): 37
Yellow (4s to <5s): 37
Navy (>=5s): 163
Failed: 0
```

## Troubleshooting

### The script does not show up in Resolve

Check that the file is in:

```
C:\Users\<YOUR-USERNAME>\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\
```

Then restart Resolve.

### Nothing changed after I ran it

Check:

- A timeline is open
- The timeline contains video clips
- Resolve was restarted after adding or editing the script

### I only want video clips colored

That is already the current behavior. The script scans only video tracks and does not modify audio tracks.

## Suggested workflow

1. Run the script
2. Zoom out on the timeline
3. Scan for clusters of short-duration colors, especially Pink and Orange
4. Review sections with unusually dense short cuts
5. Adjust pacing where needed

This is especially useful for multicam podcast edits where visual rhythm matters.

## Repository contents

| File                 | Description          |
| -------------------- | -------------------- |
| `ColorByDuration.py` | Main Resolve script  |
| `README.md`          | Setup and usage guide |
| `.gitignore`         | Git housekeeping     |
| `LICENSE`            | MIT license          |

## License

MIT
