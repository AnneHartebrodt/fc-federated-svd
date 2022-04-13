import os
import gzip
import numpy as np
import pandas as pd
import os.path as op
import argparse as ap
# Copied from fashion mnist

def load_mnist(path, kind='train'):


    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,
                               '%s-labels-idx1-ubyte.gz'
                               % kind)
    images_path = os.path.join(path,
                               '%s-images-idx3-ubyte.gz'
                               % kind)

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                               offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 784)

    return images, labels

def export_as_tsv(data, path):
    os.makedirs(path, exist_ok=True)
    data= pd.DataFrame(data)
    data.columns = ['C'+str(c) for c in data.columns]
    data.index = ['IMG' + str(c) for c in data.index]
    data.to_csv(op.join(path, 'mnist.tsv'), sep='\t')

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Generate sample data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='input directory for raw mnist files', default='.')
    parser.add_argument('-o', metavar='OUTPUT_DIRECTORY', type=str, help='out directory for tabular mnist files', default='.')
    args = parser.parse_args()

    test_data, test_lables = load_mnist(args.d, 'train')
    export_as_tsv(test_data, args.o)