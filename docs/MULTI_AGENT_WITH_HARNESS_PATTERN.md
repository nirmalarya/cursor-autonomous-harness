# Multi-Agent Workflow + Anthropic Harness Pattern

**Critical:** Multi-agent mode MUST respect the initializer/coder pattern!

---

## 🎯 The Anthropic Harness Pattern

**Foundation of autonomous-harness:**

```
Session 1: INITIALIZER
- Generate feature_list.json
- Plan the work
- Set up structure

Session 2+: CODER
- Implement features one by one
- Test each feature
- Mark as passing when verified
```

**This pattern is SACRED - don't break it!**

---

## ❌ WRONG Approach (Bypasses Pattern):

```python
# DON'T DO THIS!
for agent in ["Architect", "Engineer", "Tester"]:
    run_single_session(agent_prompt)  # One session per agent
```

**Problems:**
- Skips initializer (no feature planning!)
- One session per agent (what if agent needs multiple sessions?)
- No feature tracking (feature_list.json)
- Bypasses quality gates

---

## ✅ CORRECT Approach (Respects Pattern):

**Each Agent = Mini Autonomous Project**

### **Architect Agent:**

```
Session 1 (Initializer): 
- Generate feature_list.json for Architect tasks:
  * Feature #1: Research technical approaches
  * Feature #2: Design API contracts
  * Feature #3: Design database schema
  * Feature #4: Create ADR document
  * Feature #5: Review and finalize

Session 2-6 (Coder):
- Implement each feature
- Mark as passing
- When 5/5: Architect complete!
```

### **Engineer Agent:**

```
Session 1 (Initializer):
- Read ADR from Architect
- Generate feature_list.json for Engineer tasks:
  * Feature #1: Write failing tests (RED)
  * Feature #2: Implement minimum code (GREEN)
  * Feature #3: Refactor while keeping tests green
  * Feature #4: Add edge case tests
  * Feature #5: Achieve ≥80% coverage

Session 2-10 (Coder):
- Implement TDD cycle
- Mark features passing
- When 5/5: Engineer complete!
```

### **Tester Agent:**

```
Session 1 (Initializer):
- Generate feature_list.json for Tester tasks:
  * Feature #1: Run unit tests, verify ≥80%
  * Feature #2: Create E2E test with Playwright
  * Feature #3: Test edge cases
  * Feature #4: Verify regression (existing features)
  * Feature #5: Grade implementation (A/B/C/D/F)

Session 2-8 (Coder):
- Create E2E tests
- Run all tests
- Grade implementation
- When 5/5: Tester complete!
```

**Same for CodeReview, Security, DevOps agents!**

---

## 🔄 Multi-Agent Workflow Implementation

**Correct architecture:**

```python
async def run_multi_agent_workflow(pbi, spec_file):
    """Run PBI through all agents, respecting harness pattern."""
    
    agents = ["Architect", "Engineer", "Tester", "CodeReview", "Security", "DevOps"]
    
    for agent in agents:
        print(f"\n{'='*70}")
        print(f"  🤖 {agent} Agent")
        print(f"{'='*70}\n")
        
        # Load agent-specific rules
        agent_rules = load_agent_rules(agent)
        
        # Create agent-specific spec (PBI context + agent rules)
        agent_spec = create_agent_spec(pbi, spec_file, agent, agent_rules)
        
        # Run FULL harness for this agent (initializer + coders!)
        # This respects the Anthropic pattern!
        await run_autonomous_agent(
            project_dir=project_dir,
            mode="enhancement",  # Agent adds to existing project
            spec_file=agent_spec,
            max_iterations=50,  # Allow multiple sessions per agent
            agent_context=agent  # Flag that we're in multi-agent mode
        )
        
        # Agent ran through full pattern:
        # - Session 1: Initializer (planned agent tasks)
        # - Session 2+: Coder (implemented tasks)
        # - Stopped at 100% automatically
        
        # Check if agent passed
        agent_result = check_agent_completion(agent)
        
        if not agent_result.passed:
            print(f"❌ {agent} failed quality gates!")
            return False
        
        # Update Azure DevOps
        update_ado(pbi['id'], f"[{agent}] Complete")
        
        print(f"✅ {agent} complete!\n")
    
    # All agents passed!
    return True
```

---

## 🎯 Key Insight:

**Multi-agent workflow is NOT:**
```
6 sessions (one per agent)
```

**Multi-agent workflow IS:**
```
6 * N sessions (each agent runs full harness pattern)

Architect: 1 initializer + 5 coder sessions
Engineer: 1 initializer + 10 coder sessions
Tester: 1 initializer + 8 coder sessions
CodeReview: 1 initializer + 3 coder sessions
Security: 1 initializer + 3 coder sessions  
DevOps: 1 initializer + 3 coder sessions

Total: ~35-50 sessions per PBI
```

**Each agent gets multiple sessions to complete its work!**

---

## ✅ Benefits of Respecting the Pattern:

- ✅ Each agent can take as long as needed
- ✅ Feature tracking (feature_list.json per agent)
- ✅ Quality gates enforced
- ✅ Automatic stop when agent done
- ✅ Resumable if interrupted
- ✅ Consistent with harness foundation

---

**This is the CORRECT architecture - respect the Anthropic pattern!** 🎯

