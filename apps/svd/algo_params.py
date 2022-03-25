from enum import Enum

class QR(Enum):
    FEDERATED_QR = 'federated_qr'
    CENTRALISED_QR = 'centralised_qr'
    NO_QR = 'no_qr'

    @staticmethod
    def from_str(label):
        if label == 'federated_qr':
            return QR.FEDERATED_QR
        else:
            return QR.NO_QR

class PCA_TYPE(Enum):
    APPROXIMATE = 'approximate_pca'
    POWER_ITERATION = 'power_iteration'
    COVARIANCE = 'full_covariance'
    QR_PCA = 'qr_pca'
    RANDOMIZED = 'randomized'

    @staticmethod
    def from_str(label):
        if label == 'approximate_pca':
            return PCA_TYPE.APPROXIMATE
        elif label == 'full_covariance':
            return PCA_TYPE.COVARIANCE
        elif label == 'qr_pca':
            return PCA_TYPE.QR_PCA
        elif label == 'power_iteration':
            return PCA_TYPE.POWER_ITERATION
        elif label == 'randomized':
            return PCA_TYPE.RANDOMIZED
        else:
            return PCA_TYPE.APPROXIMATE
