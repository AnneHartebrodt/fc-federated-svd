from apps.svd.FC_Federated_PCA import FCFederatedPCA
import  numpy as np
from apps.svd.Steps import Step
import scipy as sc
import scipy.sparse.linalg as lsa
import scipy.linalg as la
from apps.svd.shared_functions import eigenvector_convergence_checker
from apps.svd.algo_params import QR, PCA_TYPE
import apps.svd.shared_functions as sh
from apps.svd.COParams import COParams

class AggregatorFCFederatedPCA(FCFederatedPCA):
    def __init__(self):
        self.dummy = None
        self.coordinator = True
        FCFederatedPCA.__init__(self)

    def unify_row_names(self, incoming):
        print(incoming)
        mysample_count = 0
        myintersect = set(incoming[0][COParams.ROW_NAMES.n])
        for s in incoming:
            myintersect = myintersect.intersection(set(s[COParams.ROW_NAMES.n]))
            mysample_count = s[COParams.SAMPLE_COUNT.n]+mysample_count
        self.total_sampels = mysample_count
        self.out = {COParams.PCS.n: self.k, COParams.SEND_PROJ: self.send_projections}
        self.out[COParams.ROW_NAMES.n] = list(myintersect)
        print('[API] [COORDINATOR] row names identified!')

    def compute_means(self, incoming):
        print(incoming)
        my_sums = []
        my_samples = 0
        for s in incoming:
            my_sums.append(s[COParams.SUMS.n])
            my_samples = my_samples+s[COParams.SAMPLE_COUNT.n]
        my_sums = np.stack(my_sums)
        my_sums = np.nansum(my_sums, axis=0)
        my_sums = my_sums/my_samples
        self.out = {COParams.MEANS.n : my_sums}
        self.number_of_samples = my_samples

    def compute_std(self, incoming):
        my_ssq  = []
        for s in incoming:
            print(s[COParams.SUM_OF_SQUARES.n].shape)
            my_ssq.append(s[COParams.SUM_OF_SQUARES.n])
        my_ssq = np.stack(my_ssq)
        my_ssq = np.nansum(my_ssq, axis=0)
        my_ssq = np.sqrt(my_ssq/(self.number_of_samples-1))
        print(my_ssq)
        hv = int(np.floor(self.tabdata.scaled.shape[0] * self.perc_highly_var))
        order = np.argsort(self.std.flatten())[0:hv]
        remove = np.where(self.std.flatten()==0)
        self.out = {COParams.STDS.n : my_ssq, COParams.SELECT.n: order, COParams.REMOVE.n: remove}

    def compute_h_local_g(self):
        # this is the case for federated PCA and the first iteration
        # of centralised PCA
        super(AggregatorFCFederatedPCA, self).compute_h_local_g()
        self.computation_done = True
        # send data if smpc is used
        self.send_data = self.use_smpc
        return True


    # def compute_g(self, incoming):
    #     self.pca.H = incoming[COParams.H_GLOBAL.n]
    #     self.converged = incoming[COParams.CONVERGED.n]
    #     self.pca.G = np.dot(self.tabdata.scaled.T, self.pca.H)
    #     if self.federated_qr == QR.FEDERATED_QR:
    #         self.queue_qr()
    #         # send local norms
    #         if self.converged:
    #             self.queue_shutdown()
    #         else:
    #             self.step_queue = self.step_queue + [Step.COMPUTE_H_LOCAL, Step.AGGREGATE_H, Step.COMPUTE_G_LOCAL]
    #
    #     # next local step is to follow!
    #     self.computation_done = True
    #     self.send_data = False
    #     print(self.step_queue)
    #     return True



    def aggregate_h(self, incoming):
        '''
        This step adds up the H matrices (nr_SNPs x target dimension) matrices to
        achieve a global H matrix
        :param parameters_from_clients: The local H matrices
        :return: Global H matrix to be sent to the client
        '''

        print("Adding up H matrices from clients ...")
        global_HI_matrix = np.zeros(incoming[0][COParams.H_LOCAL.n].shape)
        for m in incoming:
            global_HI_matrix += m[COParams.H_LOCAL.n]
        print('H matrices added up')
        global_HI_matrix, R = la.qr(global_HI_matrix, mode='economic')

        print(self.iteration_counter)
        # The previous H matrix is stored in the global variable
        if self.pca.previous_h.shape == global_HI_matrix.shape:
            # shape mismatch when modes change
            converged, deltas = eigenvector_convergence_checker(global_HI_matrix, self.pca.previous_h, tolerance=self.epsilon)
        else:
            converged = self.converged

        if self.iteration_counter == self.max_iterations or converged:
            if self.algorithm == PCA_TYPE.RANDOMIZED:
                self.converged = True
                next = 'converged'
        else:
            if self.algorithm == PCA_TYPE.RANDOMIZED and self.iteration_counter>self.pre_iterations:
                next = 'update_h_reduced'
            else:
                next = 'update_h'
        self.out = {COParams.H_GLOBAL.n: global_HI_matrix, COParams.CONVERGED.n: self.converged}
        return next


    def aggregate_randomized(self, incoming):
        global_cov = np.zeros(incoming[0][COParams.REDCOV.n].shape)

        for m in incoming:
            global_cov += m[COParams.REDCOV.n]
        # unbiased
        global_cov = global_cov/(self.total_sampels-1)
        if self.k >= min(global_cov.shape):
            self.k = min(global_cov.shape) - 1
        u,s,v = lsa.svds(global_cov, k=self.k)
        u = np.flip(u, axis=1)
        self.out = {COParams.U.n: u}



    def aggregate_eigenvector_norms(self, incoming):
        print(incoming)
        eigenvector_norm = 0
        for v in incoming:
            eigenvector_norm = eigenvector_norm + v[COParams.LOCAL_EIGENVECTOR_NORM.n]

        eigenvector_norm = np.sqrt(eigenvector_norm)
        # increment the vector index after sending back the norms
        if self.current_vector == self.k:
            self.orthonormalisation_done = True
        self.out = {COParams.GLOBAL_EIGENVECTOR_NORM.n: eigenvector_norm, COParams.ORTHONORMALISATION_DONE.n: self.orthonormalisation_done}
        self.computation_done = True
        self.send_data = True
        return True

    def aggregate_conorms(self, incoming):
        print('aggregating co norms')
        print(incoming)
        if self.use_smpc:
            conorms = np.array(incoming[0][COParams.LOCAL_CONORMS.n])
        else:
            conorms = np.zeros(len(incoming[0][COParams.LOCAL_CONORMS.n]))
            for n in incoming:
                conorms = np.sum([conorms, n[COParams.LOCAL_CONORMS.n]], axis=0)
        self.out = {COParams.GLOBAL_CONORMS.n: conorms}
        self.computation_done = True
        self.send_data = True



    def compute_covariance(self):
        super(AggregatorFCFederatedPCA, self).compute_covariance()
        self.iteration_counter = self.iteration_counter + 1
        self.computation_done = True
        # send data if smpc is used
        self.send_data = self.use_smpc
        return True

    def redistribute_projections(self, incoming):
        myproj = []
        for n in incoming:
            myproj.append(n[COParams.PROJECTIONS.n])
        myproj = np.concatenate(myproj, axis=0)
        self.out = {COParams.PROJECTIONS.n:myproj}


