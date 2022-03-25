import numpy as np
import scipy as sc
import pandas as pd
import apps.svd.spreadsheet_import as spi
import traceback
import copy

class TabData:
    def __init__(self, data, columns, rows, scaled):
        self.data = data
        self.columns = columns
        self.rows = rows
        self.scaled = scaled
        self.row_count = data.shape[0]
        self.col_count = data.shape[1]

    @classmethod
    def from_param(cls, data, columns, rows, scaled) -> 'TabData':
        "Initialize MyData from a dict's items"
        return cls(data, columns, rows, scaled)

    @classmethod
    def empty(cls) -> 'TabData':
        """
        Initialise an empty TabData object
        :return:
        """
        return cls(None, None, None, None)

    @classmethod
    def from_file(cls, filename, header=0, index=0, sep ='\t', keep_original=True, federated_dimension='columns') -> 'TabData':
        """

        :param filename:
        :param header:
        :param index:
        :param sep:
        :return:
        """

        data = pd.read_csv(filepath_or_buffer=filename, header=header, sep=sep, index_col=index)
        if data.shape[1] == 0:
            print('Suspiciously few columns ... using sniffer.')
            data = pd.read_csv(filepath_or_buffer=filename, header=header, sep=None, index_col=index, engine='python')

        sample_ids = np.array(data.index)
        variable_names = np.array(data.columns.values)
        if keep_original:
            data = data.values
            scaled = copy.deepcopy(data)
        else:
            scaled = data.values
            data = None

        #make sure the federated dimension are the columns.
        if federated_dimension == 'rows':
            data = data.T
            scaled = scaled.T
            return cls(data, sample_ids, variable_names, scaled)
        else:
            return cls(data, variable_names, sample_ids, scaled)




if __name__ == '__main__':
    tb = TabData.from_file('/home/anne/Documents/featurecloud/test-environment/controller/data/app_test/single/data_split/1/data.tsv')