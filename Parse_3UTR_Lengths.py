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


def make_pandas_df(file, sep='\t', header=3):
    with open(file, "r") as file:
        # This is a huge step. Pandas quickly converts the whole text file into a Dataframe
        df = pd.read_csv(file, sep=sep, header=header)
    return df


def mess_w_df(df, columnheaders, max_value):
    # Rename the columns...
    # because I don't know how else to get rid of hash-tag in front of IDs
    df.columns = column_headers

    # Convert sense or antisense to a category -- might make stuff faster?
    df['sense'] = df['sense'].astype('category')

    # Reduce any UTRs longer than 1500nt to 1500 nt
    df.loc[df.UTR_length >= max_value, 'UTR_length'] = max_value

    return df


def head_print_df(df, head=50):
    print(df.head(head))


def info_print_df(df, title: str = ''):
    if title:
        print(f'{title}:\n\tMax Length:{df.UTR_length.max():>6}\n\t'
              f'Min Length:{df.UTR_length.min():>6}\n\t'
              f'\t\tN = {df.size}')
    else:
        print(f'\n\tMax Length:{df.UTR_length.max():>6}\n\t'
              f'Min Length:{df.UTR_length.min():>6}\n\t'
              f'\t\tN = {df.size}')


def filter_sense(df):
    sense = df[df.sense == '+']
    anti_sense = df[df.sense == '-']
    return sense, anti_sense


def quick_plot_histo(variable: iter, number_of_bins: int = 5000, maximum: int = None):
    fig, ax = plt.subplots(tight_layout=True)
    # We can set the number of bins with the `bins` kwarg
    ax.hist(variable, bins=number_of_bins)
    if maximum:
        ax.set_xlabel(f'UTR Length,\nin {number_of_bins} bins, with cut-off at {maximum}nt')
    else:
        ax.set_xlabel(f'UTR Length,\nin {number_of_bins} bins')
    ax.set_ylabel('Number of Reads')
    ax.set_title("3' UTR reads from C.H. Jan et al. 2010")
    plt.show()


if __name__ == '__main__':
    # Open file and store into Pandas data-frame
    df = make_pandas_df("NIHMS249209-supplement-5.txt")

    # Print basics
    info_print_df(df, title="All UTRs")

    # Fix headers, try to simplify data-types, pool anything above max to max
    df = mess_w_df(df, column_headers, max_value=1500)

    # Print basics post max cut off
    info_print_df(df, title="Max Cut UTRs")

    # Plot histogram
    quick_plot_histo([df['UTR_length']], number_of_bins=500, maximum=1500)
