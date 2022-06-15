from enum import Enum
from apps.svd.Steps import Step
# communication parameters
class COParams(Enum):

    def __init__(self, name, smpc):
        self.n = name
        self.smpc = smpc

    @staticmethod
    def from_str(string_value):
        if string_value == 'H global':
            return COParams.H_GLOBAL
        elif string_value == 'H local':
            return COParams.H_LOCAL
        elif string_value =='Step':
            return COParams.STEP
        elif string_value == 'finished':
            return COParams.FINISHED
        elif string_value == 'Covariance matrix':
            return COParams.COVARIANCE_MATRIX
        elif string_value == 'Global Conorms':
            return COParams.GLOBAL_CONORMS
        elif string_value == 'Local Conorms':
            return COParams.LOCAL_CONORMS
        elif string_value == 'Global Eigenvector norm':
            return COParams.GLOBAL_EIGENVECTOR_NORM
        elif string_value == 'Local Eigenvector norm':
            return COParams.LOCAL_EIGENVECTOR_NORM
        elif string_value == 'R':
            return COParams.R
        elif string_value == 'Orthonormalisation done':
            return COParams.ORTHONORMALISATION_DONE
        elif string_value == 'PCs':
            return COParams.PCS
        elif string_value == 'Converged':
            return COParams.CONVERGED
        else:
            return None

    @staticmethod
    def to_step(string_value):
        if string_value == COParams.H_LOCAL.n:
            return Step.UPDATE_H
        elif string_value == COParams.COVARIANCE_MATRIX.n:
            return Step.COMPUTE_COVARIANCE
        elif string_value == COParams.LOCAL_EIGENVECTOR_NORM.n:
            return Step.COMPUTE_LOCAL_NORM
        elif string_value == COParams.LOCAL_CONORMS.n:
            return Step.COMPUTE_LOCAL_CONORM
        else:
            return None



    H_GLOBAL = 'H global', False
    H_LOCAL = 'H local', True
    STEP = 'Step', False
    FINISHED = 'finished', False
    COVARIANCE_MATRIX = 'Covariance matrix', True
    GLOBAL_CONORMS = 'Global Conorms', False
    LOCAL_CONORMS = 'Local Conorms', True
    GLOBAL_EIGENVECTOR_NORM = 'Global Eigenvector norm', False
    LOCAL_EIGENVECTOR_NORM = 'Local Eigenvector norm', True
    R = 'R', False
    CONVERGED = 'Converged', False
    ORTHONORMALISATION_DONE = 'Orthonormalisation done', False
    PCS = 'PCs', False
    ROW_NAMES = 'Row names', False
    SUMS = 'Sums', True
    NAN = 'Nans', False
    MEANS = 'Means', False
    SUM_OF_SQUARES = 'Sum of Squares', True
    STDS = 'Stds', False
    SAMPLE_COUNT = 'Sample count', True
    REDCOV = 'Reduced covariance', True
    U = 'Eigenvector', False
    PROJECTIONS = 'Projections', False
    SEND_PROJ = 'Send projections', False
    REMOVE = 'remove rows', False
    SELECT = 'select rows', False
    VARIANCES = 'variance', False

