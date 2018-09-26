import pandas as pd
import os
import argparse


def _make_parser():
  parser = argparse.ArgumentParser()
  parser.description = "anonymize Droid csv output"
  parser.add_argument("-i", "--input",
    help = "path to Droid output csv")
  parser.add_argument("-o", "--output",
    help = "path to anonymized output, default is input_cleaned.csv")
  return parser


def clean_siegfried(input_csv, output_csv):
	df = df[df.TYPE == 'File']
  df['warning'] = df['EXTENSION_MISMATCH'].map({True: 'extension mismatch'})
  df.drop(['ID', 'PARENT_ID', 'URI', 'FILE_PATH', 'NAME', 'METHOD', 
    'STATUS', 'TYPE', 'HASH', 'FORMAT_COUNT', 'MIME_TYPE', 'FORMAT_NAME', 
    'FORMAT_VERSION', 'EXTENSION_MISMATCH'], axis = 1, inplace = True)
  df = df.sample(frac=1).reset_index(drop=True)
  df.to_csv(output_csv)

def main():
    parser = _make_parser()
    args = parser.parse_args()

    if args.output:
    	output_csv = args.output
    else:
    	output_csv = args.input.replace('.', '_cleaned.')

    clean_siegfried(args.input, output_csv)
    print('CSV cleaned and stored at {}'.format(output_csv))


if __name__ == "__main__":
    main()