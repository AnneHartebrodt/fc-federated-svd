import numpy as np
import scipy as sc
import pandas as pd
import os
import math as math
import os.path as path

def data_import(filename, header=None, rownames=None, sep='\t', outfile=None, transpose = False):
    """
    Import data, drop 0 variance columns, scale data
    :param filename:
    :param ddpca:
    :param header: Header column? Same as in pandas read csv: None if no header row, row number of there is a header row
    :param rownames: specify the sample id colum: None, if no ids, column number if there are ids
    :return:
    """

    data = pd.read_csv(filepath_or_buffer=filename, header=header, sep=sep, index_col=rownames)
    sample_ids = data.index
    variable_names = data.columns.values
    data = data.values
    if transpose:
        data = data.transpose()
    # remove columns that have no variance
    #data, variable_names = drop0Columns(data,variable_names)
    if outfile is not None:
        export_clean_data(data, sample_ids, variable_names, outfile)
    return data, sample_ids, variable_names

def export_clean_data(data, sample_ids, variable_names, outfile):
    try:
        os.makedirs(outfile, exist_ok=True)
    except OSError:
        print("Creation of the directory %s failed" % outfile)

    # Transform data to pandas dataframe and print them to the specified location
    pd.DataFrame(data).to_csv(path_or_buf=path.join(outfile,'data_new.tsv'), sep='\t', header=False, index=False)
    if sample_ids is not None:
        pd.DataFrame(sample_ids).to_csv(path_or_buf=path.join(outfile,'sample.ids.tsv'), sep='\t', header=False,
                                    index=False)
    if variable_names is not None:
        pd.DataFrame(variable_names).to_csv(path_or_buf=path.join(outfile ,'variable.names.tsv'), sep='\t', header=False,
                                        index=False)

def scale_center_data_columnwise(data, center=True, scale_variance=False):
    return scale_center_data(data, center, scale_variance)

def scale_center_data(data, center=True, scale_variance=False):
    """
    This function centers the data by subtracting the column menans. Scaling to equal variance
    is done by divinding the entries by the column standard deviation.
    :param data: nxd numpy array , containing n samples with d variables
    :param center: if true, data is centered by subtracting the column mean
    :param scale_variance: if true, data is scaled by dividing by the standard deviation
    :return: the scaled data
    """
    # data.dtype = 'float'
    data = data.astype('float')

    if scale_variance or center:
        for column in range(data.shape[1]):
            mean_val = sc.mean(data[:, column])
            var_val = math.sqrt(sc.var(data[:, column], ddof=1))
            for elem in range(len(data[:, column])):
                if center:
                    data[elem, column] = data[elem, column] - mean_val
                if scale_variance:
                    data[elem, column] = data[elem, column] / var_val

    return data

def scale_data_0_1(data):
    """
    Scaling to values between 0 and 1 by dividing througgh the column euclidean norm
    :param data: nxd numpy array , containing n samples with d variables
    :param scale01: if true, columns are scaled to contain values between 0 and 1
    :return: the scaled data
    """
    # data.dtype = 'float'
    data = data.astype('float')

    # data has to be scaled between 0 and before the variance is scaled to
    # unit variance otherwise the it messes up with the analysis

    max_val = data.max()
    min_val = data.min()
    if (math.isclose(max_val, min_val, rel_tol=1E-15)):
        raise ZeroDivisionError('Insufficient variance in data matrix.')
    for column in range(data.shape[1]):
        for elem in range(len(data[:, column])):
            data[elem, column] = (data[elem, column] - min_val) / (max_val - min_val)
    return data


def scale_row_unit_norm(data):
    # axis = 1 - row norms, using 2 norm
    norms = np.linalg.norm(data, axis=1)
    for row in range(data.shape[0]):
        for elem in range(len(data[row, :])):
            data[row, elem] = data[row, elem] / norms[row]
    return data

def log_transform(data):
    data = data + np.ones(data.shape)
    data = np.log2(data)
    return data

def drop0Columns(data, variable_names, drop = False, noise = True):
    '''
    Remove columns that have a 0 mean or a zero variance.
    Alternatively: add a low pseudocount into columns that have 0 variance
    pseudocount= 1 in at most 10 variables.
    :param data: Data table
    :return: data without 0 columns
    '''

    indices = []
    for column in range(data.shape[1]):
        var_val = sc.std(data[:, column])
        if (math.isclose(var_val, 0, rel_tol=1E-15)):
            if drop:
                indices.append(column)
            if noise:
                cells=np.random.randint(0, data.shape[0], size=min(10, int(np.floor(data.shape[0]/2))))
                for c in cells:
                    data[c, column]=data[c, column]+1
    if drop:
        data = sc.delete(data, indices, 1)
        if variable_names is not None:
            variable_names = sc.array(variable_names)
            variable_names = sc.delete(variable_names, indices)

    return data, variable_names


