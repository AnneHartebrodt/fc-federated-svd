import yaml
import os
import re
import os.path as op
from apps.svd.params import INPUT_DIR, OUTPUT_DIR
from apps.svd.algo_params import QR, PCA_TYPE
from shutil import copyfile


class FCConfig:
    def __init__(self):

        self.config_available = False
        self.input_file = None
        self.left_eigenvector_file = None
        self.right_eigenvector_file = None
        self.projection_file = None
        self.scaled_data_file = None
        self.k = 10
        self.sep = '\t'
        self.has_rownames = 0
        self.has_colnames = 0
        self.federated_dimensions = 'row'
        self.encryption = False
        self.use_smpc = False
        self.exponent = 3
        self.send_projections=False
        self.subsample = True

        self.center = True
        self.unit_variance = True
        self.highly_variable = True
        self.perc_highly_var = 0.1
        self.log_transform = True
        self.max_nan_fraction = 0.5

    def parse_configuration(self):
        print('[API] /setup parsing parameter file ')
        regex = re.compile('^config.*\.(yaml||yml)$')
        config_file = "ginger_tea.txt"
        # check input dir for config file
        files = os.listdir(INPUT_DIR)
        for file in files:
            if regex.match(file):
                config_file = op.join(INPUT_DIR, file)
                config_out = op.join(OUTPUT_DIR, file)
                break
        # check output dir for config file
        files = os.listdir(OUTPUT_DIR)
        for file in files:
            if regex.match(file):
                config_file = op.join(OUTPUT_DIR, file)
                break
        if op.exists(config_file):
            # Copy file to output folder
            print('[API] /setup config file found ... parsing file: ' + str(op.join(INPUT_DIR, config_file)))
            copyfile(config_file, config_out)

            self.config_available = True
            with open(config_file, 'r') as file:
                parameter_list = yaml.safe_load(file)
                parameter_list = parameter_list['fc_pca']

                # Files
                try:
                    self.input_file = parameter_list['input']['data']
                    self.input_dir = parameter_list['input']['dir']

                except KeyError:
                    print('YAML file does not follow specification: missing key .data. or .dir.')
                    raise KeyError

                try:
                    self.sep = parameter_list['input']['delimiter']
                except KeyError:
                    print('YAML file does not follow specification: delimiter not specified')
                    raise KeyError

                try:
                    self.output_dir = parameter_list['output']['dir']
                except KeyError:
                    print('YAML file does not follow specification: missing key: output-dir')
                    self.output_dir = ''
                    print('defaulting to .')

                try:
                    self.eigenvalue_file = parameter_list['output']['eigenvalues']
                    self.explained_variance_file = parameter_list['output']['explained_variance']
                except KeyError:
                    print('YAML file does not follow specification: missing key: eigenvalues')
                    print('Setting default: eigenvalues.tsv')
                    self.eigenvalue_file = 'eigenvalues.tsv'

                try:
                    self.explained_variance_file = parameter_list['output']['explained_variance']
                except KeyError:
                    print('YAML file does not follow specification: missing key: explained_variance')
                    print('Setting default: eigenvalues.tsv')
                    self.explained_variance_file = 'explained_variance.tsv'

                try:
                    self.output_delimiter = parameter_list['output']['delimiter']
                except KeyError:
                    print('YAML file does not follow specification: missing key: output delimiter')
                    print('Setting default: eigenvalues.tsv')
                    self.output_delimiter = '\t'

                try:
                    self.left_eigenvector_file = parameter_list['output']['left_eigenvectors']
                except KeyError:
                    print('YAML file does not follow specification: missing key: left_eigenvectors')
                    print('Setting default: left_eigenvectors.tsv')
                    self.left_eigenvector_file ='left_eigenvectors.tsv'

                try:
                    self.right_eigenvector_file = parameter_list['output']['right_eigenvectors']
                except KeyError:
                    print('YAML file does not follow specification: missing key: right_eigenvectors')
                    print('Setting default: right_eigenvectors.tsv')
                    self.right_eigenvector_file = 'right_eigenvectors.tsv'

                try:
                    self.projection_file = parameter_list['output']['projections']
                except KeyError:
                    print('YAML file does not follow specification: missing key: projections')
                    print('Setting default: projections.tsv')
                    self.projection_file =  'projections.tsv'

                try:
                    self.scaled_data_file =   parameter_list['output']['scaled_data_file']
                except KeyError:
                    print('YAML file does not follow specification: missing key: projections')
                    print('Setting default: projections.tsv')
                    self.scaled_data_file = 'scaled_data.tsv'

                try:
                    self.k = parameter_list['algorithm']['pcs']

                except KeyError:
                    print('K not specified, defaulting to 10')
                    self.k = 10

                try:
                    self.center = parameter_list['scaling']['center']
                    self.unit_variance = parameter_list['scaling']['variance']
                    self.highly_variable = parameter_list['scaling']['highly_variable']
                    self.perc_highly_var = parameter_list['scaling']['perc_highly_var']
                    self.log_transform = parameter_list['scaling']['log_transform']
                    self.max_nan_fraction = parameter_list['scaling']['max_nan_fraction']
                except KeyError:
                    print('Scaling functionalities not specified.')

                try:
                    self.send_projections = parameter_list['privacy']['send_projections']
                    self.subsample = parameter_list['privacy']['subsample_projections']
                    #self.use_smpc = parameter_list['privacy']['use_smpc']
                    #self.exponent = parameter_list['privacy']['exponent']
                    self.use_smpc=False
                    self.exponent = 3

                except KeyError:
                    print('YAML file does not follow specification: privacy settings')
                    raise KeyError

                print('[API] /setup config file found ... parsing done')

        else:
            print('[API] /setup no configuration file found')
            self.config_available = False