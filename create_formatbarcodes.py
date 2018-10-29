import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os
import logging

LOGFORMAT = '%(asctime)-15s %(levelname)s: %(message)s'
DATEFORMAT = '%m/%d/%Y %H:%M:%S'

def _make_parser():
	parser = argparse.ArgumentParser()
	parser.description = "Create format lifecycle graphs"
	parser.add_argument("-i", "--input",
	help = "path to anonymized collection format profile",
	required = True)
	parser.add_argument("-o", "--output",
	help = "path to directory where to save lifecycle graphs",
	required = True)
	parser.add_argument("--alpha",
	help = "how transparent should bars be, between 0 and 1",
	default = .2)
	return parser


def create_graphs(input_csv, output_dir, alpha = .2):
	df = pd.read_csv(input_csv)
	df.modified = pd.to_datetime(df.modified)
	datemin = df.modified.min()
	datemax = df.modified.max()
	for format_id in df.id.unique():
		ax = sns.scatterplot(x="modified", y="id", data=df[df.id == format_id], alpha = alpha, marker = '|')
		ax.set_xlim(datemin, datemax)
		ax.set_ylim
		try:
			display_id = format_id.replace('/', '_')
		except AttributeError:
			logging.info(
				"%s encountered while parsing CSV, loop will continue without",
				format_id)
			continue
		ax.set(xlabel='Last Modified Date', ylabel='Format ID')
		plt.savefig("{}.png".format(os.path.join(output_dir, display_id)))
		plt.close()


def main():
	logging.basicConfig(format=LOGFORMAT, datefmt=DATEFORMAT, level="INFO")

	parser = _make_parser()
	args = parser.parse_args()

	if os.path.exists(args.output):
		create_graphs(args.input, args.output, args.alpha)
	else:
		raise Exception('Output directory does not exist.')


if __name__ == "__main__":
    main()
