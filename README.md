# cursor-autonomous-harness

Production-ready autonomous coding harness using **Cursor CLI + Claude Code SDK**. Build complete applications autonomously with a two-agent pattern (initializer + coding agents).

**Proven Success:** Built [AutoGraph v3.0](https://github.com/nirmalarya/autograph) - 679 features, full-stack microservices platform.

---

## Features

- **Two-agent pattern**: Initializer (session 1) + Coding agents (sessions 2+)
- **Cursor CLI integration**: Uses `cursor agent --print --stream-json`
- **Feature-driven development**: Structured feature_list.json tracking
- **Session management**: Auto-resume with fresh context windows
- **Security**: Bash allowlist + filesystem sandbox
- **Git integration**: Automatic commits per session
- **Browser automation**: Puppeteer MCP for E2E testing
- **Progress tracking**: Real-time monitoring and logging

---

## Prerequisites

1. **Cursor CLI** installed and authenticated
   ```bash
   cursor --version
   # If not installed: https://cursor.sh/
   ```

2. **Python 3.11+**
   ```bash
   python3 --version
   ```

3. **Git** configured
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/nirmalarya/cursor-autonomous-harness.git
cd cursor-autonomous-harness

# Install dependencies
pip install -r requirements.txt

# Verify Cursor CLI works
cursor agent --help
```

---

## Usage

### Start New Project

```bash
python3 cursor_autonomous_agent.py --project-dir ./my-project

# The harness will:
# 1. Session 1: Generate feature_list.json from spec
# 2. Sessions 2+: Implement features autonomously
# 3. Auto-commit after each session
# 4. Continue until all features pass
```

### Continue Existing Project

```bash
# Just run the same command - auto-resumes!
python3 cursor_autonomous_agent.py --project-dir ./my-project
```

### Monitor Progress

```bash
# In another terminal
./monitor_progress.sh ./my-project

# Or check manually
cat ./my-project/cursor-progress.txt
cat ./my-project/feature_list.json | grep '"passes": true' | wc -l
```

---

## Project Structure

```
cursor-autonomous-harness/
├── cursor_autonomous_agent.py  # Main entry point
├── cursor_agent_runner.py      # Session management logic
├── anthropic_client.py          # Claude SDK + Cursor CLI wrapper
├── security.py                  # Bash allowlist & sandbox
├── progress.py                  # Progress tracking utilities
├── prompts.py                   # Prompt loading
├── prompts/
│   ├── app_spec.txt             # Example project spec
│   ├── initializer_prompt.md    # Session 1 prompt
│   └── coding_prompt.md         # Sessions 2+ prompt
├── requirements.txt             # Python dependencies
├── kill_cursor_agent.sh         # Emergency stop
├── monitor_progress.sh          # Progress monitoring
└── README.md                    # This file
```

**Excluded from repo:**
- `generations/` - Where built projects go (not committed)
- `cursor_test/` - Test artifacts
- Planning docs - Development notes

---

## How It Works

### Session 1: Initializer

1. Reads `app_spec.txt` (your project specification)
2. Generates comprehensive `feature_list.json` (100+ features)
3. Creates `init.sh` setup script
4. Initializes git repository

### Sessions 2+: Coding Agent

1. Reads `feature_list.json`
2. Finds next feature with `"passes": false`
3. Implements the feature
4. Tests thoroughly
5. Updates feature to `"passes": true`
6. Commits to git
7. Continues to next feature

**Runs autonomously until all features pass!**

---

## Configuration

### Security

Edit `security.py` to customize:
- Bash command allowlist
- Filesystem restrictions
- MCP server permissions

### Prompts

Edit prompts to customize:
- `prompts/initializer_prompt.md` - How features are generated
- `prompts/coding_prompt.md` - How features are implemented

### Project Spec

Create your own `app_spec.txt`:
```xml
<application_specification>
  <name>My App</name>
  <description>What it does</description>
  <features>
    <feature>User authentication</feature>
    <feature>Dashboard</feature>
    <!-- ... -->
  </features>
  <technology_stack>
    <backend>Python + FastAPI</backend>
    <frontend>React + Vite</frontend>
  </technology_stack>
</application_specification>
```

---

## Emergency Commands

```bash
# Stop the agent
./kill_cursor_agent.sh

# Or manually
ps aux | grep cursor_autonomous | grep -v grep | awk '{print $2}' | xargs kill

# Check progress
cat generations/my-project/cursor-progress.txt | tail -50
```

---

## Success Story: AutoGraph v3.0

**Built with cursor-autonomous-harness v1.0:**

- **Features:** 679/679 (100% complete)
- **Time:** ~35-40 hours autonomous coding (165 sessions)
- **Code:** 30,000+ lines Python + Next.js frontend
- **Architecture:** 10 microservices + PostgreSQL + Redis + MinIO
- **Result:** Full-stack AI-powered diagramming platform

**What was built:**
- User authentication & authorization
- TLDraw canvas integration
- AI-powered diagram generation
- Real-time collaboration (WebSockets)
- Export features (PNG, SVG, PDF, Mermaid)
- Cloud integrations (AWS S3, Dropbox, Google Drive)
- Version history & comments
- Advanced search & organization

**Quality:** B+ (8.5/10) - production-quality code, needs minor cleanup

---

## Comparison with autonomous-harness

**cursor-autonomous-harness** (this repo):
- Uses **Cursor CLI** (`cursor agent --print --stream-json`)
- Claude via Cursor's CLI interface
- Proven: Built AutoGraph (679 features)
- Best for: Cursor users, large projects

**autonomous-harness** (sister repo):
- Uses **Claude Code SDK** (direct API)
- Claude via Anthropic's SDK
- Proven: Built SHERPA (165 features)  
- Best for: API users, smaller projects

**Both use the same pattern:**
- Two-agent approach
- Feature-driven development
- Session management
- Git integration
- Security sandbox

---

## Requirements

- Python 3.11+
- Cursor CLI installed and authenticated
- Git configured
- 8GB+ RAM recommended (for large projects)
- Disk space for generated projects

---

## Troubleshooting

**Agent not starting:**
```bash
# Check Cursor CLI works
cursor agent --help

# Check authentication
cursor --version
```

**Out of memory:**
```bash
# Reduce context by splitting large features
# Or use smaller project scope
```

**Cursor streaming issues:**
```bash
# Use streaming client
python3 cursor_client_streaming.py --project-dir ./my-project
```

---

## Contributing

Based on Anthropic's autonomous-coding pattern. Enhancements welcome!

**Planned for v2.0:**
- Browser integration testing (CORS verification)
- Security checklist enforcement
- Puppeteer E2E testing (mandatory)
- Enhancement mode (brownfield support)
- Agent Skills support
- Stop condition (prevent scope creep)
- Zero TODOs policy

See `docs/v2/` for enhancement roadmap.

---

## License

MIT License

---

## Related Projects

- **autonomous-harness**: Claude Code SDK version
- **SHERPA**: Autonomous coding orchestrator (built with autonomous-harness)
- **AutoGraph**: AI diagramming platform (built with cursor-autonomous-harness)

---

## Acknowledgments

Based on Anthropic's autonomous-coding pattern and examples.
Uses Cursor CLI for agent interaction.

