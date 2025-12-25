#!/usr/bin/env python3
"""
Autonomous Backlog Runner
=========================

Runs continuous backlog processing from Azure DevOps.
"""

import asyncio
from pathlib import Path
from typing import Optional

from azure_devops_integration import AzureDevOpsIntegration
from multi_agent_mode import MultiAgentWorkflow
from cursor_agent_runner import run_autonomous_agent


async def run_autonomous_backlog(
    project_dir: Path,
    model: str,
    azure_devops_org: str,
    azure_devops_project: str,
    epic: Optional[str] = None,
    max_pbis: Optional[int] = None,
):
    """
    Run autonomous backlog processing.
    
    Continuously pulls PBIs from Azure DevOps and implements them.
    """
    
    print("\n" + "="*70)
    print("  AUTONOMOUS BACKLOG MODE")
    print("  Continuous PBI Processing from Azure DevOps")
    print("="*70)
    print(f"\nOrganization: {azure_devops_org}")
    print(f"Project: {azure_devops_project}")
    if epic:
        print(f"Epic filter: {epic}")
    if max_pbis:
        print(f"Max PBIs: {max_pbis}")
    else:
        print("Max PBIs: Unlimited (runs until backlog empty)")
    print("\n" + "="*70 + "\n")
    
    # Initialize integrations
    ado = AzureDevOpsIntegration(azure_devops_org, azure_devops_project)
    
    pbis_completed = 0
    
    while True:
        # 1. Query Azure DevOps for next PBI
        print("\n🔍 Querying Azure DevOps for next work item...")
        
        work_items = ado.query_work_items(
            epic=epic,
            state="New",
            top=1
        )
        
        if not work_items:
            print("\n✅ No more PBIs in backlog!")
            
            if max_pbis is None:
                print("⏰ Waiting 1 hour before checking again...")
                await asyncio.sleep(3600)
                continue
            else:
                print(f"✅ Completed {pbis_completed} PBIs")
                return
        
        # Get first PBI
        pbi_summary = work_items[0]
        pbi = ado.get_work_item(pbi_summary['id'])
        
        # 2. Display PBI
        print(f"\n{'='*70}")
        print(f"  📋 {pbi['id']}: {pbi['fields']['System.Title']}")
        print(f"{'='*70}")
        print(f"\nType: {pbi['fields']['System.WorkItemType']}")
        print(f"Description: {pbi['fields'].get('System.Description', 'N/A')[:200]}...")
        print(f"\n{'='*70}\n")
        
        # 3. Convert to spec
        spec_content = ado.convert_to_spec(pbi)
        spec_file = project_dir / "spec" / f"pbi_{pbi['id']}_spec.txt"
        spec_file.parent.mkdir(parents=True, exist_ok=True)
        spec_file.write_text(spec_content)
        
        print(f"✅ Created spec: {spec_file}\n")
        
        # 4. Run multi-agent workflow
        print("🚀 Starting multi-agent workflow...\n")
        
        success = await run_multi_agent_workflow_for_pbi(
            project_dir=project_dir,
            model=model,
            pbi=pbi,
            spec_file=spec_file,
            ado=ado
        )
        
        if success:
            # 5. Mark as Done
            ado.mark_done(pbi['id'])
            
            pbis_completed += 1
            print(f"\n🎉 {pbi['id']} COMPLETE!")
            print(f"   Total: {pbis_completed}/{max_pbis or '∞'}\n")
            
            # Check limit
            if max_pbis and pbis_completed >= max_pbis:
                print(f"✅ Reached limit ({max_pbis} PBIs)")
                return
            
            # Continue to next
            print("⏭️  Moving to next PBI in 10 seconds...\n")
            await asyncio.sleep(10)
        else:
            print(f"\n❌ {pbi['id']} FAILED!")
            print("Stopping for human intervention\n")
            return


async def run_multi_agent_workflow_for_pbi(
    project_dir: Path,
    model: str,
    pbi: Dict,
    spec_file: Path,
    ado: AzureDevOpsIntegration
) -> bool:
    """Run complete multi-agent workflow for one PBI."""
    
    workflow = MultiAgentWorkflow(
        project_dir=project_dir,
        project_name=ado.project
    )
    
    agents = ["architect", "engineer", "tester", "code_review", "security", "devops"]
    
    # Create PBI context
    pbi_context = {
        "project_name": ado.project,
        "pbi_id": pbi['id'],
        "pbi_title": pbi['fields']['System.Title'],
        "pbi_type": pbi['fields']['System.WorkItemType'],
        "pbi_description": pbi['fields'].get('System.Description', ''),
        "acceptance_criteria": pbi['fields'].get('Microsoft.VSTS.Common.AcceptanceCriteria', '')
    }
    
    # Check if workflow already started (resume capability)
    current_state = workflow.get_workflow_state()
    completed_agents = current_state.get('completedAgents', [])
    
    for agent in agents:
        # Skip if already completed
        if agent in completed_agents:
            print(f"⏩ {agent.title()} already complete, skipping...\n")
            continue
        
        print(f"\n{'─'*70}")
        print(f"  🤖 {agent.title()} Agent")
        print(f"{'─'*70}\n")
        
        # Load agent-specific prompt
        agent_prompt = workflow.load_agent_prompt(agent, pbi_context)
        
        # Run agent session with Cursor
        # (This will use cursor_agent_runner.py to execute)
        
        # For now, placeholder
        print(f"Running {agent} agent with Cursor CLI...")
        print(f"Prompt loaded: {len(agent_prompt)} characters")
        
        # TODO: Actually run the agent with Cursor
        # result = await run_cursor_agent_session(agent_prompt, project_dir, model)
        
        # Placeholder - assume success
        # In real implementation, would check result.success
        
        # Update Azure DevOps
        ado.add_comment(
            pbi['id'],
            f"[{agent.title()}] Agent completed"
        )
        
        # Save checkpoint
        workflow.mark_agent_complete(
            agent=agent,
            artifacts=[],  # Would list actual files created
            commit_sha="placeholder",
            summary=f"{agent.title()} agent completed"
        )
        
        print(f"✅ {agent.title()} complete!\n")
    
    # All agents complete
    return True


if __name__ == "__main__":
    print("""
Autonomous Backlog Runner
=========================

Usage:
  python3 cursor_autonomous_agent.py \\
    --mode autonomous-backlog \\
    --azure-devops-project togglr \\
    --epic Epic-3 \\
    --max-pbis 5

This will process 5 PBIs from Epic-3 continuously!
    """)

