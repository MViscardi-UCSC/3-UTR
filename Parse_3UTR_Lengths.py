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
    store them within a numpy array, and try to plot them in some distinguishable way
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


def quick_plot_histo(variable: iter, number_of_bins: int = 5000):
    fig, ax = plt.subplots(tight_layout=True)
    # We can set the number of bins with the `bins` kwarg
    ax.hist(variable, bins=number_of_bins)
    plt.show()


if __name__ == '__main__':
    # Open file and store into Pandas dataframe
    with open("NIHMS249209-supplement-5.txt", "r") as file:
        # This is a huge step. Pandas quickly converts the whole text file into a Dataframe
        df = pd.read_csv(file, sep='\t', header=3)

    # Rename the columns...
    # because I don't know how else to get rid of hash-tag in front of IDs
    df.columns = column_headers

    # Print first 25 rows
    # print(df.head(25))

    # Print average UTR length
    print(f'UTR Length Average: {df["UTR_length"].mean():.2f}')

    quick_plot_histo(df['UTR_length'])
