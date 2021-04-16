#!/usr/bin/env python3
#
# Very simple script that randomly assigns reviewers and creates scoring excel sheets.
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
    example_text = '''examples:

  assign-reviewers -c testing/form.csv -r Anna -r Elsa -r Christophe -r Sven -n 3
  assign-reviewers -c form.csv -r Anna -a "Chiang Mai" -r Elsa -a UBC "British Columbia"
    '''

    parser = argparse.ArgumentParser(
        prog='assign-reviewers',
        description="Assign reviewers and create scoring excel sheets. The input is a CSV file formatted"
                    " as in testing/form.csv. This CSV can be exported from Google form.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False)
    parser.add_argument('-h', '--help', action="help", help="Show this help message and exit")
    parser.add_argument('-c', '--csv',
                        help="CSV file following the format found in testing/form.csv")
    parser.add_argument('-r', '--reviewer', nargs='?', action='append',
                        help='Name of a reviewer. No space allowed.')
    parser.add_argument('-a', '--affiliation', nargs='+', action='append',
                        help='Affiliation(s) of the previously-listed reviewer. If you decide to '
                             'add affiliations, you need to add them for ALL reviewers. One reviewer can have multiple'
                             'affiliations; if this is the case, separate them with space. If an affiliation has '
                             'spaces in it, add double-quotes. Example: "University of Toronto"')
    parser.add_argument('-n', '--number-reviewers', type=int, default=2,
                        help='Number of reviewers per entry to assign.')
    parser.add_argument('-v', '--version', action='version',
                        version=pkg_resources.require('assign-reviewers')[0].version)
    parser.add_argument('-l', '--log-level',
                        default="INFO",
                        help="Logging level (eg. INFO, see Python logging docs)")
 
    return parser


def remove_same_affiliation(aff_entry, aff_reviewers):
    """
    Find reviewers which affiliations match that of the entry and return a list of eligible reviewers.
    :param aff_entry:
    :param aff_reviewers:
    :return: list of int
    """
    eligible_reviewer = []
    for i_rev in range(len(aff_reviewers)):
        if not any(aff_rev in aff_entry for aff_rev in aff_reviewers[i_rev]):
            eligible_reviewer.append(i_rev)
    return eligible_reviewer


def select_from_pool(list_reviewers, eligible_reviewers, n_rev_to_assign):
    """
    Find reviewers who are least assigned
    :param list_reviewers: list of string:
    :param eligible_reviewers: list of int:
    :param n_rev_to_assign: int:
    :return:
    """
    df_reviewers_flat = [item for sublist in list_reviewers for item in sublist]
    # Get indices corresponding to reviewers who are least assigned
    ind_rev = np.argsort(np.array([df_reviewers_flat.count(i) for i in eligible_reviewers]))
    return [eligible_reviewers[i] for i in ind_rev.tolist()][:n_rev_to_assign]


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

    reviewers = args.reviewer
    n_reviewers = len(reviewers)
    reviewers_per_entry = args.number_reviewers

    # Make sure number of affiliations match number of reviewers
    if args.affiliation is None:
        # If no affiliation given, use all reviewers.
        eligible_reviewers = list(range(n_reviewers))
    elif not len(args.affiliation) == n_reviewers:
        raise RuntimeError("The number of affiliations should match the number of reviewers. Exit.")

    for i_entry in range(n_entries):
        if args.affiliation is not None:
            eligible_reviewers = remove_same_affiliation(df.loc[i_entry]['Affiliation'], args.affiliation)
        list_reviewers[i_entry] = select_from_pool(list_reviewers,
                                                   eligible_reviewers=eligible_reviewers,
                                                   n_rev_to_assign=reviewers_per_entry)

    for i_reviewer in range(n_reviewers):
        ind_rev = [i for i in range(n_entries) if i_reviewer in list_reviewers[i]]
        df_tmp = df.copy()
        df_tmp.loc[~df_tmp.index.isin(ind_rev)] = ''
        df_tmp[reviewers[i_reviewer]] = ''
        df_tmp.to_csv(f'grading_form_{reviewers[i_reviewer]}.csv')


if __name__ == '__main__':
    main()
