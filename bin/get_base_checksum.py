#!/usr/bin/env python3
from argparse import ArgumentParser
from docker_utils import get_labels

parser = ArgumentParser()
parser.add_argument(
    "-n", "--name", dest="name", help="Docker image name e.g cmssw/el8:aarch64-runtime", type=str
)
args = parser.parse_args()

labels = get_labels(args.name)
print(labels['build-checksum'])
