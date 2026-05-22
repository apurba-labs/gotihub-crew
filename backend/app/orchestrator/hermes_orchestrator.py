from typing import Dict

from app.agents.security_agent import SecurityAgent
from app.agents.architecture_agent import (
    ArchitectureAgent,
)


class HermesOrchestrator:

    def __init__(self):

        self.security_agent = SecurityAgent()
        self.architecture_agent = ArchitectureAgent()

    async def run_analysis(
        self,
        repository_files: Dict[str, str]
    ):

        security_report = await (
            self.security_agent.analyze(repository_files)
        )

        architecture_report = await (
            self.architecture_agent.analyze(
                repository_files
            )
        )

        return {
            "security_report": security_report,
            "architecture_report": architecture_report,
        }