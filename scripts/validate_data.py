""" Python script to validate data

Run as:

    python3 scripts/validata_data.py data
"""

import os
import sys
import hashlib


def file_hash(filename):
    """ Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.
    """
    with open(filename, 'rb') as fobj:
        file_bytes = fobj.read()
    return hashlib.sha1(file_bytes).hexdigest()


def validate_data(data_directory):
    """ Read ``hash_list.txt`` file in ``data_directory``, check hashes
    
    An example file ``data_hashes.txt`` is found in the baseline version
    of the repository template for your reference.

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``hash_list.txt`` file.

    Returns
    -------
    None

    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``hash_list.txt`` file.
    """
    # Read lines from ``hash_list.txt`` file.
    # Split into SHA1 hash and filename
    # Calculate actual hash for given filename.
    # If hash for filename is not the same as the one in the file, raise
    # ValueError
    hash_file_path = os.path.join(data_directory, "group-00/hash_list.txt")
    with open(hash_file_path) as f:
        lines = f.read().splitlines()
    for line in lines :
        split_line = line.split(" ")
        filename = split_line[1]
        correct_hash = split_line[0]

        file_path = os.path.join(data_directory, filename)
        actual_hash = file_hash(file_path)
        if correct_hash != actual_hash :
            raise ValueError(f"Oh no, seems that {filename} is corrupted")
    
    print('All good! \n')



def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        raise RuntimeError("Please give data directory on "
                           "command line")
    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
