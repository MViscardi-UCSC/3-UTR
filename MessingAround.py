"""
MessingAround.py
By Marcus Viscardi, March 29 2020
"""

import pandas as pd
import numpy as np


# Taken from my method in lab-scripts
def pandas_df_method(chrs, chrSize, N):
    """This is really just generating the data, in an effort to look at the 'weight' of the final df"""
    # Empty dataframe makes the if statements below a little easier
    df = pd.DataFrame()
    for ii in range(chrs):
        if not df.empty:
            # hold onto previous chromosomes, to be added together later
            old_df = df
            # pandas was freaking about about using .insert with non-empty dataframe
            df = pd.DataFrame()
        # below three calls generate and add columns
        df.insert(0, 'loc',
                  [x[0] for x in np.random.randint(0, chrSize, size=(N, 1))])
        df.insert(1, 'trans',
                  [f'somestring:{x[0]}:s' for x in np.random.randint(0, 10**5, size=(N, 1))])
        df.insert(0, 'chr', f"chr{ii}")
        if ii > 0:
            # if we are working with more than one chromosomes, reconnect the generated chr to old chrs
            df = old_df.append(df, ignore_index=True)
        # F-STRINGS!!
        print(f'Dataframe size (cells): {df.size}, after {ii+1} chromosome(s)')
        first_index = 0 + (ii * N)
        print(f"\tFirst index of chr{ii}({first_index}):\n\t{df.values[first_index]}\n\n")
    # Unsure if this is necessary, but could be a way to lighten the dataframe later on
    df.astype({'chr': 'category', 'loc': 'Int32', 'trans': 'object'}).dtypes
    print(df.size, '\n\n')
    #print(df)
    return df


if __name__ == '__main__':
    dataframe = pandas_df_method(5, 10**9, 10**5)
    print(f'Memory Usage:\n{dataframe.memory_usage(deep=True)}')
    print(dataframe.head())
    pd.MultiIndex.from_frame(dataframe)
    #print(f'Memory Usage:\n{dataframe.memory_usage(deep=True)}')
