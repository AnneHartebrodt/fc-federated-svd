import apps.svd.TabData as TabData
import apps.svd.shared_functions as sh
import json
import pandas as pd
import copy

class SVD:
    def __init__(self, H, G, S, tabdata: 'TabData', k: int):
        self.H = H
        self.G = G
        self.S = S
        self.tabdata = tabdata
        self.k = k
        self.previous_h = copy.deepcopy(H)
        self.projections = None

        self.H_list = []
        self.reduced = None
        self.rG = None
        self.rH = None

    @classmethod
    def init_random(cls,  tabdata, k=10) -> 'SVD':
        """
        Initialise an SVD object with random matrices
        :param k: number of eigenvectors, (default: 10)
        :param tabdata: TabData object.
        :return:
        """

        k = min(tabdata.col_count, k)
        H = sh.generate_random_gaussian(tabdata.row_count, k)
        G = sh.generate_random_gaussian(tabdata.col_count, k)
        S = sh.generate_random_gaussian(k, 1).flatten()
        return cls(H, G, S, tabdata, k)

    @classmethod
    def init_param(cls, H, G, S, tabdata, k=10) -> 'SVD':
        """
        Initialise an SVD object from pre-existing vector
        :param H: right eigenvector matrix
        :param G: left eigenvector matrix
        :param S: eigenvalues
        :param tabdata: TabData object
        :param k: number of eigenvectors
        :return: instance of class 'SVD'
        """
        return cls(H, G, S, tabdata, k)

    @classmethod
    def init_local_subspace(cls,  tabdata, k=10) -> 'SVD':
        """
        Initialise an SVD object using the local subspace
        method
        :param k: number of eigenvectors, (default: 10)
        :param tabdata: TabData object.
        :return:
        """
        k = min(tabdata.col_count, k)
        print(k)
        H, S, G, k = sh.svd_sub(tabdata.data, ndims=k*2)
        return cls(H, G, S, tabdata, k)

    @classmethod
    def from_file(cls, filename) -> 'SVD':
        #TODO: implement this
        return (None, None, None, None, None)

    @classmethod
    def from_json(cls, json_file) -> 'SVD':
        # TODO: implement this
        return (None, None, None, None, None)



    def to_json(self):

        return True

    def to_csv(self, left_eigenvector_file, right_eigenvector_file, eigenvalue_file, sep='\t'):
        print('saving pca'+left_eigenvector_file)
        print(sep)
        pd.DataFrame(self.H, index=self.tabdata.rows).to_csv(left_eigenvector_file, sep=str(sep))
        pd.DataFrame(self.G, self.tabdata.columns).to_csv(right_eigenvector_file, sep=str(sep))
        pd.DataFrame(self.S).to_csv(eigenvalue_file, sep=str(sep), header=False, index=False)


    def save_projections(self, projection_file, sep='\t'):
        save = pd.DataFrame(self.projections, index=self.tabdata.columns)
        save.to_csv(projection_file, sep=str(sep), header=True, index=True)