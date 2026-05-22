from typing import Dict, List

from app.schemas.report_schema import (
    AgentIssue,
    AgentReport,
)


class ArchitectureAgent:

    async def analyze(
        self,
        repository_files: Dict[str, str]
    ) -> AgentReport:

        issues: List[AgentIssue] = []

        file_paths = list(repository_files.keys())

        # Simple heuristic checks
        if len(file_paths) < 5:
            issues.append(
                AgentIssue(
                    title="Minimal Project Structure",
                    severity="medium",
                    description=(
                        "Repository contains very few files."
                    ),
                    recommendation=(
                        "Consider improving modularity and "
                        "project organization."
                    ),
                )
            )

        has_readme = any(
            "readme" in path.lower()
            for path in file_paths
        )

        if not has_readme:
            issues.append(
                AgentIssue(
                    title="Missing Documentation",
                    severity="low",
                    description=(
                        "README documentation not detected."
                    ),
                    recommendation=(
                        "Add project documentation for "
                        "developer onboarding."
                    ),
                )
            )

        summary = (
            "Architecture review completed successfully."
        )

        return AgentReport(
            agent_name="Architecture Agent",
            summary=summary,
            score=max(0, 100 - (len(issues) * 10)),
            issues=issues,
        )