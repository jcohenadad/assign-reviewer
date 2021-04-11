#!/usr/bin/env python3
#
# Very simple script that randomly assign reviewers and create scoring excel sheets.
#
# Author: Julien Cohen-Adad

import argparse
import logging
import logging.handlers
import pandas as pd
import sys

logger = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Assign reviewers and create scoring excel sheets. The input is a CSV file formatted"
                    " as in testing/form.csv. This CSV can be exported from Google form.",
        add_help=False)
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    optional.add_argument("-c", "--csv",
                          help="CSV file following the format found in testing/form.csv")
    optional.add_argument("-l", "--log-level",
                          default="INFO",
                          help="Logging level (eg. INFO, see Python logging docs)")
    return parser


def main():
    # Get input params
    parser = get_parser()
    args = parser.parse_args()

    # Set logging
    logging.basicConfig(stream=sys.stdout, level=args.log_level, format="%(levelname)s %(message)s")

    # put CSV into Panda dataframe
    df = pd.read_csv(args.csv)

    # Generate a Panda DF per reviewer
    raise NotImplementedError


if __name__ == '__main__':
    main()
