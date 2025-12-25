# TODO: Complete Togglr Integration

**Status:** Architecture complete, need final wiring

---

## ✅ What's Done:

1. ✅ Multi-agent prompts (6 agents)
2. ✅ Azure DevOps fetcher prompt
3. ✅ Workflow state management
4. ✅ Autonomous backlog runner structure
5. ✅ Arguments (--mode, --azure-devops-project, etc.)
6. ✅ Routing logic
7. ✅ Respects Anthropic harness pattern

---

## ⏳ What's Needed (2-3 hours):

### **1. Implement `run_fetcher_session()`** (30 min)

```python
# In autonomous_backlog_runner.py

async def run_fetcher_session(...):
    """Run Cursor session with azure_devops_fetcher_prompt.md"""
    
    # Load fetcher prompt
    fetcher_prompt = load_prompt("azure_devops_fetcher_prompt")
    
    # Replace placeholders
    fetcher_prompt = fetcher_prompt.replace("{{PROJECT_NAME}}", ado_project)
    fetcher_prompt = fetcher_prompt.replace("{{ORGANIZATION}}", ado_org)
    fetcher_prompt = fetcher_prompt.replace("{{EPIC}}", epic or "")
    
    # Run Cursor session (agent uses MCP tools to fetch PBI)
    result = await run_cursor_cli_session(
        prompt=fetcher_prompt,
        project_dir=project_dir,
        model=model
    )
    
    # Check if spec file was created
    spec_files = list(project_dir.glob("spec/*_spec.txt"))
    if spec_files:
        latest_spec = max(spec_files, key=lambda p: p.stat().st_mtime)
        pbi_id = latest_spec.stem.replace("_spec", "")
        return {"pbi_id": pbi_id, "spec_file": latest_spec}
    
    return None
```

---

### **2. Implement `create_agent_spec()`** (30 min)

```python
async def create_agent_spec(project_dir, pbi_spec_file, agent, model):
    """Create agent-specific spec (PBI + agent rules)."""
    
    # Read PBI spec
    pbi_spec = pbi_spec_file.read_text()
    
    # Load agent rules
    agent_rules_file = Path("prompts/multi-agent") / f"{agent}_agent.md"
    agent_rules = agent_rules_file.read_text()
    
    # Combine into agent-specific spec
    agent_spec = f"""
{pbi_spec}

---

# Agent-Specific Instructions

{agent_rules}

---

# Task Breakdown

Generate feature_list.json for {agent.upper()} agent tasks.

For example, if {agent} is "Engineer":
- Feature #1: Write failing tests (RED)
- Feature #2: Implement code (GREEN)  
- Feature #3: Refactor (REFACTOR)
- Feature #4: Edge cases
- Feature #5: Coverage ≥80%

Mark each complete as you finish!
"""
    
    # Save agent spec
    agent_spec_file = project_dir / "spec" / f"{agent}_spec.txt"
    agent_spec_file.write_text(agent_spec)
    
    return agent_spec_file
```

---

### **3. Helper Functions** (30 min)

```python
def get_latest_commit():
    """Get latest git commit SHA."""
    import subprocess
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        cwd=project_dir
    )
    return result.stdout.strip()

async def run_cursor_cli_session(prompt, project_dir, model):
    """Run single Cursor CLI session."""
    # Use existing cursor_client_streaming.py
    from cursor_client_streaming import CursorAgentClient
    
    client = CursorAgentClient(project_dir, model, None)
    result = await client.run_session(prompt)
    
    return result
```

---

### **4. Update Prompts for Agent Context** (30 min)

Add to each agent prompt (architect, engineer, etc.):

```markdown
## Context

You are running as the **{{AGENT_NAME}}** agent in a multi-agent workflow.

**Your specific responsibilities:**
[Agent-specific role description]

**Previous agents completed:**
{{COMPLETED_AGENTS}}

**Artifacts from previous agents:**
{{ARTIFACTS}}

Generate feature_list.json for YOUR agent tasks only!
```

---

### **5. Testing** (30 min)

```bash
# Test on one PBI
python3 cursor_autonomous_agent.py \
  --mode autonomous-backlog \
  --project-dir /Users/nirmalarya/Workspace/togglr \
  --azure-devops-project togglr \
  --max-pbis 1

# Watch:
# 1. Fetcher session (uses MCP)
# 2. Architect sessions (initializer + coders)
# 3. Engineer sessions (initializer + coders)
# etc.
```

---

## 📊 Estimated Work:

- Implement functions: 2 hours
- Testing & debugging: 1 hour
- **Total: 3 hours**

Then: **Ready to process Togglr Epic 3 backlog!** 🎯

---

## 🎊 The Vision (Once Complete):

```bash
# Process entire Epic 3 (20 PBIs)
python3 cursor_autonomous_agent.py \
  --mode autonomous-backlog \
  --project-dir /Users/nirmalarya/Workspace/togglr \
  --azure-devops-project togglr \
  --epic Epic-3 \
  --max-pbis 20

# Runs for days...
# Implements 20 PBIs autonomously!
# Updates Azure DevOps continuously!
# No human intervention needed!
```

**Fully autonomous enterprise SDLC!** 🚀

