import sys
sys.path.append('/home/anne/Documents/featurecloud/apps/fc-federated-svd/')

import apps.svd.shared_functions as sh
import apps.svd.comparison as co
import pandas as pd
import argparse as ap
import numpy as np
import os as os
import os.path as op
import yaml
import markdown
import apps.svd.markdown_utils as md

def write_markdown_report(basedir, report, runstats=None):
    files = os.listdir(basedir)
    fl = []
    print(files)
    for f in files:
        fl.append(pd.read_csv(op.join(basedir, f), sep='\t', engine='python', header=0, index_col=None))
    table = pd.concat(fl)
    if runstats is not None:
        runs = pd.read_csv(op.join(basedir,'..' ,runstats), sep='\t', engine='python', header=0, index_col=None)

    table.to_csv(op.join(basedir, 'summary.tsv'), sep='\t', header=True,index=False)
    mdr = md.df_to_markdown(table)
    #mdr2 = md.df_to_markdown(runs)
    with open(report, 'w') as handle:
        handle.write('# Test report\n')
        handle.write('## Accuracy\n')
        handle.write(mdr+'\n')
        if runstats is not None:
            handle.write('## Run stats\n')
            #handle.write(mdr2)



if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Split complete data into test data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='input the report directory', default='.')
    parser.add_argument('-r', metavar='REPORT', type=str, help='report as markdown', default='.')
    parser.add_argument('-s', metavar='RUN STATS', type=str, help='run stats file', default=None)
    args = parser.parse_args()
    basedir = args.d

    write_markdown_report(basedir, args.r, args.s)


