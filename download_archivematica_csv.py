#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""download_archivematica_csv.py

Download compatible data from an Archivematica Dashboard instance.
"""
import argparse
import getpass

import MySQLdb
import pandas as pd

ALL_FILES_QUERY = (
    """
    select FilesIDs.formatRegistryKey as "id",
           FilesIDs.formatName as "formatname",
           FilesIDs.formatVersion as "formatversion",
           Files.modificationTime as "modified",
           Files.fileSize as "size" from Files
    inner join FilesIDs
    where fileGrpUse = 'original'
    and Files.fileUUID = FilesIDs.fileUUID
    """
)


def _make_parser():
    """Create a parse for our command line arguments."""
    parser = argparse.ArgumentParser()
    parser.description = "download Archivematica data"
    parser.add_argument(
        "--url", "--host",
        help="url to connect to the database on",
        required=True)
    parser.add_argument(
        "-p", "--port",
        help="port to connect to the database on",
        required=True)
    parser.add_argument(
        "--user",
        help="user to connect with (default: root)",
        default="root",
        required=False)
    parser.add_argument(
        "--pwd", "--pass",
        help="password to connect with (default: 12345) "
             "WARNING: you will be prompted with a masked field so please "
             "don't pass your credentials with this flag",
        default=False,
        action="store_true",
        required=False)
    parser.add_argument(
        "-o", "--output",
        default="archivematica_data.csv",
        help="path to anonymized output, default is archivematica_data.csv")
    return parser


def download_am(host, port, user, pass_, output_csv):
    """Download file format identification data from Archivematica."""

    # Connect to the database and then run our query.
    conn = MySQLdb.connect(
        host=host, port=port, user=user, passwd=pass_, db="MCP")
    cursor = conn.cursor()
    cursor.execute(ALL_FILES_QUERY)
    result = cursor.fetchall()
    conn.close()
    # Construct our csv to then save it.
    data_field = pd.DataFrame.from_records(list(result))
    data_field.columns = [col[0] for col in cursor.description]
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

    pass_ = "12345"
    if args.pwd:
        pass_ = getpass.getpass("Password: ")

    download_am(args.url, int(args.port), args.user, pass_, output_csv)
    print('CSV stored at {}'.format(output_csv))


if __name__ == "__main__":
    main()
