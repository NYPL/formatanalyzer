#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""create_formatbarcodes.py

Generate data-based distribution (barcode) charts for a given dataset. The
identifier value sits on the y-axis and last-modified date on the x-axis.
"""
import argparse
import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

LOGFORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
DATEFORMAT = '%m/%d/%Y %H:%M:%S'


def _make_parser():
    """Create a parse for our command line arguments."""
    parser = argparse.ArgumentParser()
    parser.description = "Create format lifecycle graphs"
    parser.add_argument(
        "-i", "--input",
        help="path to anonymized collection format profile",
        required=True)
    parser.add_argument(
        "-o", "--output",
        help="path to directory where to save lifecycle graphs",
        required=True)
    parser.add_argument(
        "--alpha",
        help="how transparent should bars be, between 0 and 1",
        default=.2)
    return parser


def create_graphs(input_csv, output_dir, alpha=.2):
    """Generate graph output from the input data."""
    data_frame = pd.read_csv(input_csv)
    data_frame.modified = pd.to_datetime(data_frame.modified)
    datemin = data_frame.modified.min()
    datemax = data_frame.modified.max()
    for format_id in data_frame.id.unique():
        axis_ = sns.scatterplot(
            x="modified", y="id", data=data_frame[data_frame.id == format_id],
            alpha=alpha, marker='|')
        axis_.set_xlim(datemin, datemax)
        axis_.set_ylim()
        try:
            display_id = format_id.replace('/', '_')
        except AttributeError:
            logging.info(
                "%s encountered while parsing CSV, loop will continue without",
                format_id)
            continue
        axis_.set(xlabel='Last Modified Date', ylabel='Format ID')
        plt.savefig("{}.png".format(os.path.join(output_dir, display_id)))
        plt.close()


def main():
    """Primary entry point for the script."""
    logging.basicConfig(format=LOGFORMAT, datefmt=DATEFORMAT, level="INFO")

    parser = _make_parser()
    args = parser.parse_args()

    if os.path.exists(args.output):
        create_graphs(args.input, args.output, args.alpha)
    else:
        raise Exception('Output directory does not exist.')


if __name__ == "__main__":
    main()
