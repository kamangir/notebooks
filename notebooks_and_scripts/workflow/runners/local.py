from typing import Any, List, Tuple
from abcli.modules import objects
from abcli import file
from notebooks_and_scripts.workflow.generic import Workflow
from notebooks_and_scripts.workflow.runners import RunnerType
from notebooks_and_scripts.workflow.runners.generic import GenericRunner
from notebooks_and_scripts.logger import logger


class LocalRunner(GenericRunner):
    def __init__(self, **kw_args):
        super().__init__(**kw_args)
        self.type: RunnerType = RunnerType.LOCAL

    def monitor(
        self,
        workflow: Workflow,
        hot_node: str = "void",
    ) -> bool:
        assert super().monitor(workflow, hot_node)

        return True

    def submit(
        self,
        workflow: Workflow,
        dryrun: bool = True,
    ) -> bool:
        assert super().submit(workflow, dryrun)

        return True

    def submit_command(
        self,
        command_line: str,
        job_name: str,
        dependencies: List[str],
        verbose: bool = False,
    ) -> Tuple[bool, Any]:
        super().submit_command(command_line, job_name, dependencies, verbose)

        filename = objects.path_of(f"{job_name}.sh", job_name)
        success, script = file.load_text(filename, civilized=True, log=True)
        if not success:
            script = ["#! /usr/bin/env bash", ""]

        script += [command_line]

        return file.save_text(filename, script), {"id": job_name}
