#!/usr/bin/env python3
#
# Very simple script that randomly assign reviewers and create scoring excel sheets.
#
# Author: Julien Cohen-Adad

import argparse
import logging
import logging.handlers
import numpy as np
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


def select_from_pool(list_reviewers, n_rev_total, n_rev_to_assign):
    """Find reviewers who are least assigned"""
    # TODO: add constraints based on affiliation
    df_reviewers_flat = [item for sublist in list_reviewers for item in sublist]
    # Get indices corresponding to reviewers who are least assigned
    ind_rev = np.argsort(np.array([df_reviewers_flat.count(i) for i in range(n_rev_total)]))
    return ind_rev.tolist()[:n_rev_to_assign]


def main():
    # Get input params
    parser = get_parser()
    args = parser.parse_args()

    # Set logging
    logging.basicConfig(stream=sys.stdout, level=args.log_level, format="%(levelname)s %(message)s")

    # put CSV into Panda dataframe
    df = pd.read_csv(args.csv)

    # Generate a Panda DF per reviewer
    list_reviewers = [[]] * 7
    n_entries = df.shape[0]

    # TODO: make it input args
    n_reviewers = 5
    reviewers_per_entry = 2

    for i_entry in range(n_entries):
        list_reviewers[i_entry] = select_from_pool(list_reviewers,
                                                   n_rev_total=n_reviewers,
                                                   n_rev_to_assign=reviewers_per_entry)

    df['Reviewers'] = list_reviewers


if __name__ == '__main__':
    main()
