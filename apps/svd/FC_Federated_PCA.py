import os
import os.path as op
from apps.svd.TabData import TabData
import pandas as pd
import traceback
import numpy as np
import copy
from apps.svd.algo_params import QR
from apps.svd.SVD import SVD
from apps.svd.params import INPUT_DIR, OUTPUT_DIR
from apps.svd.COParams import COParams
import time
import scipy.linalg as la
import scipy.sparse.linalg as lsa
import apps.svd.shared_functions as sh
from apps.svd.params import INPUT_DIR, OUTPUT_DIR
import shutil

class FCFederatedPCA:
    def __init__(self):
        self.step = 0
        self.tabdata = None
        self.pca = None
        self.config_available = False
        self.out = None
        self.send_data = False
        self.computation_done = False
        self.coordinator = False
        self.step_queue = [] # this is the initial step queue
        self.state = 'waiting_for_start' # this is the inital state
        self.iteration_counter = 0
        self.converged = False
        self.outliers = []
        self.approximate_pca = True
        self.data_incoming = {}
        self.progress = 0.0
        self.silent_step=False
        self.use_smpc = False
        self.start_time = time.monotonic()
        self.pre_iterations = 10


        self.means = None
        self.std = None

        self.total_sampels = 0


    def copy_configuration(self, config):
        print('[STARTUP] Copy configuration and create dir')
        self.config_available = config.config_available
        self.input_file = op.join(INPUT_DIR,config.input_dir, config.input_file)
        os.makedirs(op.join(OUTPUT_DIR,config.output_dir), exist_ok=True)
        self.left_eigenvector_file = op.join(OUTPUT_DIR,config.output_dir,  config.left_eigenvector_file)
        self.right_eigenvector_file = op.join(OUTPUT_DIR,config.output_dir, config.right_eigenvector_file)
        self.eigenvalue_file = op.join(OUTPUT_DIR,config.output_dir, config.eigenvalue_file)
        self.projection_file = op.join(OUTPUT_DIR,config.output_dir, config.projection_file)
        self.scaled_data_file =  op.join(OUTPUT_DIR,config.output_dir, config.scaled_data_file)
        self.explained_variance_file = op.join(OUTPUT_DIR,config.output_dir, config.explained_variance_file)
        self.means_file = op.join(OUTPUT_DIR,config.output_dir, 'mean.tsv')
        self.stds_file = op.join(OUTPUT_DIR,config.output_dir, 'std.tsv')
        self.log_file = op.join(OUTPUT_DIR,config.output_dir, 'run_log.txt')
        self.output_delimiter = config.output_delimiter
        self.k = config.k

        self.exponent = config.exponent

        self.sep = config.sep
        self.has_rownames = config.has_rownames
        self.has_colnames = config.has_colnames
        self.send_projections = config.send_projections
        self.subsample = config.subsample

        self.center = config.center
        self.unit_variance = config.unit_variance
        self.highly_variable = config.highly_variable
        self.perc_highly_var = config.perc_highly_var
        self.log_transform = config.log_transform
        self.max_nan_fraction = config.max_nan_fraction


    def read_input_files(self):
        self.progress = 0.1
        self.tabdata = TabData.from_file(self.input_file, header=self.has_colnames,
                                         index=self.has_rownames, sep=self.sep)

        if self.log_transform:
            print('Log Transform performed')
            self.tabdata.scaled = np.log2(self.tabdata.scaled+1)

        nans = np.sum(np.isnan(self.tabdata.scaled), axis=1)
        infs = np.sum(np.isinf(self.tabdata.scaled), axis=1)
        isneginf = np.sum(np.isneginf(self.tabdata.scaled), axis=1)
        nans = np.sum([nans, isneginf, infs], axis=0)
        self.out = {COParams.ROW_NAMES.n : self.tabdata.rows, COParams.SAMPLE_COUNT.n: self.tabdata.col_count, COParams.NAN.n: nans}


    def init_random(self):
        print('[STARTUP] Random initialisation')
        self.progress = 0.2
        self.pca = SVD.init_random(self.tabdata, k=self.k)
        self.k = self.pca.k
        return True

    def compute_covariance(self):
        print('[STARTUP] Computing covariance matrix')
        self.init_random()
        self.progress = 0.2
        self.covariance = np.dot(self.tabdata.scaled, self.tabdata.scaled.T)
        print('TABDATA SCALED')
        print(self.tabdata.scaled)
        self.k = self.pca.k
        self.out = {COParams.REDCOV.n: self.covariance}



    def set_parameters(self, incoming):
        print('[API] Setting parameters')
        self.k2 = incoming[COParams.PCS.n]*2
        self.k = incoming[COParams.PCS.n]


    def select_rows(self, incoming):
        subset = incoming[COParams.ROW_NAMES.n]
        print(subset)
        d = {k: v for v, k in enumerate(self.tabdata.rows)}
        index = []
        for elem in subset:
            if elem in d:
                index.append(d[elem])
        print('INDEX')
        print(index)
        self.tabdata.scaled = self.tabdata.scaled[index,:]
        self.tabdata.rows = self.tabdata.rows[index]
        self.tabdata.row_count = len(self.tabdata.rows)



    def compute_sums(self):
        self.sums = np.nansum(self.tabdata.scaled, axis=1)

        self.out = {COParams.SUMS.n: self.sums, COParams.SAMPLE_COUNT.n: self.tabdata.col_count}

    def compute_sum_of_squares(self, incoming):
        self.means = incoming[COParams.MEANS.n].reshape((len(incoming[COParams.MEANS.n]),1))
        print(self.means.shape)
        self.sos = np.nansum(np.square(self.tabdata.scaled-self.means), axis=1)
        self.out = {COParams.SUM_OF_SQUARES.n: self.sos.flatten()}

    def apply_scaling(self, incoming, highly_variable=True):
        self.std = incoming[COParams.STDS.n].reshape((len(incoming[COParams.STDS.n]),1))
        self.variances = incoming[COParams.VARIANCES.n]
        remove = incoming[COParams.REMOVE.n] # remove due to 0
        select = incoming[COParams.SELECT.n] # select due to highly var
        # for row in range(self.tabdata.scaled.shape[0]):
        #     self.tabdata.scaled[row, :]= self.tabdata.scaled[row, :]- self.means[row,0]
        if self.center:
            self.tabdata.scaled = np.subtract(self.tabdata.scaled,self.means)


        # self.tabdata.scaled = np.delete(self.tabdata.scaled, remove)
        # self.tabdata.rows = np.delete(self.tabdata.rows, remove)
        if self.unit_variance:
            self.tabdata.scaled = self.tabdata.scaled/self.std

        if self.center:
            # impute. After centering, the mean should be 0, so this effectively mean imputation
            self.tabdata.scaled = np.nan_to_num(self.tabdata.scaled, nan=0, posinf=0, neginf=0)
        else:
            # impute
            self.tabdata.scaled = np.where(np.isnan(self.tabdata.scaled), self.means, self.tabdata.scaled)

        print(select)
        print(remove)
        if highly_variable:

            self.tabdata.scaled = self.tabdata.scaled[select, :]
            self.tabdata.rows = self.tabdata.rows[select]
            print('Selected')
        return self.tabdata.scaled.shape[0]


    def update_h(self, incoming):
        self.iteration_counter = self.iteration_counter + 1
        # First, update the local G estimate
        self.pca.H = incoming[COParams.H_GLOBAL.n]
        self.pca.G = np.dot(self.tabdata.scaled.T, self.pca.H)
        self.pca.S = np.linalg.norm(self.pca.G, axis=1)

        if self.iteration_counter<self.pre_iterations:
            self.pca.H_list.append(incoming[COParams.H_GLOBAL.n])
            self.pca.H = np.dot(self.tabdata.scaled, self.pca.G)
            self.out = {COParams.H_LOCAL.n: self.pca.H}
            next = 'iter'
        else:
            self.pca.H_list.append(incoming[COParams.H_GLOBAL.n])
            self.init_reduced()
            self.out = {COParams.REDCOV.n: self.pca.reduced_covariance}
            next = 'reduced'

        return next


    def save_scaled_data(self):
        saveme = pd.DataFrame(self.tabdata.scaled)
        saveme.to_csv(self.scaled_data_file, header=False, index=False, sep=str(self.output_delimiter))
        self.computation_done = True
        self.send_data = False
        return True

    def save_pca(self):
        # update PCA and save
        self.save_logs()
        if self.means is not None:
            pd.DataFrame(self.means).to_csv(self.means_file, sep=str(self.output_delimiter))
            pd.DataFrame(self.std).to_csv(self.stds_file, sep=str(self.output_delimiter))
        self.pca.to_csv(self.left_eigenvector_file, self.right_eigenvector_file, self.eigenvalue_file, sep=self.output_delimiter)

    def save_logs(self):
        with open(self.log_file, 'w') as handle:
            handle.write('iterations:\t'+str(self.iteration_counter)+'\n')
            handle.write('runtime:\t' + str(time.monotonic()-self.start_time)+'\n')
        self.out = {COParams.FINISHED: True}

    def orthogonalise_current(self, incoming):
        print('starting orthogonalise_current')
        self.global_conorms = incoming[COParams.GLOBAL_CONORMS.n]
        # update every cell individually
        for gp in range(len(self.global_conorms)):
            for row in range(self.pca.G.shape[0]):
                self.pca.G[row, self.current_vector] = self.pca.G[row, self.current_vector] - \
                                                      self.pca.G[row, gp] * self.global_conorms[gp]
        print('ending orthogonalise_current')


    def normalise_orthogonalised_matrix(self, incoming):
        print('Normalising')
        # get the last eigenvector norm
        self.all_global_eigenvector_norms.append(incoming[COParams.GLOBAL_EIGENVECTOR_NORM.n])

        # divide all elements through the respective vector norm.
        print(self.pca.G.shape)
        print(len(self.all_global_eigenvector_norms))
        for col in range(self.pca.G.shape[1]):
            for row in range(self.pca.G.shape[0]):
                self.pca.G[row, col] = self.pca.G[row, col] / self.all_global_eigenvector_norms[col]

        # reset eigenvector norms
        # Store current eigenvalue guess
        self.pca.S = copy.deepcopy(self.all_global_eigenvector_norms)


        self.current_vector = 0
        self.all_global_eigenvector_norms = []
        self.orthonormalisation_done = False
        self.computation_done = True
        self.send_data = False
        print('End normalising')




    def compute_projections(self):
        self.pca.projections = np.dot(self.tabdata.scaled.T, self.pca.H)
        print(self.pca.projections.shape)
        if self.subsample:
            cov = np.cov(self.pca.projections.T)
            print(cov.shape)
            mean = np.nanmean(self.pca.projections, axis=0)
            print(mean.shape)
            fake_data = np.random.multivariate_normal(mean = mean, cov = cov, size=self.pca.projections.shape[0])
            print(fake_data.shape)
            self.out = {COParams.PROJECTIONS.n: fake_data}
        else:
            self.out = {COParams.PROJECTIONS.n: self.pca.projections}


    def save_projections(self, incoming=None):
        # Save local clear text projections
        self.pca.save_projections(self.projection_file, sep=str(self.output_delimiter))
        # save global sampled projections

        if incoming is not None:
            self.pca.projections = incoming[COParams.PROJECTIONS.n]
            self.pca.save_projections(self.projection_file+'.all', sep=str(self.output_delimiter))

    def save_explained_variance(self):
        varex = sh.variance_explained(eigenvalues=self.pca.S, variances=self.variances)
        pd.DataFrame(varex).to_csv(self.explained_variance_file, sep=str(self.output_delimiter))

    def init_federated_qr(self):
        self.orthonormalisation_done = False
        self.current_vector = 0
        self.global_cornoms = []
        self.local_vector_conorms = []
        self.local_eigenvector_norm = -1
        self.all_global_eigenvector_norms = []

    def init_power_iteration(self):
        self.iteration_counter = 0
        self.converged = False
        self.pca.H = np.dot(self.tabdata.scaled, self.pca.G)
        self.out = {COParams.H_LOCAL.n: self.pca.H}
        self.init_federated_qr()


    def calculate_local_vector_conorms(self, incoming):
        vector_conorms = []
        # append the lastly calculated norm to the list of global norms
        self.all_global_eigenvector_norms.append(incoming[COParams.GLOBAL_EIGENVECTOR_NORM.n])
        for cvi in range(self.current_vector):
            vector_conorms.append(np.dot(self.pca.G[:, cvi], self.pca.G[:, self.current_vector]) / self.all_global_eigenvector_norms[cvi])
        self.local_vector_conorms = vector_conorms
        if self.current_vector == self.k:
            self.orthonormalisation_done = True
        local_conorms = [float(a) for a in self.local_vector_conorms]
        self.out = {COParams.LOCAL_CONORMS.n: local_conorms}
        #self.out = {COParams.LOCAL_CONORMS.n: 10}
        return True

    def compute_local_eigenvector_norm(self):
        print('starting eigenvector norms')
        # not the euclidean norm, because the square root needs to be calculated
        # at the aggregator
        self.local_eigenvector_norm = np.dot(self.pca.G[:, self.current_vector],
                                  self.pca.G[:, self.current_vector])
        self.current_vector = self.current_vector + 1
        print(self.k)
        if self.current_vector == self.k:
            self.orthonormalisation_done = True
        self.out = {COParams.LOCAL_EIGENVECTOR_NORM.n: float(self.local_eigenvector_norm)}
        return self.orthonormalisation_done


    def init_reduced(self):
        H_stack = np.concatenate(self.pca.H_list, axis=1)
        tempo_k = (H_stack.shape[1] - 1)
        H, S, G = lsa.svds(H_stack, k=tempo_k)
        H = np.flip(H, axis=1).T
        self.pca.reduced = np.dot(H, self.tabdata.scaled)
        self.pca.reduced_covariance = np.dot(self.pca.reduced, self.pca.reduced.T)

    def project_u(self, incoming):
        self.pca.G = np.dot(self.pca.reduced.T, incoming[COParams.U.n])
        self.pca.H = np.dot(self.pca.G.T, self.tabdata.scaled.T).T
        print(self.pca.G.shape)
        print(self.pca.H.shape)
        #self.out = {COParams.H_LOCAL.n: self.pca.H}

    def compute_g(self, incoming):
        self.k = min(self.k, incoming[COParams.H_GLOBAL.n].shape[1])
        self.pca.H = incoming[COParams.H_GLOBAL.n][:, 0:self.k]
        self.pca.G = np.dot(self.tabdata.scaled.T, self.pca.H)[:, 0:self.k]

    def project_u_cov(self, incoming):
        self.pca.H = incoming[COParams.U.n]
        print('Setting k')
        self.k = self.pca.H.shape[1]
        self.pca.G = np.dot(self.tabdata.scaled.T, self.pca.H)

    def save_h(self, incoming):
        self.pca.H = incoming[COParams.H_GLOBAL.n]

    def send_h(self):
        self.pca.H = np.dot(self.tabdata.scaled, self.pca.G)
        self.out = {COParams.H_LOCAL.n: self.pca.H}


    def copy_input_to_output(self):
        print('MOVE INPUT TO OUTPUT')
        shutil.copytree(INPUT_DIR, OUTPUT_DIR, dirs_exist_ok=True)







