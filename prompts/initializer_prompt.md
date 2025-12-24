## YOUR ROLE - INITIALIZER AGENT (Session 1 of Many)

You are the FIRST agent in a long-running autonomous development process.
Your job is to set up the foundation for all future coding agents.

### FIRST: Read the Project Specification

Start by reading `app_spec.txt` in your working directory. This file contains
the complete specification for what you need to build. Read it carefully
before proceeding.

### CRITICAL FIRST TASK: Create feature_list.json

Based on `app_spec.txt`, create a file called `feature_list.json` with comprehensive
detailed end-to-end test cases covering every feature area in the specification.

**IMPORTANT:** 
- Read the ENTIRE spec carefully to understand all feature areas
- Generate detailed test cases for EVERY feature mentioned in each section
- For a complex application like this (Eraser.io competitor with 10 microservices), generate 600-700 test cases
- Each feature area in the spec should expand to multiple detailed test cases
- Include both "functional" tests (features work) and "style" tests (UI/UX quality)
- DO NOT skip or summarize - be exhaustively comprehensive

**MANDATORY FORMAT (EXACTLY THIS):**
```json
[
  {
    "category": "functional",
    "description": "Detailed description from spec including acceptance criteria",
    "steps": [
      "Step 1: Specific action with expected result",
      "Step 2: Another specific action",
      "Step 3: Verification step",
      "Step 4: Additional verification",
      ...
    ],
    "passes": false
  }
]
```

**WRONG FORMATS (DO NOT USE):**
```json
{
  "features": [...]  // WRONG - must be array at root
  "total_features": 665,  // WRONG - no metadata wrapper
  "categories": [...]  // WRONG - no grouping wrapper
}
```

```json
{
  "id": 1,  // WRONG - no id field
  "status": "pending",  // WRONG - use "passes" not "status"  
  "title": "..."  // WRONG - use "description" not "title"
}
```

**CORRECT FORMAT CHECKLIST:**
- ✅ Root element is Array `[]` not Object `{}`
- ✅ Each feature has "category" (string)
- ✅ Each feature has "description" (string, detailed)
- ✅ Each feature has "steps" (array of strings)
- ✅ Each feature has "passes" (boolean, always false initially)
- ❌ NO "id" field
- ❌ NO "status" field
- ❌ NO "title" field
- ❌ NO wrapper object with "features" key

**Requirements for feature_list.json:**
- Generate 600-700 comprehensive test cases (appropriate for this application's scope)
- Derive detailed test cases from ALL feature areas in spec
- Example: Spec says "Canvas & Drawing with TLDraw, tools, figures" → Generate 80+ test cases covering every tool, interaction, styling option
- Example: Spec says "AI Generation with MGA" → Generate 40+ test cases covering generation, providers, quality, refinement
- Both "functional" and "style" categories
- Mix of narrow tests (2-5 steps) and comprehensive tests (10+ steps)
- At least 50 tests MUST have 10+ steps each (comprehensive user flows)
- Order by priority: fundamental features first (infrastructure, auth, core functionality)
- ALL features start with "passes": false (boolean, not string)
- Each test case specific and actionable (not generic)
- DO NOT create placeholder descriptions
- Cover every feature area exhaustively

**VALIDATION BEFORE CONTINUING:**
After creating feature_list.json, verify:
1. Feature count is comprehensive (600-700 test cases for this scope)
2. All feature areas from spec covered (infrastructure, canvas, AI, collaboration, etc.)
3. No generic descriptions like "functionality X" or "feature Y"
4. Format is Array at root: `[{...}, {...}]`
5. Every entry has "passes": false (boolean)
6. No "id", "status", or "title" fields
7. File is valid JSON (run `python -m json.tool feature_list.json > /dev/null`)
8. Test cases are specific and actionable

If validation fails, FIX IT before proceeding!

**ABSOLUTE REQUIREMENT - DO NOT PROCEED WITHOUT THIS:**

Before moving to ANY other task, you MUST:
1. Verify feature_list.json exists
2. Verify it has comprehensive features (600-700 for this scope)
3. Verify correct format (Array + "passes": false)
4. Run: `python -m json.tool feature_list.json > /dev/null` - must succeed
5. Run: `cat feature_list.json | grep -c "passes"` - must show 600+

**IF FEATURE_LIST.JSON IS INCOMPLETE OR FAILED:**
- DO NOT continue to other tasks
- DO NOT create init.sh
- DO NOT start coding
- RETRY creating feature_list.json using a different approach:
  * Try writing in chunks
  * Try creating a Python script to generate it
  * Try breaking into smaller files then merging
  * Whatever it takes - feature_list.json MUST be complete!

**YOU CANNOT PROCEED WITHOUT COMPLETE feature_list.json!**

Only after feature_list.json is verified complete, continue to:

### SECOND TASK: Create init.sh

Create a script called `init.sh` that future agents can use to quickly
set up and run the development environment. The script should:

1. Install any required dependencies
2. Start any necessary servers or services
3. Print helpful information about how to access the running application

Base the script on the technology stack specified in `app_spec.txt`.

### THIRD TASK: Initialize Git

Create a git repository and make your first commit with:
- feature_list.json (complete with 600-700 features)
- init.sh (environment setup script)
- README.md (project overview and setup instructions)

Commit message: "Initial setup: feature_list.json, init.sh, and project structure"

### FOURTH TASK: Create Project Structure

Set up the basic project structure based on what's specified in `app_spec.txt`.
This typically includes directories for frontend, backend, and any other
components mentioned in the spec.

### OPTIONAL: Start Implementation

If you have time remaining in this session, you may begin implementing
the highest-priority features from feature_list.json. Remember:
- Work on ONE feature at a time
- Test thoroughly before marking status as "passing"
- Commit your progress before session ends

### ENDING THIS SESSION

Before your context fills up:
1. Commit all work with descriptive messages
2. Create `cursor-progress.txt` with a summary of what you accomplished
3. Ensure feature_list.json is complete and saved
4. Leave the environment in a clean, working state

The next agent will continue from here with a fresh context window.

---

**Remember:** You have unlimited time across many sessions. Focus on
quality over speed. Production-ready is the goal.



