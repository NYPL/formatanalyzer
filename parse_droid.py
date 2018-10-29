#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""parse_droid.py

Anonymize and convert DROID csv to be compatible with
create_formatbarcodes.py.
"""
import argparse

import pandas as pd


def _make_parser():
    """Create a parse for our command line arguments."""
    parser = argparse.ArgumentParser()
    parser.description = "anonymize Droid csv output"
    parser.add_argument(
        "-i", "--input",
        help="path to Droid output csv",
        required=True)
    parser.add_argument(
        "-o", "--output",
        help="path to anonymized output, default is input_cleaned.csv")
    return parser


def clean_droid(input_csv, output_csv):
    """Anonymize and format the input provided."""
    data_field = pd.read_csv(input_csv)
    data_field = data_field[data_field.TYPE == 'File']
    data_field['warning'] = data_field['EXTENSION_MISMATCH']\
        .map({True: 'extension mismatch'})
    data_field.drop(['ID', 'PARENT_ID', 'URI', 'FILE_PATH', 'NAME', 'METHOD',
                     'STATUS', 'TYPE', 'HASH', 'FORMAT_COUNT', 'MIME_TYPE',
                     'FORMAT_NAME', 'FORMAT_VERSION', 'EXTENSION_MISMATCH'],
                    axis=1, inplace=True)
    # Rename fields to be consistent with the Siegfried Format
    data_field = data_field.rename(columns={
        'SIZE': 'filesize', 'PUID': 'id', 'LAST_MODIFIED': 'modified',
        'EXT': 'ext'})
    data_field = data_field.sample(frac=1).reset_index(drop=True)
    data_field.to_csv(output_csv, index=False)


def main():
    """Generate graph output from the input data."""
    parser = _make_parser()
    args = parser.parse_args()

    if args.output:
        output_csv = args.output
    else:
        output_csv = args.input.replace('.', '_cleaned.')

    clean_droid(args.input, output_csv)
    print('CSV cleaned and stored at {}'.format(output_csv))


if __name__ == "__main__":
    main()
