"""
Progress Tracking Utilities
============================

Track and display agent progress across sessions.
"""

import json
from pathlib import Path


def print_session_header(iteration: int, is_first_run: bool) -> None:
    """Print session header."""
    print("\n" + "=" * 70)
    if is_first_run:
        print(f"  SESSION {iteration}: INITIALIZER AGENT")
        print("  Generating comprehensive test suite...")
    else:
        print(f"  SESSION {iteration}: CODING AGENT")
        print("  Implementing features from test suite...")
    print("=" * 70)
    print()


def print_progress_summary(project_dir: Path) -> None:
    """Print progress summary from feature_list.json."""
    feature_file = project_dir / "feature_list.json"

    if not feature_file.exists():
        print("Progress: No feature list yet")
        return

    try:
        with open(feature_file, "r") as f:
            data = json.load(f)

        # Handle both formats
        if isinstance(data, dict) and "features" in data:
            features = data["features"]
        elif isinstance(data, list):
            features = data
        else:
            print("Progress: Invalid feature list format")
            return

        if not features:
            print("Progress: Feature list is empty")
            return

        total = len(features)
        passing = sum(1 for f in features if f.get("passes") == True)
        pending = total - passing

        print(f"Progress: {passing}/{total} features passing ({pending} remaining)")

        # Show next few pending features
        pending_features = [f for f in features if not f.get("passes", False)]
        if pending_features:
            print("\nNext features to implement:")
            for i, feature in enumerate(pending_features[:5], 1):
                desc = feature.get("description", "No description")
                # Truncate long descriptions
                desc_short = desc[:80] + "..." if len(desc) > 80 else desc
                print(f"  {i}. {desc_short}")
            if len(pending_features) > 5:
                print(f"  ... and {len(pending_features) - 5} more")

    except Exception as e:
        print(f"Progress: Error reading feature list: {e}")


def count_features(project_dir: Path) -> tuple[int, int]:
    """
    Count total and passing features.

    Returns:
        Tuple of (passing_count, total_count)
    """
    feature_file = project_dir / "feature_list.json"

    if not feature_file.exists():
        return 0, 0

    try:
        with open(feature_file, "r") as f:
            data = json.load(f)

        # Handle both formats
        if isinstance(data, dict) and "features" in data:
            features = data["features"]
        elif isinstance(data, list):
            features = data
        else:
            return 0, 0

        total = len(features)
        passing = sum(1 for f in features if f.get("passes") == True)

        return passing, total
    except:
        return 0, 0



