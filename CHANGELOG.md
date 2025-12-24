# Changelog

All notable changes to cursor-autonomous-harness will be documented in this file.

## [1.0.0] - 2024-12-24

### 🎉 Initial Release - AutoGraph v3.0 Success

First production-ready release of cursor-autonomous-harness.
Successfully built AutoGraph v3.0 - a complete full-stack microservices platform!

### Features

#### Core Harness
- Two-agent pattern (Initializer + Coding agents)
- Cursor CLI integration (`cursor agent --print --stream-json`)
- Feature-driven development (feature_list.json)
- Session management with fresh context windows
- Auto-resume between sessions (3s delay)
- Git integration with automatic commits
- Progress tracking via cursor-progress.txt
- Comprehensive security model (sandbox + allowlist)

#### Cursor CLI Integration
- Streaming JSON output for real-time monitoring
- Chat ID management for session continuity
- Error handling and retries
- Process management and cleanup

#### Security
- Bash command allowlist (security.py)
- Filesystem sandbox restrictions
- MCP server integration (Puppeteer for browser testing)
- Credential handling

#### Developer Experience
- Progress monitoring script
- Emergency kill switch
- Real-time logging
- Session progress tracking

### Built with This Harness

**AutoGraph v3.0:**
- 679/679 features (100% complete)
- 10 microservices architecture
- 30,000+ lines of code
- FastAPI backends + Next.js frontend
- TLDraw canvas integration
- Real-time collaboration
- AI-powered diagram generation
- Cloud integrations (AWS, Dropbox, Google Drive)
- Comprehensive export features

**Quality:** B+ (8.5/10) - production-quality, needs v3.1 cleanup

**Time:** ~35-40 hours autonomous coding (165 sessions)

### Known Limitations (v1.0)

- No brownfield/enhancement mode (greenfield only)
- No stop condition (continues after 100%)
- No browser integration testing (CORS issues missed)
- No security gates (some issues not caught)
- No TODO prevention policy (3 TODOs remained)
- No Agent Skills support

**Planned for v2.0:** All above limitations will be addressed.

---

## [Unreleased] - v2.0 Roadmap

### Planned Enhancements

**Quality Gates:**
- Browser integration testing (CORS verification)
- Security checklist (prevent credential leaks)
- Zero TODOs policy
- Stop condition (exit at 100%)
- File organization rules

**Enhanced Testing:**
- Puppeteer E2E mandatory
- DevTools verification
- Regression testing framework

**New Capabilities:**
- Enhancement mode (brownfield support!)
- Agent Skills integration (universal format!)
- Linear tracker integration
- GitHub Issues integration

See `docs/v2/` for detailed roadmap.

