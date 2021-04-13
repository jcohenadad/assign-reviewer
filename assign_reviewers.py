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
import pkg_resources
import sys

logger = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser(
        prog='assign-reviewers',
        description="Assign reviewers and create scoring excel sheets. The input is a CSV file formatted"
                    " as in testing/form.csv. This CSV can be exported from Google form.",
        add_help=False)
    parser.add_argument('-h', '--help', action="help", help="Show this help message and exit")
    parser.add_argument('-c', '--csv',
                        help="CSV file following the format found in testing/form.csv")
    parser.add_argument('-r', '--reviewer', nargs='?', action='append',
                        help='Name of a reviewer. No space allowed.')
    parser.add_argument('-n', '--number-reviewers', type=int, default=2,
                        help='Number of reviewers per entry to assign.')
    parser.add_argument('-v', '--version', action='version',
                        version=pkg_resources.require('assign-reviewers')[0].version)
    parser.add_argument('-l', '--log-level',
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
    n_entries = df.shape[0]
    list_reviewers = [[]] * n_entries

    # TODO: make it input args
    reviewers = args.reviewer
    n_reviewers = len(reviewers)
    reviewers_per_entry = args.number_reviewers

    for i_entry in range(n_entries):
        list_reviewers[i_entry] = select_from_pool(list_reviewers,
                                                   n_rev_total=n_reviewers,
                                                   n_rev_to_assign=reviewers_per_entry)

    for i_reviewer in range(n_reviewers):
        ind_rev = [i for i in range(n_entries) if i_reviewer in list_reviewers[i]]
        df_tmp = df.copy()
        df_tmp.loc[~df_tmp.index.isin(ind_rev)] = ''
        df_tmp['Rank'] = ''
        df_tmp.to_csv(f'grading_form_{reviewers[i_reviewer]}.csv')

    df['Reviewers'] = list_reviewers
    df.to_csv(f'grading_form.csv')


if __name__ == '__main__':
    main()
