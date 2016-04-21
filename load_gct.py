'''
This script contains examples for reading .gctx files in Python.
'''

import cmap.io.gct as gct
import cmap.io.plategrp as grp

# give input file
# path_to_gctx_file = '/xchip/cogs/l1ktools/data/modzs_n272x978.gctx'
path_to_gctx_file = 'gcts/LDS-1207.gct'

# read the full data file
GCTObject = gct.GCT(path_to_gctx_file)
GCTObject.read(verbose=False)

print(GCTObject.matrix.shape)

# get the available meta data headers for data columns and row
cat_titles = {}
# get the gene symbol meta data field from the row data
cat_titles['row'] = GCTObject.get_rhd()
# get the perturbagen description meta data field from the column data
cat_titles['col'] = GCTObject.get_chd()

for inst_rc in ['row', 'col']:

  for inst_title in cat_titles[inst_rc]:

    if inst_rc == 'row':
      inst_cats = GCTObject.get_row_meta(inst_title)

    elif inst_rc == 'col':
      inst_cats = GCTObject.get_column_meta(inst_title)
  

    print('\nfound '+ str(len(inst_cats)) + ' categories for ' + inst_title)





