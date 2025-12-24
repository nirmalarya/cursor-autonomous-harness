"""
Security Validation for Bash Commands
======================================

Command allowlist and validation for autonomous agent.
"""

import os
import re
import shlex


class SecurityValidator:
    """Validates bash commands against an allowlist."""

    # Allowed commands for development tasks
    ALLOWED_COMMANDS = {
        # File inspection
        "ls",
        "cat",
        "head",
        "tail",
        "wc",
        "grep",
        "find",
        "tree",
        # File operations
        "cp",
        "mv",
        "mkdir",
        "chmod",
        "touch",
        # Directory
        "pwd",
        "cd",
        # Node.js development
        "npm",
        "node",
        "npx",
        # Python development
        "python",
        "python3",
        "pip",
        "pip3",
        # Version control
        "git",
        # Process management
        "ps",
        "lsof",
        "sleep",
        "pkill",
        # Other utilities
        "echo",
        "which",
        "curl",
        "wget",
        # Script execution
        "init.sh",
        "bash",
        "sh",
    }

    # Commands needing extra validation
    COMMANDS_NEEDING_EXTRA_VALIDATION = {"pkill", "chmod", "init.sh", "bash", "sh", "curl", "wget"}

    def validate_command(self, command_string: str) -> tuple[bool, str]:
        """
        Validate a bash command.

        Args:
            command_string: The command to validate

        Returns:
            Tuple of (is_allowed, reason_if_blocked)
        """
        # Extract all commands from the string
        commands = self._extract_commands(command_string)

        if not commands:
            return False, "Could not parse command for security validation"

        # Check each command against allowlist
        for cmd in commands:
            if cmd not in self.ALLOWED_COMMANDS:
                return False, f"Command '{cmd}' is not in the allowed commands list"

            # Additional validation for sensitive commands
            if cmd in self.COMMANDS_NEEDING_EXTRA_VALIDATION:
                if cmd == "pkill":
                    is_allowed, reason = self._validate_pkill(command_string)
                    if not is_allowed:
                        return False, reason
                elif cmd == "chmod":
                    is_allowed, reason = self._validate_chmod(command_string)
                    if not is_allowed:
                        return False, reason
                elif cmd == "init.sh":
                    is_allowed, reason = self._validate_init_script(command_string)
                    if not is_allowed:
                        return False, reason
                elif cmd in ("bash", "sh"):
                    is_allowed, reason = self._validate_shell_script(command_string)
                    if not is_allowed:
                        return False, reason
                elif cmd in ("curl", "wget"):
                    is_allowed, reason = self._validate_network_command(command_string)
                    if not is_allowed:
                        return False, reason

        return True, ""

    def _extract_commands(self, command_string: str) -> list[str]:
        """Extract command names from a shell command string."""
        commands = []

        # Split on semicolons
        segments = re.split(r'(?<!["\'])\s*;\s*(?!["\'])', command_string)

        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue

            try:
                tokens = shlex.split(segment)
            except ValueError:
                # Malformed command - fail safe
                return []

            if not tokens:
                continue

            # Track when we expect a command vs arguments
            expect_command = True

            for token in tokens:
                # Shell operators
                if token in ("|", "||", "&&", "&"):
                    expect_command = True
                    continue

                # Skip shell keywords
                if token in ("if", "then", "else", "elif", "fi", "for", "while",
                           "until", "do", "done", "case", "esac", "in", "!", "{", "}"):
                    continue

                # Skip flags
                if token.startswith("-"):
                    continue

                # Skip variable assignments
                if "=" in token and not token.startswith("="):
                    continue

                if expect_command:
                    cmd = os.path.basename(token)
                    commands.append(cmd)
                    expect_command = False

        return commands

    def _validate_pkill(self, command_string: str) -> tuple[bool, str]:
        """Validate pkill - only allow killing dev processes."""
        allowed_process_names = {
            "node",
            "npm",
            "npx",
            "vite",
            "next",
            "webpack",
            "parcel",
            "python",
            "python3",
        }

        try:
            tokens = shlex.split(command_string)
        except ValueError:
            return False, "Could not parse pkill command"

        # Get process name arguments
        args = [t for t in tokens[1:] if not t.startswith("-")]

        if not args:
            return False, "pkill requires a process name"

        target = args[-1]

        # Extract first word if full command line
        if " " in target:
            target = target.split()[0]

        if target in allowed_process_names:
            return True, ""

        return False, f"pkill only allowed for dev processes: {allowed_process_names}"

    def _validate_chmod(self, command_string: str) -> tuple[bool, str]:
        """Validate chmod - only allow +x (make executable)."""
        try:
            tokens = shlex.split(command_string)
        except ValueError:
            return False, "Could not parse chmod command"

        if len(tokens) < 3:
            return False, "chmod requires mode and file"

        mode = None
        for token in tokens[1:]:
            if not token.startswith("-"):
                if mode is None:
                    mode = token
                    break

        if mode is None:
            return False, "chmod requires a mode"

        # Only allow +x variants
        if not re.match(r"^[ugoa]*\+x$", mode):
            return False, f"chmod only allowed with +x mode, got: {mode}"

        return True, ""

    def _validate_init_script(self, command_string: str) -> tuple[bool, str]:
        """Validate init.sh execution."""
        try:
            tokens = shlex.split(command_string)
        except ValueError:
            return False, "Could not parse init script command"

        if not tokens:
            return False, "Empty command"

        script = tokens[0]

        if script == "./init.sh" or script.endswith("/init.sh"):
            return True, ""

        return False, f"Only ./init.sh is allowed, got: {script}"

    def _validate_shell_script(self, command_string: str) -> tuple[bool, str]:
        """Validate bash/sh execution - only allow running specific scripts."""
        try:
            tokens = shlex.split(command_string)
        except ValueError:
            return False, "Could not parse shell command"

        if len(tokens) < 2:
            return False, "Shell command requires a script to run"

        # Only allow running init.sh or similar safe scripts
        script_arg = tokens[1]

        if "init.sh" in script_arg:
            return True, ""

        return False, f"bash/sh only allowed for init.sh, got: {script_arg}"

    def _validate_network_command(self, command_string: str) -> tuple[bool, str]:
        """Validate curl/wget - only allow safe operations."""
        # For now, allow all curl/wget but could add URL allowlist
        # This is less restrictive but still logged
        return True, ""



