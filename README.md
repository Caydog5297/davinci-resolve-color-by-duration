# davinci-resolve-color-by-duration
DaVinci Resolve script that colors timeline video clips by duration.

# Resolve Color by Duration

Color timeline **video clips** on the DaVinci Resolve **Edit** page based on clip duration.

This script is designed for editors who want to quickly visualize pacing in multicam edits, podcast timelines, interviews, and other cut-heavy sequences.

## What it does

On a chosen **video track**, the script colors clips using these rules by default:

| Duration | Color |
|---|---|
| Under 3 seconds | Pink |
| 3 to under 4 seconds | Orange |
| 4 to under 5 seconds | Yellow |
| 5 seconds and up | Navy |

Only **video clips** are targeted. Audio tracks are not modified.

## Requirements

- Windows
- DaVinci Resolve installed
- A project and timeline open in Resolve
- Access to your Resolve user scripts folder

No `pip install` is required.

## Important

This is a **DaVinci Resolve script**, not a standalone Windows application.

Users should:

1. Download `ColorByDuration.py`
2. Copy it into Resolve's **Edit scripts** folder
3. Restart Resolve
4. Run it from **Workspace > Scripts > Edit**

---

## Install

### 1. Download the script

Download `ColorByDuration.py` from this repository.

### 2. Copy it into the Resolve Edit scripts folder

Place the file here:

```
C:\Users\<YOUR-USERNAME>\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\
```

**Example:**

```
C:\Users\Cayden Drake\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\
```

If the `Edit` folder does not exist, create it.

> **Tip:** To get to AppData quickly, press `Win + R`, type `%appdata%`, and press Enter. Then navigate to `Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\`.

### 3. Restart DaVinci Resolve

Resolve may not detect newly added scripts until it is restarted.

---

## How to use

1. Open **DaVinci Resolve**
2. Open the target project and timeline
3. Go to the **Edit** page
4. Make sure the target clips are on the video track you want to scan
5. Run: **Workspace > Scripts > Edit > ColorByDuration**

The script will color the clips on the configured video track and print a summary.

---

## Default track selection

By default, the script scans **Video Track 1**:

```python
TRACK_INDEX = 1
```

Change this if your clips are on another track:

- `1` = V1
- `2` = V2
- `3` = V3

**Example for V2:**

```python
TRACK_INDEX = 2
```

---

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

**Example with different thresholds:**

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

---

## Example output

After running, the script prints a summary like this in Resolve's console output:

```
Done.
Track: V1
Timeline FPS: 24.0
Pink (<3s): 79
Orange (3s to <4s): 29
Yellow (4s to <5s): 33
Navy (>=5s): 143
Failed: 0
```

---

## Troubleshooting

### The script does not show up in Resolve

Check that the file is in:

```
C:\Users\<YOUR-USERNAME>\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\
```

Then restart Resolve.

### Nothing changed after I ran it

Check:

- The clips are on the correct video track
- `TRACK_INDEX` matches that track
- Resolve was restarted after adding or editing the script

### I only want video clips colored

That is already the current behavior. The script scans only:

```python
timeline.GetItemListInTrack("video", TRACK_INDEX)
```

### Some clips fail to color

That usually means a color name is not accepted by Resolve. The included defaults use names that worked in testing: `Pink`, `Orange`, `Yellow`, `Navy`.

### I tried `pip install DaVinciResolveScript` and it failed

That is expected. `DaVinciResolveScript` is not a PyPI package. This script is meant to run inside Resolve from the Scripts menu and does not require any pip installation.

---

## Known limitations

- Windows-focused instructions only
- One video track per run
- Must be run from inside Resolve
- Does not color audio clips
- Does not automatically scan all video tracks

---

## Suggested workflow

1. Run the script
2. Zoom out on the timeline
3. Scan for clusters of short-duration colors (Pink, Orange)
4. Review sections with unusually dense short cuts
5. Adjust pacing where needed

This is especially useful for multicam podcast edits where visual rhythm matters.

---

## Repository contents

| File | Description |
|---|---|
| `ColorByDuration.py` | Main Resolve script |
| `README.md` | Setup and usage guide |
| `.gitignore` | Git housekeeping |
| `LICENSE` | MIT license |

## License

MIT
