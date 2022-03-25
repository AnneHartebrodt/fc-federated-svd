from enum import Enum

class Step(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, step, smpc):
        self.step = step
        self.smpc = smpc


    LOAD_CONFIG = 'Loading configuration parameters', False
    WAIT_FOR_PARAMS = 'Waiting for parameters', False
    READ_DATA = 'Reading data', False
    COMPUTE_H_LOCAL = 'Updating local eigenvectors', True
    COMPUTE_G_LOCAL = 'Updating local left eigenvectors', False
    AGGREGATE_H = 'Aggregating eigenvectors', False
    INIT_POWER_ITERATION = 'Inititialising Power iteration', True
    UPDATE_H = 'Updating local eigenvectors (no QR)', True
    SAVE_SVD = 'Saving SVD', False
    SAVE_SCALED_DATA = 'Saving scaled data', False
    UPDATE_H_REDUCED = 'Update reduced H', True
    FINALIZE = 'Finalising', False
    FINISHED = 'Finished', False
    COMPUTE_PROJECTIONS = 'Computing projections', False
    SAVE_PROJECTIONS = 'Saving projections', False


    APPROXIMATE_LOCAL_PCA = 'Approximating local subspaces', True
    AGGREGATE_SUBSPACES = 'Aggregating approx. subspaces', False

    COMPUTE_COVARIANCE = 'Computing local covariance matrix', True
    AGGREGATE_COVARIANCE = 'Aggregating covariance matrix', False

    COMPUTE_QR = 'Computing local QR', True
    AGGREGATE_QR = 'Aggregating R matrices', False

    COMPUTE_LOCAL_NORM = 'Computing local norm', True
    COMPUTE_LOCAL_CONORM = 'Computing local co-norm', True
    AGGREGATE_NORM = 'Aggregating norms', False
    AGGREGATE_CONORM = 'Aggregating co-norms', False
    ORTHOGONALISE_CURRENT = "orthogonalising eigenvectors (federated QR)", False
    NORMALISE_G = 'Normalising orthongonalised matrix', False

