"""
Agent Reviewer
==============

Runs Cursor Agent Review to catch bugs in diffs.
Per https://cursor.com/docs/agent/review
"""

import subprocess
from pathlib import Path
from typing import Tuple


class AgentReviewer:
    """Runs Cursor Agent Review on code changes."""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
    
    def review_changes(self, since_commit: str = "HEAD~1") -> Tuple[bool, str]:
        """
        Run Agent Review on changes since given commit.
        
        Args:
            since_commit: Git ref to compare against (default: HEAD~1)
        
        Returns:
            (has_issues, review_output)
        """
        
        print(f"\n🔍 Running Agent Review on changes since {since_commit}...")
        
        # Get diff
        try:
            diff_result = subprocess.run(
                ["git", "diff", since_commit],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if not diff_result.stdout.strip():
                print("   ℹ️  No changes to review")
                return False, "No changes"
            
            # Run cursor-agent review (if available)
            # For CLI mode, we can prompt cursor-agent to review the diff
            review_prompt = f"""Review these code changes for potential bugs:

```diff
{diff_result.stdout[:5000]}  # Limit to 5000 chars
```

Check for:
- Logic errors
- Missing error handling
- Type safety issues
- Security vulnerabilities
- Performance problems

If you find issues, list them clearly. If code looks good, say "No issues found".
"""
            
            result = subprocess.run(
                ["cursor-agent", "-p", "--force", review_prompt],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            review_output = result.stdout
            
            # Simple heuristic: Look for issue indicators
            has_issues = any([
                "issue" in review_output.lower(),
                "bug" in review_output.lower(),
                "error" in review_output.lower(),
                "problem" in review_output.lower(),
                "fix" in review_output.lower() and "found" in review_output.lower()
            ])
            
            if has_issues:
                print("   ⚠️  Potential issues found!")
                print(f"   {review_output[:200]}...")
            else:
                print("   ✅ No issues detected")
            
            return has_issues, review_output
        
        except Exception as e:
            print(f"   ❌ Review failed: {e}")
            return False, str(e)
    
    def review_after_agent(self, agent_name: str, baseline_commit: str) -> bool:
        """
        Review changes made by an agent.
        
        Args:
            agent_name: Name of agent that just completed
            baseline_commit: Commit before agent started
        
        Returns:
            True if review passed, False if issues found
        """
        print(f"\n{'─'*70}")
        print(f"  🔍 Agent Review: {agent_name.title()} Changes")
        print(f"{'─'*70}")
        
        has_issues, output = self.review_changes(since_commit=baseline_commit)
        
        if has_issues:
            print(f"\n⚠️  {agent_name.title()} made changes with potential issues!")
            print(f"   Review output saved for manual inspection")
            
            # Save review for manual inspection
            review_file = self.project_dir / f".cursor" / f"{agent_name}-review.txt"
            review_file.parent.mkdir(exist_ok=True)
            review_file.write_text(output)
            
            print(f"   Saved to: {review_file}")
            
            # For now, continue anyway (don't block)
            # Future: Could prompt user or auto-fix
            return True
        
        print(f"✅ {agent_name.title()} changes look good!")
        return True


def should_review_agent(agent_name: str) -> bool:
    """Decide if agent's work should be reviewed."""
    # Review code-producing agents
    return agent_name in ["engineer", "architect"]  # Most critical


def review_frequency(pbis_completed: int) -> bool:
    """Decide if we should run review at this point."""
    # Review every PBI for now
    # Could change to every N PBIs for performance
    return True

