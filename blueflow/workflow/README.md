# 📜 workflow

an abstraction to run mixed-type (cpu/gpu/...) [DAG](https://networkx.org/documentation/stable/reference/classes/digraph.html)s of commands with dependencies on [aws batch](https://aws.amazon.com/batch/), and a few other compute resources.

```bash
 > workflow help
workflow create \
	pattern=a-bc-d|hourglass|map-reduce,~upload \
	.|<job-name> \
	[--publish_as <public-object-name>]
 . create a <pattern> workflow.
workflow monitor \
	~download,node=<node>,publish_as=<public-object-name>,~upload \
	.|<job-name>
 . monitor workflow.
workflow submit \
	~download,dryrun,to=aws_batch|generic|local,~upload \
	.|<job-name>
 . submit workflow.
```

example use: [literature review using OpenAI API](https://github.com/kamangir/openai-commands/tree/main/openai_commands/literature_review).

|   |   |   |   |
| --- | --- | --- | --- |
| 📜 | [`a-bc-d`](./patterns/a-bc-d.dot) | [`hourglass`](./patterns/hourglass.dot) | [`map-reduce`](./patterns/map-reduce.dot) |
| [aws_batch](./runners/aws_batch.py) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/aws_batch-a-bc-d/workflow.gif?raw=true&random=phGJvrmos0aFCaT2)](https://kamangir-public.s3.ca-central-1.amazonaws.com/aws_batch-a-bc-d/workflow.gif?raw=true&random=phGJvrmos0aFCaT2) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/aws_batch-hourglass/workflow.gif?raw=true&random=HFQ7wxFAvH2x9rCk)](https://kamangir-public.s3.ca-central-1.amazonaws.com/aws_batch-hourglass/workflow.gif?raw=true&random=HFQ7wxFAvH2x9rCk) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/aws_batch-map-reduce/workflow.gif?raw=true&random=b87LtVppmAkzWWm1)](https://kamangir-public.s3.ca-central-1.amazonaws.com/aws_batch-map-reduce/workflow.gif?raw=true&random=b87LtVppmAkzWWm1) |
| [generic](./runners/generic.py) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/generic-a-bc-d/workflow.gif?raw=true&random=zy1Eb8j0yt4cXlqJ)](https://kamangir-public.s3.ca-central-1.amazonaws.com/generic-a-bc-d/workflow.gif?raw=true&random=zy1Eb8j0yt4cXlqJ) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/generic-hourglass/workflow.gif?raw=true&random=aJdChs5XGM83kUEJ)](https://kamangir-public.s3.ca-central-1.amazonaws.com/generic-hourglass/workflow.gif?raw=true&random=aJdChs5XGM83kUEJ) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/generic-map-reduce/workflow.gif?raw=true&random=eEGG6icU3S5MLBjv)](https://kamangir-public.s3.ca-central-1.amazonaws.com/generic-map-reduce/workflow.gif?raw=true&random=eEGG6icU3S5MLBjv) |
| [local](./runners/local.py) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/local-a-bc-d/workflow.gif?raw=true&random=hTQDhqdL8lLXiKAA)](https://kamangir-public.s3.ca-central-1.amazonaws.com/local-a-bc-d/workflow.gif?raw=true&random=hTQDhqdL8lLXiKAA) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/local-hourglass/workflow.gif?raw=true&random=guLpaklz3DehFoID)](https://kamangir-public.s3.ca-central-1.amazonaws.com/local-hourglass/workflow.gif?raw=true&random=guLpaklz3DehFoID) | [![image](https://kamangir-public.s3.ca-central-1.amazonaws.com/local-map-reduce/workflow.gif?raw=true&random=7U16F9PwZVDmBPY4)](https://kamangir-public.s3.ca-central-1.amazonaws.com/local-map-reduce/workflow.gif?raw=true&random=7U16F9PwZVDmBPY4) |

- [dev notes](https://arash-kamangir.medium.com/%EF%B8%8F-openai-experiments-54-e49117dc69ef)

---


[![pylint](https://github.com/kamangir/notebooks-and-scripts/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/notebooks-and-scripts/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/notebooks-and-scripts/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/notebooks-and-scripts/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/notebooks-and-scripts/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/notebooks-and-scripts/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/notebooks-and-scripts.svg)](https://pypi.org/project/notebooks-and-scripts/) [![PyPI - Downloads](https://img.shields.io/pypi/dd/notebooks-and-scripts)](https://pypistats.org/packages/notebooks-and-scripts)

built by 🌀 [`blue_options-4.127.1`](https://github.com/kamangir/awesome-bash-cli), based on [`blueflow-4.770.1`](https://github.com/kamangir/notebooks-and-scripts).
