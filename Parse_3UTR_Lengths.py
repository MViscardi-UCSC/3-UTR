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


def quick_plot_histo(variable: iter, number_of_bins: int = 5000):
    fig, ax = plt.subplots(tight_layout=True)
    # We can set the number of bins with the `bins` kwarg
    ax.hist(variable, bins=number_of_bins)
    ax.set_xlabel('UTR Length')
    ax.set_ylabel('Number of Reads')
    ax.set_title('')
    plt.show()


if __name__ == '__main__':
    # Open file and store into Pandas dataframe
    with open("NIHMS249209-supplement-5.txt", "r") as file:
        # This is a huge step. Pandas quickly converts the whole text file into a Dataframe
        df = pd.read_csv(file, sep='\t', header=3)

    # Rename the columns...
    # because I don't know how else to get rid of hash-tag in front of IDs
    df.columns = column_headers

    # Convert sense or antisense to a category -- might make stuff faster?
    df['sense'] = df['sense'].astype('category')

    # Reduce any UTRs longer than 1500nt to 1500 nt
    df.loc[df.UTR_length >= 1500, 'UTR_length'] = 1500

    # Quick Filter!
    df_plus = df[df.sense == '+']
    df_minus = df[df.sense == '-']

    # # Print first 50 rows
    # print(df_plus.head(50))
    # print(df_minus.head(50))

    # # Print average, max & min UTR length
    # print(f'UTR Length Max: {df.UTR_length.max():}')
    # print(f'UTR Length Average: {df.UTR_length.mean():.2f}')
    # print(f'UTR Length Min: {df.UTR_length.min():}')

    # Print basics for each plus and minus
    print(f'All UTRs:\n\tMax Length:{df.UTR_length.max():>6}\n\t'
          f'Min Length:{df.UTR_length.min():>6}\n\t'
          f'\t\tN = {df.size}')
    print(f'Antisense UTRs:\n\tMax Length:{df_minus.UTR_length.max():>6}\n\t'
          f'Min Length:{df_minus.UTR_length.min():>6}\n\t'
          f'\t\tN= {df_minus.size}')
    print(f'Sense UTRs:\n\tMax Length:{df_plus.UTR_length.max():>6}\n\t'
          f'Min Length:{df_plus.UTR_length.min():>6}\n\t'
          f'\t\tN= {df_plus.size}')

    # # Look at ends of UTRs
    # for UTR in df_plus['UTR_sequence'].head(50).values:
    #     print(f'{UTR[-50:]:.>50}')
    # print('*' * 50)
    # for UTR in df_minus['UTR_sequence'].head(50).values:
    #     print(f'{UTR[:50]:.<50}')

    quick_plot_histo([df['UTR_length']], number_of_bins=100)
