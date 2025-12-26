"""
MCP Manager - Direct MCP Server Communication
==============================================

Manages MCP servers via stdio protocol, bypassing Cursor CLI's MCP limitations.
User-friendly: Just specify MCPs needed, harness handles everything!
"""

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
import os


class MCPServer:
    """Represents a single MCP server process."""
    
    def __init__(self, name: str, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
        self.name = name
        self.command = command
        self.args = args
        self.env = env or {}
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
    
    def start(self):
        """Start the MCP server subprocess."""
        print(f"🔧 Starting MCP server: {self.name}")
        
        # Prepare environment
        server_env = os.environ.copy()
        server_env.update(self.env)
        
        # Start server
        self.process = subprocess.Popen(
            [self.command] + self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=server_env,
            bufsize=1,  # Line buffered
        )
        
        print(f"   ✅ {self.name} started (PID: {self.process.pid})")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool via JSON-RPC.
        
        Args:
            tool_name: Name of the tool (e.g., "list_projects")
            arguments: Tool arguments
        
        Returns:
            Tool result
        """
        if not self.process:
            raise RuntimeError(f"MCP server {self.name} not started")
        
        self.request_id += 1
        
        # Construct JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Send request
        try:
            request_json = json.dumps(request) + "\n"
            self.process.stdin.write(request_json)
            self.process.stdin.flush()
            
            # Read response
            response_line = self.process.stdout.readline()
            response = json.loads(response_line)
            
            if "error" in response:
                raise RuntimeError(f"MCP error: {response['error']}")
            
            return response.get("result", {})
        
        except BrokenPipeError:
            raise RuntimeError(f"MCP server {self.name} crashed")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON from MCP server: {e}")
    
    def stop(self):
        """Stop the MCP server."""
        if self.process:
            print(f"🛑 Stopping MCP server: {self.name}")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None


class MCPManager:
    """
    Manages multiple MCP servers.
    
    User-friendly: Specify MCPs needed, manager handles everything!
    """
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
    
    def register_server(self, name: str, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
        """
        Register an MCP server.
        
        Args:
            name: Server name (e.g., "azure-devops", "playwright")
            command: Command to run (e.g., "npx")
            args: Command arguments
            env: Environment variables
        """
        server = MCPServer(name, command, args, env)
        self.servers[name] = server
    
    def start_all(self):
        """Start all registered MCP servers."""
        print("\n🚀 Starting MCP servers...")
        for server in self.servers.values():
            server.start()
        print()
    
    def stop_all(self):
        """Stop all MCP servers."""
        print("\n🛑 Stopping MCP servers...")
        for server in self.servers.values():
            server.stop()
        print()
    
    def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool.
        
        Args:
            server_name: Server name (e.g., "azure-devops")
            tool_name: Tool name (e.g., "search_workitem")
            arguments: Tool arguments
        
        Returns:
            Tool result
        """
        if server_name not in self.servers:
            raise ValueError(f"MCP server '{server_name}' not registered")
        
        return self.servers[server_name].call_tool(tool_name, arguments)
    
    def __enter__(self):
        """Context manager entry."""
        self.start_all()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_all()


def load_mcp_config_from_cursor() -> Dict[str, Any]:
    """
    Load MCP configuration from ~/.cursor/mcp.json.
    
    Returns:
        Dictionary of MCP server configurations
    """
    cursor_mcp_file = Path.home() / ".cursor" / "mcp.json"
    
    if not cursor_mcp_file.exists():
        print("ℹ️  No ~/.cursor/mcp.json found")
        return {}
    
    with open(cursor_mcp_file) as f:
        config = json.load(f)
    
    return config.get("mcpServers", {})


def create_mcp_manager_from_cursor_config() -> MCPManager:
    """
    Create MCP manager from Cursor's mcp.json configuration.
    
    Returns:
        Configured MCPManager ready to use
    """
    manager = MCPManager()
    
    cursor_config = load_mcp_config_from_cursor()
    
    for name, server_config in cursor_config.items():
        command = server_config.get("command", "npx")
        args = server_config.get("args", [])
        env = server_config.get("env", {})
        
        # Expand environment variables
        expanded_env = {}
        for key, value in env.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                expanded_env[key] = os.environ.get(env_var, "")
            else:
                expanded_env[key] = value
        
        manager.register_server(name, command, args, expanded_env)
    
    return manager


def create_minimal_mcp_manager() -> MCPManager:
    """
    Create MCP manager with minimal essential servers.
    
    For use when no ~/.cursor/mcp.json exists.
    """
    manager = MCPManager()
    
    # Puppeteer (browser automation)
    manager.register_server(
        "puppeteer",
        "npx",
        ["-y", "@modelcontextprotocol/server-puppeteer"]
    )
    
    # Playwright (alternative browser automation)
    manager.register_server(
        "playwright",
        "npx",
        ["-y", "@playwright/mcp@latest"]
    )
    
    # Azure DevOps (if PAT token available)
    if os.environ.get("AZURE_DEVOPS_PAT"):
        manager.register_server(
            "azure-devops",
            "npx",
            ["-y", "@azure-devops/mcp", os.environ.get("AZURE_DEVOPS_ORG", "")],
            {
                "AZURE_DEVOPS_PAT": os.environ["AZURE_DEVOPS_PAT"],
                "AZURE_DEVOPS_ORG": os.environ.get("AZURE_DEVOPS_ORG", ""),
            }
        )
    
    return manager

