#! /usr/bin/env python3
"""
Parse_3UTR_Lengths.py
By Marcus Viscardi
Updated: 03-22-2020

Goal of this script is to parse the identified 3' UTR reads that came out of the CH Jan et al.
    2010 Nature paper: Formation, Regulation and Evolution of Caenorhabditis elegans 3'UTRs
The data is stored as a .txt file with tab separated values corresponding to:
    Entrez_ID	UTR_type	chromosome	sense	UTR_start	cleavage_site	UTR_length
    	intron_starts(comma_separted)	intron_ends(comma_separted)	UTR_sequence
For the initial parsing (with this script), lets just try to iterate through the first thousand or so data points,
    store them within a pandas array, and try to plot them in some distinguishable way
All that is really needed for this initial run through is the EntrezID and the UTR_length
"""
import matplotlib.pyplot as plt
import pandas as pd
# Pandas default would cut off basically all the columns so:
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)

# Hard coded column headers make tracking a little easier
column_headers = ['entrez_ID',
                  'UTR_type',
                  'chromosome',
                  'sense',
                  'UTR_start',
                  'cleavage_site',
                  'UTR_length',
                  'intron_starts',
                  'intron_ends',
                  'UTR_sequence',
                  ]


# The following functions just help legibility for main()
# Parse the sup data file
def make_pandas_df(file, sep='\t', header=3):
    with open(file, "r") as file:
        # This is a huge step. Pandas quickly converts the whole text file into a Dataframe
        df = pd.read_csv(file, sep=sep, header=header)
    return df


# for use with timeit
def hardcode_make_df():
    """This is only for the use with timeit"""
    return make_pandas_df("NIHMS249209-supplement-5.txt")


# rename columns and cut off anything larger than max_value
def mess_w_df(df, column_headers, max_value):
    # Rename the columns...
    # because I don't know how else to get rid of hash-tag in front of IDs
    df.columns = column_headers

    # Convert sense or antisense to a category -- might make stuff faster?
    df['sense'] = df['sense'].astype('category')

    # Reduce any UTRs longer than 1500nt to 1500 nt
    df.loc[df.UTR_length >= max_value, 'UTR_length'] = max_value

    return df


# used as needed to print df info
def info_print_df(df, title: str = ''):
    if title:
        print(f'{title}:\n\tMax Length:{df.UTR_length.max():>6}\n\t'
              f'Min Length:{df.UTR_length.min():>6}\n\t'
              f'\t\tN = {df.size}')
    else:
        print(f'\n\tMax Length:{df.UTR_length.max():>6}\n\t'
              f'Min Length:{df.UTR_length.min():>6}\n\t'
              f'\t\tN = {df.size}')


# used as needed to return two separate dataframes of sense and antisense
def filter_sense(df):
    sense = df[df.sense == '+']
    anti_sense = df[df.sense == '-']
    return sense, anti_sense


# no longer used - would bin and plot data using matplotlib
def quick_plot_histo(variable: iter,
                     number_of_bins: int = 5000,
                     maximum: int = None):
    fig, ax = plt.subplots(tight_layout=True)
    # We can set the number of bins with the `bins` kwarg
    ax.hist(variable, bins=number_of_bins)
    if maximum:
        ax.set_xlabel(f'UTR Length,\nin {number_of_bins} bins,'
                      f'with cut-off at {maximum}nt')
    else:
        ax.set_xlabel(f'UTR Length,\nin {number_of_bins} bins')
    ax.set_ylabel('Number of Reads')
    ax.set_title("3' UTR reads from C.H. Jan et al. 2010")
    plt.show()


# bin data and calculate moving average with pandas, plot against histo with matplotlib
def bin_and_plot_df(df, num_bins, rolling_window_size):
    """"""
    # Tuple with the range of numbers that are basically the indexes of our bins (+1)
    index_list = range(1, num_bins+1)
    # bin our values into num_bins bins
    binned_series = pd.cut(df.UTR_length, bins=num_bins, labels=index_list).value_counts()
    # reorder binned series based on indexes (which correspond to UTR length here)
    binned_ordered_series = binned_series.sort_index()
    # find moving average for each bin
    rolling_average = binned_ordered_series.rolling(rolling_window_size,
                                                    center=True,
                                                    min_periods=int(rolling_window_size/2)
                                                    ).mean()
    # # Converting to a list makes it easier to pass into MatPlotLib
    # binned_ordered_list = binned_ordered_series.values
    # bin_factor allows us to translate the bin indexes back to the UTR_length values
    bin_factor = int(df.UTR_length.max() / num_bins)

    fig, axs = plt.subplots()
    # # plot binned data
    # axs.plot([x * bin_factor for x in index_list], binned_ordered_list)

    # plot moving average
    axs.plot([x * bin_factor for x in index_list],
             rolling_average,
             label=f"Simple Moving Average, window={rolling_window_size}",
             linewidth=2.3, color=(0/255, 114/255, 178/255, 255/255))

    # plot histogram with data binned independently by matplotlib (slow)
    axs.hist(df.UTR_length.values,
             bins=num_bins,
             label=f"Binned Histogram, bins={num_bins}",
             color=(213/255, 94/255, 0/255, 255/255))

    axs.legend()
    axs.set_title("3' UTR reads from C.H. Jan et al. 2010")
    plt.xlabel(f"3' UTR Lengths (nt)")  # TODO: Change this to 'fraction of reads'
    plt.ylabel(f"Number of UTRs Counted,\nn={df.shape[0]}")
    plt.show()


if __name__ == '__main__':
    # Open file and store into Pandas data-frame
    df = make_pandas_df("NIHMS249209-supplement-5.txt")

    # Print basics
    # info_print_df(df, title="All UTRs")

    # Print zero length UTRs
    # print(df[df.UTR_length == 0].sort_values("chromosome"))
    # print(df.sort_values(["chromosome", "UTR_start"]))
    print(df.info())

    # Fix headers, try to simplify data-types, pool anything above max_value to max_value
    df = mess_w_df(df, column_headers, max_value=1500)

    # Bin data with pandas.cut, make a simple moving average of binned data,
    # and blot against data binned by matplotlib
    bin_and_plot_df(df, 500, 5)
