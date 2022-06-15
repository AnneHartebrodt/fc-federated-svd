# FeatureCloud Singular Value decomposition Application

## FeatureCloud

The FeatureCloud AppStore allow non-computer scientists to make use of privacy-aware federated learning by providing federated Apps that run within the FeatureCloud framework. For more information on Featurecloud please visit [featurecloud.ai](www.featurecloud.ai)


## Federated SVD
Singular value decomposition/Prinicpal Component Analysis is a versatile tool frequently used in biomedical workflows. For this application, we developed a fast and accurate federated singular value decomposition algorithm. Singular value decomposition returns two sets of mututally orthonormal vectors which can be used to approximate the data. One set of eigenvectors can be seen as a feature reprentation. The other set of vectors summarizes information about each sample. The 'sample singular vectors' should not be shared due to potential privacy issues. In [1] we describe an efficient, privacy aware PCA scheme which runs in a constant number of rounds, is acurate and suitable for high-dimensional data. 

For more information on the fedeated singular value decomposition you might find [this repository](https://github.com/AnneHartebrodt/federated-pca-simulation) useful where simulation code for the algorithms can be found.

## Input specification
The application requires the follwing input:
- a config.yml file, which specifies the input and output files and parameters
- a data file in tabular format. IMPORTANT: data can be partitioned in multiple ways in federated learning (more information and illustration: [here](https://github.com/AnneHartebrodt/federated-pca-simulation)). This data set needs to be formatted correctly, which means there must be an overlap between the column (feature) names over the different sites. The rows are the 'federated' dimension, i.e. the samples. Row and column names are mandatory.
```
fc_pca:
  algorithm:
    pcs: 5 # Choose the number of PCs to return
  input:
    dir: '' # In which directory is the data located
    data: localData.csv # name of the data file
    delimiter: ; # delimiter of the input
  output:
    dir: pca # output will be saved in a directory called 'pca'
    eigenvalues: eigenvalues.tsv
    left_eigenvectors: left_eigenvectors.tsv
    projections: localData.csv
    right_eigenvectors: right_eigenvectors.tsv
    scaled_data_file: scaled_data.tsv
    variance_explained_file: variance_explained.csv
  privacy:
    send_projections: false # If this is true, the projections (lower dimensionality data points) will be sent to all participants.
    subsample_projections: true # Fake data points are created instead of sending the original
  scaling:
    center: true # substract the mean from each variable
    highly_variable: false # choose only highly variable genes
    log_transform: true # log transform the data before analysis
    max_nan_fraction: 1 # How many NA's are tolerated (NAs are imputed with the mean of the variable)
    perc_highly_var: 0.9 # How many of the highly variable genes are to be chosen.
    variance: true # Scale to unit variance.
```


### References
<a id="1">[1]</a> 
Hartebrodt, A., Röttger,R. and Blumenthal, D., 2022. Federated singular value decomposition for high dimensional data. arXiv preprint arXiv:2205.12109

<a id="1">[2]</a> 
Matschinske, J., Späth, J., Nasirigerdeh, R., Torkzadehmahani, R., Hartebrodt, A., Orbán, B., Fejér, S., Zolotareva,
O., Bakhtiari, M., Bihari, B. and Bloice, M., 2021.
The FeatureCloud AI Store for Federated Learning in Biomedicine and Beyond. arXiv preprint arXiv:2105.05734.
