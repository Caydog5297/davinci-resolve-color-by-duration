#!/usr/bin/env python3
"""
Resolve Color by Duration

Colors timeline video clips on a chosen track based on clip duration.

Default mapping:
    < 3s   -> Pink
    3-4s   -> Orange
    4-5s   -> Yellow
    >= 5s  -> Navy

Run from inside DaVinci Resolve:
    Workspace > Scripts > Edit > ColorByDuration
"""

# --------------------------
# USER SETTINGS
# --------------------------
TRACK_INDEX = 1
# --------------------------


def get_color_for_duration_seconds(duration_seconds: float) -> str:
    if duration_seconds < 3.0:
        return "Pink"
    elif duration_seconds < 4.0:
        return "Orange"
    elif duration_seconds < 5.0:
        return "Yellow"
    else:
        return "Navy"


def main():
    r = globals().get("resolve", None)
    if not r:
        raise RuntimeError(
            "This script must be run from inside DaVinci Resolve via Workspace > Scripts."
        )

    project_manager = r.GetProjectManager()
    if not project_manager:
        raise RuntimeError("Could not access Project Manager.")

    project = project_manager.GetCurrentProject()
    if not project:
        raise RuntimeError("No current project is open.")

    timeline = project.GetCurrentTimeline()
    if not timeline:
        raise RuntimeError("No current timeline is open.")

    fps_str = (
        timeline.GetSetting("timelinePlaybackFrameRate")
        or timeline.GetSetting("timelineFrameRate")
        or project.GetSetting("timelinePlaybackFrameRate")
        or project.GetSetting("timelineFrameRate")
    )
    if not fps_str:
        raise RuntimeError("Could not read timeline frame rate.")

    fps = float(fps_str)

    items = timeline.GetItemListInTrack("video", TRACK_INDEX)
    if not items:
        print(f"No video clips found on V{TRACK_INDEX}.")
        return

    counts = {
        "Pink": 0,
        "Orange": 0,
        "Yellow": 0,
        "Navy": 0,
        "Failed": 0,
    }

    for i, item in enumerate(items, start=1):
        try:
            duration_frames = item.GetDuration()
            duration_seconds = float(duration_frames) / fps
            color = get_color_for_duration_seconds(duration_seconds)
            ok = item.SetClipColor(color)
            if ok:
                counts[color] += 1
            else:
                counts["Failed"] += 1
                print(f"Failed on item {i}: {item.GetName()} -> {color}")
        except Exception as e:
            counts["Failed"] += 1
            print(f"Error on item {i}: {e}")

    print("Done.")
    print(f"Track: V{TRACK_INDEX}")
    print(f"Timeline FPS: {fps}")
    print(f"Pink (<3s): {counts['Pink']}")
    print(f"Orange (3s to <4s): {counts['Orange']}")
    print(f"Yellow (4s to <5s): {counts['Yellow']}")
    print(f"Navy (>=5s): {counts['Navy']}")
    print(f"Failed: {counts['Failed']}")


if __name__ == "__main__":
    main()
