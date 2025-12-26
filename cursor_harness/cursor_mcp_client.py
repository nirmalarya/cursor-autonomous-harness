"""
Cursor + MCP Hybrid Client
===========================

DEPRECATED: Cursor CLI's MCP implementation is fundamentally broken in headless mode.

Use ClaudeSDKClient instead (set ANTHROPIC_API_KEY).

This file kept for reference/future Cursor CLI fixes.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from .mcp_manager import MCPManager, create_mcp_manager_from_cursor_config


class CursorMCPClient:
    """
    Hybrid client: Cursor CLI for AI + Direct MCP for tools.
    
    This solves Cursor CLI's MCP limitation while keeping the AI working.
    """
    
    def __init__(
        self,
        project_dir: Path,
        model: str = "sonnet-4.5",
        mcp_manager: Optional[MCPManager] = None
    ):
        self.project_dir = project_dir
        self.model = model
        # Don't spawn MCPs ourselves! cursor-agent handles them automatically
        self.mcp_manager = None
    
    async def run_session(self, prompt: str) -> Tuple[str, str]:
        """
        Run a single agent session.
        
        Uses Cursor CLI for AI reasoning + Direct MCP for tools.
        
        Args:
            prompt: The prompt to send to the agent
        
        Returns:
            (status, response) where status is "continue" or "error"
        """
        
        print(f"Running cursor-agent session...")
        print(f"  Model: {self.model}")
        print(f"  Project: {self.project_dir}")
        print(f"  MCPs: Auto-loaded from ~/.cursor/mcp.json")
        print()
        
        # cursor-agent auto-discovers MCPs, no need to augment prompt
        augmented_prompt = prompt
        
        # Use cursor-agent with streaming for real-time progress
        # Per official docs: https://cursor.com/docs/cli/headless
        cmd = [
            "cursor-agent",
            "-p",  # Print mode
            "--force",  # Allow file modifications
            "--approve-mcps",  # Auto-approve MCP servers
            "--output-format", "stream-json",  # Stream events in real-time
            "--stream-partial-output",  # Stream partial text deltas
            augmented_prompt,
        ]
        
        try:
            # Run cursor agent with real-time streaming
            process = subprocess.Popen(
                cmd,
                cwd=self.project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered
            )
            
            # Parse and display streaming JSON events
            tool_count = 0
            accumulated_text = ""
            last_text = ""  # Track to avoid duplicates
            
            for line in process.stdout:
                try:
                    event = json.loads(line.strip())
                    event_type = event.get('type', '')
                    subtype = event.get('subtype', '')
                    
                    if event_type == 'assistant':
                        # Accumulate text deltas
                        if 'message' in event and 'content' in event['message']:
                            for content_block in event['message']['content']:
                                if 'text' in content_block:
                                    text = content_block['text']
                                    # Avoid printing duplicates
                                    if text != last_text:
                                        accumulated_text += text
                                        print(text, end='', flush=True)
                                        last_text = text
                    
                    elif event_type == 'tool_call':
                        if subtype == 'started':
                            tool_count += 1
                            tool_call = event.get('tool_call', {})
                            
                            # Compact tool output
                            if 'writeToolCall' in tool_call:
                                path = tool_call['writeToolCall'].get('args', {}).get('path', 'unknown')
                                # Shorten path for readability
                                if len(path) > 60:
                                    path = "..." + path[-57:]
                                print(f"\n✏️  #{tool_count}: Write {path}", flush=True)
                            elif 'readToolCall' in tool_call:
                                path = tool_call['readToolCall'].get('args', {}).get('path', 'unknown')
                                if len(path) > 60:
                                    path = "..." + path[-57:]
                                print(f"\n📖 #{tool_count}: Read {path}", flush=True)
                            elif 'bashToolCall' in tool_call:
                                cmd_str = tool_call['bashToolCall'].get('args', {}).get('command', 'unknown')
                                if len(cmd_str) > 50:
                                    cmd_str = cmd_str[:47] + "..."
                                print(f"\n⚡ #{tool_count}: {cmd_str}", flush=True)
                        
                        elif subtype == 'completed':
                            # Don't print "Done" for every tool (too verbose)
                            # Just show completion inline with next tool
                            pass
                    
                    elif event_type == 'result':
                        duration = event.get('duration_ms', 0)
                        duration_sec = duration / 1000
                        print(f"\n\n✅ Completed in {duration_sec:.1f}s ({tool_count} tools)\n", flush=True)
                
                except json.JSONDecodeError:
                    # Non-JSON line (error messages, etc.)
                    print(line, end='', flush=True)
            
            # Wait for completion
            returncode = process.wait(timeout=3600)
            result = type('obj', (object,), {'returncode': returncode})()
            
            if result.returncode == 0:
                print("\n✅ Session complete")
                return "continue", ""
            else:
                print(f"\n❌ Session failed (exit code: {result.returncode})")
                return "error", ""
        
        except subprocess.TimeoutExpired:
            print("❌ Session timed out (1 hour limit)")
            return "error", "Session timeout"
        
        except FileNotFoundError:
            print("❌ Cursor CLI not found!")
            return "error", "Cursor CLI not found"
        
        except Exception as e:
            print(f"❌ Error running session: {e}")
            return "error", str(e)
    
    def _get_mcp_tools_list(self) -> str:
        """Get formatted list of available MCP tools."""
        tools_desc = []
        
        if "azure-devops" in self.mcp_manager.servers:
            tools_desc.append("""
**Azure DevOps MCP:**
- Query work items (search, filter by epic/state)
- Get work item details
- Add comments to work items
- Update work item fields
- Mark work items as Done
""")
        
        if "playwright" in self.mcp_manager.servers:
            tools_desc.append("""
**Playwright MCP:**
- Navigate to URLs
- Click elements
- Fill forms
- Take screenshots
- Verify page content
""")
        
        if "puppeteer" in self.mcp_manager.servers:
            tools_desc.append("""
**Puppeteer MCP:**
- Navigate to URLs
- Click elements
- Fill forms
- Take screenshots
- Execute JavaScript
""")
        
        return "\n".join(tools_desc) if tools_desc else "None configured"
    
    def __enter__(self):
        """Start MCP servers when entering context."""
        self.mcp_manager.start_all()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop MCP servers when exiting context."""
        self.mcp_manager.stop_all()


def check_cursor_prerequisites() -> Tuple[bool, str]:
    """
    Check if cursor-agent CLI is installed.
    
    Returns:
        (is_ready, error_message)
    """
    try:
        result = subprocess.run(
            ["cursor-agent", "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, ""
        else:
            return False, "cursor-agent not working"
    except FileNotFoundError:
        return False, """
cursor-agent not found!

Please install Cursor CLI:
  curl https://cursor.com/install -fsS | bash

Then ensure cursor-agent is available:
  cursor-agent --version
"""
    except Exception as e:
        return False, f"Error checking cursor-agent: {e}"

