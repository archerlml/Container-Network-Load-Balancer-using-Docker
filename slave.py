"""
slave.py

Train a machine learning model using the given model, parameter and dataset.

Usage:
    python3 slave.py model_name parameter_file dataset_file
"""

import sys, time

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit()
    # This part is left for furture work. 
    # We can write our own machine learning training program here.
    time.sleep(2)
    print("Training finished!!")