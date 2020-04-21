"""Amazing race script info.

The script reads the data provided in two types of files: a index.json, where info about the participants, days,
distances and stages (race legs) is found and day_xxxx.json, where data about each day is stored. The script runs in
parallel reading each day's worth of data, combining information and calculating total distance, average speed and
transport type used by each participant.

To use the script call method  summarize_amazing_race(:path_to_data, :num_processes) with arguments path to the folder
containing json files and number of processes that the programm should use.

The script contains following methods:
 * summarize_amazing_race - main method that analyzes the race
 * combine_data - combines data from multiple processes
 * summarize_data_for_batch - combines data from different legs and days on a single process
 * __main__ - example on how to run the script

Created by: Jani Bizjak
Created at: 05.04.2020
"""

import json
import pathlib
import multiprocessing as mp
import math

from partial_summary import PartialSummary
from progress_monitor import ProgressMonitor
from utils import combine_batch_pair


def summarize_amazing_race(path_to_data='sample_data/test1/', num_processes=4):
    """Calculates the amazing race statistics and prints them out for each person in the race.

    Goes through all the days annotated in index.json file. From each day it gatheres data for each participant and then
    combines data for whole race. The method can run in parallel, recommended number of processes is
    < number_cpu_cores * 2. While the data is being processed the progress is written to std in 5% increments by number
    of legs. At the end the data for each participant is printed to stdout.

    :param path_to_data: string, path to the folder containing data_xxx.json and index.json
    :param num_processes: int, number of processes to run in parallel
    """

    path = pathlib.Path(path_to_data)
    with open(path / "index.json", "r") as f:  # Because you use with, indent everything below to the same level
        index_jsonable = json.load(f)

        #  Read data from index.json file and stores it for later use.
        friend_list = index_jsonable['friends']
        total_distance = sum(dist for _, dist, _ in index_jsonable['files'])
        total_legs = sum(num_legs for *_, num_legs in index_jsonable['files'])
        file_names = [fn for fn, *_ in index_jsonable['files']]
        total_files = len(file_names)

        queue = mp.Queue()  # Create shared queue in order to bring back results after they have been processed.
        progress_monitor = ProgressMonitor(total_legs, total_distance)  # Create shared ProgressMonitor

        processes = []
        step_size = math.ceil(total_files / num_processes)  # How many files per process

        for i in range(0, len(file_names), step_size):
            #  Write all filename that are to be processed in this batch (by a single process)
            batch = [path / file_names[j] for j in range(i, min(i + step_size, total_files))]
            processes.append(mp.Process(
                target=summarize_data_for_batch,
                args=(batch, i // step_size, queue, progress_monitor))
            )

        for t in processes:
            t.start()
        for t in processes:
            t.join()

        #  Print final progress, it should be at 100%.
        progress_monitor.print_progress(True)

        #  Gather shared data from the queue.
        all_data = [None] * queue.qsize()
        while not queue.empty():
            processed_day = queue.get()
            all_data[processed_day[0]] = processed_day[1]

        friend_summaries = combine_data(all_data)  # Combine data from different batches into one.

        print("\n\n++++++++++++")
        print("In total %i friends participated in this race: " % (len(friend_list)) + ", ".join(friend_list))
        print("Together they traveled for total distance of %0.1f km\n" % total_distance)
        for friend in friend_summaries.keys():
            friend_summary = friend_summaries[friend]
            print("%s\n--------" % (friend,))
            friend_summary.print()
            print("")


def combine_data(list_of_summaries):
    """Combines data from each batch.

    :param list_of_summaries: list[list], of PartialSummary(s)
    :return: list, of PartialSummary(s)
    """

    combined = list_of_summaries[0]  # Take first list in list as base
    for i in range(1, len(list_of_summaries)):  # Add combine following lists to base
        combined = combine_batch_pair(combined, list_of_summaries[i])

    return combined


def summarize_data_for_batch(files_in_batch, data_idx, queue, progress_monitor):
    """Summarizes the data for days in the batch, each batch should be processed on separate process.

    :param files_in_batch: list of paths, paths to all the files that should be processed
    :param data_idx: int, index of the batch
    :param queue: Queue, processed data is stored in queue (shared memory)
    :param progress_monitor: ProgressMonitor
    :return:
    """

    summary = {}
    for file_for_day in files_in_batch:
        with open(file_for_day, "r") as f:
            data = json.load(f)

            for leg in data:
                friend = leg['participant']

                # If person hasn't been seen yet, create new PartialSummary of person's trip.
                if friend not in summary:
                    summary[friend] = PartialSummary()

                summary[friend].add_new_leg(leg)  # Update values of this leg
                progress_monitor.increment_legs_and_distance(1, float(leg['distance']))  # Update total progress

    queue.put((data_idx, summary))


if __name__ == '__main__':
    # It's better to use spawn as it works both on Linux, Windows and Mac.
    mp.set_start_method('spawn')

    summarize_amazing_race('sample_data/test1/', num_processes=1)
    summarize_amazing_race('sample_data/test2/', num_processes=2)
    summarize_amazing_race('sample_data/test3/', num_processes=4)
    summarize_amazing_race('sample_data/test4/', num_processes=16)



