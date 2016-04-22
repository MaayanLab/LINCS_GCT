  
def main():
  import glob
  # all_paths = glob.glob('gcts/*')
  all_paths = ['gcts/LDS-1207.gct']

  for inst_filename in all_paths:

    # print('\n'+inst_filename)
    # try:
    df = load_file(inst_filename)
    # except:
    #   print('failed')

    make_viz_from_df(df)

def make_viz_from_df(df):
  from clustergrammer import Network

  net = Network()

  net.df_to_dat(df)
  net.swap_nan_for_zero()

  views = ['N_row_sum', 'N_row_var']
  net.make_clust(dist_type='cos', views=views)

  net.write_json_to_file('viz', 'json/example_gct.json')

def load_file(filename):
  import pandas as pd
  import cmap.io.gct as gct
  import cmap.io.plategrp as grp

  GCTObject = gct.GCT(filename)
  GCTObject.read(verbose=False)

  print(GCTObject.matrix.shape)

  # get the available meta data headers for data columns and row
  cat_titles = {}
  # get the gene symbol meta data field from the row data
  cat_titles['row'] = GCTObject.get_rhd()
  # get the perturbagen description meta data field from the column data
  cat_titles['col'] = GCTObject.get_chd()

  # generate unique names, append name and id (since names are not unique)
  names = {}
  meta_data = {}

  for inst_rc in ['row', 'col']:

    # generate unique names for rows and columns 
    if inst_rc == 'row':
      tmp_names = GCTObject.get_row_meta('smName')
      tmp_ids = GCTObject.get_row_meta('id') 
      names['row'] = merge_name_id(tmp_names, tmp_ids)

    elif inst_rc == 'col':
      names['col'] = GCTObject.get_column_meta('id')

    # determine which categories (meta-data) will be included 
    # must be more than one unique category and the number of unique categories
    # must not equal the number of data points
    for inst_title in cat_titles[inst_rc]:

      if inst_rc == 'row':
        inst_cats = GCTObject.get_row_meta(inst_title)
      elif inst_rc == 'col':
        inst_cats = GCTObject.get_column_meta(inst_title)

    # define metadata: names, categories with optional titles 
    meta_data[inst_rc] = []
    for inst_name in names[inst_rc]:
      meta_data[inst_rc].append( (inst_name, 'something: yes') )

  mat = GCTObject.matrix 

  df = {}
  df['mat'] = pd.DataFrame(data=mat, columns=meta_data['col'], 
    index=meta_data['row'])

  return df 

def merge_name_id(tmp_names, tmp_ids):
  new_names = []
  for i in range(len(tmp_names)):
    inst_name = tmp_names[i]
    inst_id = tmp_ids[i]

    new_name = inst_name+'-'+inst_id

    new_names.append(new_name)

  return new_names

main()