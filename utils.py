"""
Utility functions.

Created by: Jani Bizjak
Created at: 05.04.2020
"""


def combine_batch_pair(summary_a, summary_b):
    """Combines two batches into one.

    :param summary_a: list, of first batch
    :param summary_b: list, of second batch
    :return: list: PartialSummary, combined data of first and second batch in single list
    """

    summary = summary_a  # Set first list as base
    for friend in summary_b:
        if friend not in summary:  # If person is not in the base, add it to the base
            summary[friend] = summary_b[friend]
        else:
            summary[friend].add_new_data(
                summary_b[friend].speed,
                summary_b[friend].distance,
                summary_b[friend].transport
            )

    return summary


def round_progress(x, base=5):
    """Rounds the number to closes multiple of base.

    :param x: float
    :param base: int, to which multiple the method rounds the number
    :return: int, rounded number
    """

    return base * round(x / base)

