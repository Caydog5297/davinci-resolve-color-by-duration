#!/usr/bin/env python3

def get_color_for_duration_seconds(duration_seconds: float) -> str:
    if duration_seconds < 3.0:
        return "Pink"
    elif duration_seconds < 4.0:
        return "Orange"
    elif duration_seconds < 5.0:
        return "Yellow"
    else:
        return "Navy"


def make_counts_dict() -> dict:
    return {
        "Pink": 0,
        "Orange": 0,
        "Yellow": 0,
        "Navy": 0,
        "Failed": 0,
    }


def add_counts(target: dict, source: dict) -> None:
    for key in target:
        target[key] += source.get(key, 0)


def main():
    resolve_app = globals().get("resolve", None)

    if not resolve_app:
        raise RuntimeError(
            "This script must be run from inside DaVinci Resolve via Workspace > Scripts."
        )

    project_manager = resolve_app.GetProjectManager()
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

    try:
        fps = float(fps_str)
    except (TypeError, ValueError):
        raise RuntimeError(f"Invalid timeline frame rate: {fps_str!r}")

    video_track_count = timeline.GetTrackCount("video")
    if not video_track_count or video_track_count < 1:
        print("No video tracks found in the current timeline.")
        return

    total_counts = make_counts_dict()
    total_clips_colored = 0

    print("Starting clip coloring across all video tracks...")
    print(f"Timeline FPS: {fps}")
    print(f"Video tracks found: {video_track_count}")
    print("")

    for track_index in range(1, video_track_count + 1):
        items = timeline.GetItemListInTrack("video", track_index)

        if not items:
            print(f"Track V{track_index}: no clips found.")
            print("")
            continue

        track_counts = make_counts_dict()
        track_clips_colored = 0

        for item_number, item in enumerate(items, start=1):
            try:
                duration_frames = item.GetDuration()
                duration_seconds = float(duration_frames) / fps
                color = get_color_for_duration_seconds(duration_seconds)

                ok = item.SetClipColor(color)
                if ok:
                    track_counts[color] += 1
                    track_clips_colored += 1
                else:
                    track_counts["Failed"] += 1
                    print(
                        f"Failed on V{track_index} item {item_number}: "
                        f"{item.GetName()} -> {color}"
                    )

            except Exception as exc:
                track_counts["Failed"] += 1
                print(f"Error on V{track_index} item {item_number}: {exc}")

        add_counts(total_counts, track_counts)
        total_clips_colored += track_clips_colored

        print(f"Track V{track_index} done.")
        print(f"  Pink (<3s): {track_counts['Pink']}")
        print(f"  Orange (3s to <4s): {track_counts['Orange']}")
        print(f"  Yellow (4s to <5s): {track_counts['Yellow']}")
        print(f"  Navy (>=5s): {track_counts['Navy']}")
        print(f"  Failed: {track_counts['Failed']}")
        print("")

    print("Done.")
    print(f"Tracks scanned: {video_track_count}")
    print(f"Total clips colored: {total_clips_colored}")
    print(f"Pink (<3s): {total_counts['Pink']}")
    print(f"Orange (3s to <4s): {total_counts['Orange']}")
    print(f"Yellow (4s to <5s): {total_counts['Yellow']}")
    print(f"Navy (>=5s): {total_counts['Navy']}")
    print(f"Failed: {total_counts['Failed']}")


if __name__ == "__main__":
    main()
