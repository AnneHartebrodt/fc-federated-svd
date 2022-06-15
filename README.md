# FeatureCloud Singular Value decomposition Application

## FeatureCloud

The FeatureCloud AppStore allow non-computer scientists to make use of privacy-aware federated learning by providing federated Apps that run within the FeatureCloud framework. For more information on Featurecloud please visit [featurecloud.ai](www.featurecloud.ai)


## Federated SVD
Singular value decomposition/Prinicpal Component Analysis is a versatile tool frequently used in biomedical workflows. For this application, we developed a fast and accurate federated singular value decomposition algorithm. Singular value decomposition returns two sets of mututally orthonormal vectors which can be used to approximate the data. One set of eigenvectors can be seen as a feature reprentation. The other set of vectors summarizes information about each sample. The 'sample singular vectors' should not be shared due to potential privacy issues. In [1] we describe an efficient, privacy aware PCA scheme which runs in a constant number of rounds, is acurate and suitable for high-dimensional data. 

For more information on the fedeated singular value decomposition you might find [this repository](https://github.com/AnneHartebrodt/federated-pca-simulation) useful where simulation code for the algorithms can be found.

## Usage
Please find the input specification and more information on the app website https://featurecloud.ai/app/federated-svd


## References
If you use the information provided on this page, please consider citing our work.

<a id="1">[1]</a> 
Hartebrodt, A., Röttger,R. and Blumenthal, D., 2022. Federated singular value decomposition for high dimensional data. arXiv preprint arXiv:2205.12109

<a id="1">[2]</a> 
Matschinske, J., Späth, J., Nasirigerdeh, R., Torkzadehmahani, R., Hartebrodt, A., Orbán, B., Fejér, S., Zolotareva,
O., Bakhtiari, M., Bihari, B. and Bloice, M., 2021.
The FeatureCloud AI Store for Federated Learning in Biomedicine and Beyond. arXiv preprint arXiv:2105.05734.
