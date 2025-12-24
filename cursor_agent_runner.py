"""
Cursor Agent Runner with Session Management
===========================================

Core logic for running autonomous coding sessions using Cursor CLI.
"""

import asyncio
from pathlib import Path
from typing import Optional

from cursor_client_streaming import CursorAgentClient
from progress import count_features, print_progress_summary, print_session_header
from security import SecurityValidator


# Configuration
AUTO_CONTINUE_DELAY_SECONDS = 3


async def run_autonomous_agent(
    project_dir: Path,
    model: str,
    max_iterations: Optional[int],
    initializer_prompt: str,
    coding_prompt: str,
) -> None:
    """
    Run the autonomous agent loop using Cursor CLI.

    Args:
        project_dir: Directory for the project
        model: Cursor model to use (e.g., sonnet-4, gpt-5, sonnet-4-thinking)
        max_iterations: Maximum number of iterations (None for unlimited)
        initializer_prompt: Prompt for first session
        coding_prompt: Prompt for continuation sessions
    """
    print("\n" + "=" * 70)
    print("  CURSOR AUTONOMOUS CODING AGENT")
    print("  (Using Cursor CLI)")
    print("=" * 70)
    print(f"\nProject directory: {project_dir.resolve()}")
    print(f"Model: {model}")
    if max_iterations:
        print(f"Max iterations: {max_iterations}")
    else:
        print("Max iterations: Unlimited (will run until completion)")
    print()

    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=True)

    # Initialize security validator
    security_validator = SecurityValidator()

    # Check if this is a fresh start or continuation
    feature_file = project_dir / "feature_list.json"
    is_first_run = not feature_file.exists()

    if is_first_run:
        print("Fresh start - will use initializer agent")
        print()
        print("=" * 70)
        print("  NOTE: First session takes 10-20+ minutes!")
        print("  The agent is generating comprehensive test cases.")
        print("  This may appear to hang - it's working.")
        print("=" * 70)
        print()
    else:
        print("Continuing existing project")
        print_progress_summary(project_dir)

    # Main loop
    iteration = 0

    while True:
        iteration += 1

        # Check max iterations
        if max_iterations and iteration > max_iterations:
            print(f"\nReached max iterations ({max_iterations})")
            print("To continue, run the script again without --max-iterations")
            break

        # Print session header
        print_session_header(iteration, is_first_run)

        # Create client (fresh context for each session)
        client = CursorAgentClient(
            project_dir=project_dir,
            model=model,
            security_validator=security_validator,
        )

        # Choose prompt based on session type
        if is_first_run:
            prompt = initializer_prompt
            is_first_run = False  # Only use initializer once
        else:
            prompt = coding_prompt

        # Run session
        status, response = await client.run_session(prompt)

        # Handle status
        if status == "complete":
            print("\nAgent completed this session")
            print_progress_summary(project_dir)

            # Check if all features are done
            passing, total = count_features(project_dir)
            if total > 0 and passing >= total:
                print("\n🎉 All features complete! Project finished.")
                break

            # Auto-continue
            print(f"\nAgent will auto-continue in {AUTO_CONTINUE_DELAY_SECONDS}s...")
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        elif status == "max_turns":
            print("\nSession reached max turns")
            print("Will continue with a fresh session...")
            print_progress_summary(project_dir)
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        elif status == "error":
            print(f"\nSession encountered an error: {response}")
            print("Will retry with a fresh session...")
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)

        # Small delay between sessions
        if max_iterations is None or iteration < max_iterations:
            print("\nPreparing next session...\n")
            await asyncio.sleep(1)

    # Final summary
    print("\n" + "=" * 70)
    print("  SESSION COMPLETE")
    print("=" * 70)
    print(f"\nProject directory: {project_dir.resolve()}")
    print_progress_summary(project_dir)

    # Print instructions for running the generated application
    print("\n" + "-" * 70)
    print("  TO RUN THE GENERATED APPLICATION:")
    print("-" * 70)
    print(f"\n  cd {project_dir.resolve()}")
    print("  ./init.sh           # Run the setup script")
    print("  # Or manually:")
    print("  npm install && npm run dev")
    print("\n  Then open http://localhost:3000 (or check init.sh for the URL)")
    print("-" * 70)

    print("\nDone!")

