# For fq we cannot quite use the out of the box CSV reader because fq
# files have a multiline header
import pandas
from tiled.adapters.dataframe import DataFrameAdapter


def read_fq(filepath):
    # Extract column headers.
    with open(filepath) as file:
        for line in file:
            if line.startswith("# #L"):
                # This line declares the column names.
                names = line[4:].split()  # "# #L a b" -> ["a", "b"]
                break
        else:
            # Reached end of file, never found column names
            raise ValueError("The fq file at {filepath} had not column name delcaration # #L ...")
    # Read file into CSV, ignoring all lines that begin with #,
    # and manually setting the column names found above.
    df = pandas.read_csv(filepath, comment="#", names=names)
    return DataFrameAdapter.from_pandas(df, npartitions=1)
