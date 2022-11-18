#!/usr/bin/env python3

import click
from loguru import logger
from .utils import read_config


@click.group()
def cli():
    pass


@cli.command()
@click.option("--experiment", required=False, type=click.STRING)
@click.option(
    "--checkpoint-uri",
    default=None,
    type=click.STRING,
    required=False,
    help="preload checkpoint from this uri (to continue training)",
)
def train(experiment, checkpoint_uri):
    from .trainer import trainer
    import mlflow

    cfg = read_config()
    mlflow.set_experiment(experiment)
    if checkpoint_uri:
        mlflow.artifacts.download_artifacts(
            artifact_uri=checkpoint_uri,
            dst_path=cfg["DIR"]["LOG_ROOT_DIR"] + "checkpoint/",
        )

    trainer(cfg, "checkpoint")


""" Generate fingerprint (after training) """


@cli.command()
@click.option(
    "--source",
    "-s",
    default=None,
    type=click.STRING,
    required=True,
    help=(
        "Custom source root directory. The source must be 16-bit "
        "8 Khz mono WAV. This is only useful when constructing a database"
        " without synthesizing queries."
    ),
)
@click.option(
    "--output",
    "-o",
    default=None,
    type=click.STRING,
    required=True,
    help="Root directory where the generated embeddings (uncompressed)"
    + " will be stored",
)
@click.option(
    "--checkpoint-uri",
    default=None,
    type=click.STRING,
    required=False,
    help="preload checkpoint from this uri (to generate embeddings)",
)
def generate(source, output, checkpoint_uri):
    from .generator.generate import generate_fingerprint

    cfg = read_config()
    generate_fingerprint(cfg, source, output, checkpoint_uri)


if __name__ == "__main__":
    cli()
