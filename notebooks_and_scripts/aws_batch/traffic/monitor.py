import boto3
from tqdm import tqdm
from abcli import string
from abcli.modules import objects
from abcli.plugins.metadata import get, MetadataSourceType
from notebooks_and_scripts.logger import logger
from notebooks_and_scripts.aws_batch.dot_file import (
    load_from_file,
    export_graph_as_image,
    status_color_map,
)


def monitor_traffic(
    job_name: str,
    verbose: bool = False,
) -> bool:
    pattern = get(
        "traffic.pattern",
        "",
        job_name,
        MetadataSourceType.OBJECT,
    )

    success, G = load_from_file(objects.path_of(f"{pattern}.dot", job_name))
    if not success:
        return success

    logger.info(f"monitor_traffic: {job_name} @ {pattern}: {G}")

    client = boto3.client("batch")

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/describe_jobs.html
    page_size = 100
    for index in tqdm(range(0, len(G.nodes), page_size)):
        nodes = list(G.nodes)[index : index + page_size]

        jobs = [G.nodes[node].get("job_id").replace('"', "") for node in nodes]

        response = client.describe_jobs(jobs=jobs)

        for node, status in zip(
            nodes,
            [item["status"] for item in response["jobs"]],
        ):
            G.nodes[node]["status"] = status

            if verbose:
                logger.info(f"{node}: {status}")

    return export_graph_as_image(
        G,
        objects.path_of(
            "history/{}-{}.png".format(
                pattern,
                string.pretty_date(as_filename=True, unique=True),
            ),
            job_name,
        ),
        colormap=status_color_map,
    )
