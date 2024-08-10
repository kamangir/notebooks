from typing import Any, List, Tuple, Dict
import boto3
import glob
from tqdm import tqdm
from blueness import module
from abcli import file
from abcli import string
from abcli.modules import objects
from abcli.plugins.graphics.gif import generate_animated_gif
from abcli.plugins.metadata import post_to_object
from notebooks_and_scripts import NAME
from notebooks_and_scripts.logger import logger
from notebooks_and_scripts.workflow import dot_file
from notebooks_and_scripts.workflow.generic import Workflow
from notebooks_and_scripts.workflow.runners.factory import RunnerType


NAME = module.name(__file__, NAME)


class GenericRunner:
    def __init__(self):
        self.type: RunnerType = RunnerType.GENERIC
        self.job_name: str = ""

    def monitor(
        self,
        workflow: Workflow,
        hot_node: str = "void",
    ) -> bool:
        self.job_name = workflow.job_name

        try:
            workflow = self.monitor_function(workflow)
        except Exception as e:
            logger.warning(f"monitor failed: {e}")

        summary: Dict[str, str] = {}
        for node in workflow.G.nodes:
            summary.setdefault(workflow.G.nodes[node].get("status"), []).append(node)
        for status, nodes in summary.items():
            logger.info("{}: {}".format(status, ", ".join(sorted(nodes))))

        if not dot_file.export_graph_as_image(
            workflow.G,
            objects.path_of(
                "workflow-{}.png".format(
                    string.pretty_date(as_filename=True, unique=True),
                ),
                workflow.job_name,
            ),
            colormap=dot_file.status_color_map,
            hot_node=hot_node,
        ):
            return False

        return generate_animated_gif(
            [
                filename
                for filename in sorted(
                    glob.glob(objects.path_of("workflow-*.png", workflow.job_name))
                )
                if len(file.name(filename)) > 15
            ],
            objects.path_of("workflow.gif", workflow.job_name),
            frame_duration=333,
        )

    def monitor_function(self, workflow: Workflow) -> Workflow:
        logger.info(f"{NAME}.{self.__class__.__name__}.monitor: {workflow}")
        return workflow

    def submit(
        self,
        workflow: Workflow,
        dryrun: bool = True,
    ) -> bool:
        self.job_name = workflow.job_name

        logger.info(
            "{}.{}.submit({}, dryrun={})".format(
                NAME,
                self.__class__.__name__,
                workflow.G,
                dryrun,
            )
        )

        metadata: Dict[str, Any] = {}
        failure_count: int = 0
        round: int = 1
        while not all(
            workflow.G.nodes[node].get("job_id") for node in workflow.G.nodes
        ):
            for node in tqdm(workflow.G.nodes):
                if workflow.G.nodes[node].get("job_id"):
                    continue

                pending_dependencies = [
                    node_
                    for node_ in workflow.G.successors(node)
                    if not workflow.G.nodes[node_].get("job_id")
                ]
                if pending_dependencies:
                    logger.info(
                        '⏳ node "{}": {} pending dependenci(es): {}'.format(
                            node,
                            len(pending_dependencies),
                            ", ".join(pending_dependencies),
                        )
                    )
                    continue

                command_line = workflow.G.nodes[node]["command_line"]
                job_name = f"{workflow.job_name}-{node}"

                if dryrun:
                    workflow.G.nodes[node]["job_id"] = f"dryrun-round-{round}"
                    logger.info(f"{command_line} -> {job_name}")
                    continue

                success, metadata[node] = self.submit_command(
                    command_line=command_line,
                    job_name=job_name,
                    dependencies=[
                        workflow.G.nodes[node_].get("job_id")
                        for node_ in workflow.G.successors(node)
                    ],
                    verbose=False,
                )
                if not success:
                    failure_count += 1

                workflow.G.nodes[node]["job_id"] = (
                    metadata[node]["job_id"] if success else "failed"
                )

            logger.info(f"end of round {round}")
            round += 1

        if failure_count:
            logger.error(f"{failure_count} failure(s).")

        if not dot_file.save_to_file(
            objects.path_of("workflow.dot", workflow.job_name),
            workflow.G,
        ):
            return False

        if not post_to_object(
            workflow.job_name,
            "submission",
            {
                "metadata": metadata,
                "failure_count": failure_count,
                "runner_type": self.type.name.lower(),
            },
        ):
            return False

        return failure_count == 0

    def submit_command(
        self,
        command_line: str,
        job_name: str,
        dependencies: List[str],
        verbose: bool = False,
    ) -> Tuple[bool, Any]:
        logger.info(
            "⏳ {}.{}: {} @ {} X {}: {}".format(
                NAME,
                self.__class__.__name__,
                job_name,
                command_line,
                len(dependencies),
                ", ".join(dependencies),
            )
        )
        return True, {"job_id": job_name}
