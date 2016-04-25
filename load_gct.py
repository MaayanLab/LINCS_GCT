  
def main():
  import glob
  all_paths = glob.glob('gcts/*')

  done_jsons = glob.glob('json/*')

  for inst_filename in all_paths:
    name = inst_filename.split('/')[1].split('.gct')[0]

    found_done = False
    for done_name in done_jsons:
      done_name = done_name.split('/')[1].split('.json')[0]
      if name == done_name:
        found_done = True

        print('done with '+inst_filename)

    if found_done == False:

      print('\n'+inst_filename)
      try:
        df = load_file(inst_filename)
        make_viz_from_df(df, inst_filename)
      except:
        print('failed')

def make_viz_from_df(df, filename):
  from clustergrammer import Network

  net = Network()

  net.df_to_dat(df)
  net.swap_nan_for_zero()

  # zscore first to get the columns distributions to be similar 
  net.normalize(axis='col', norm_type='zscore', keep_orig=True)

  # filter the rows to keep the perts with the largest normalizes values
  net.filter_N_top('row', 2000)

  num_coluns = net.dat['mat'].shape[1]

  if num_coluns < 50:
    # views = ['N_row_sum', 'N_row_var']
    views = ['N_row_sum']
    net.make_clust(dist_type='cos', views=views)

    filename = 'json/' + filename.split('/')[1].replace('.gct','') + '.json'

    net.write_json_to_file('viz', filename)

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
  cat_info = {}

  for inst_rc in ['row', 'col']:

    cat_info[inst_rc] = {}

    # generate unique names for rows and columns 
    if inst_rc == 'row':

      if 'smName' in cat_titles['row']:
        tmp_names = GCTObject.get_row_meta('smName')
      elif 'smallmolecule_smName' in cat_titles['row']:
        tmp_names = GCTObject.get_row_meta('smallmolecule_smName')
      else: 
        tmp_names = GCTObject.get_row_meta('id')

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

      num_data = len(inst_cats)

      num_unique_cats = len(list(set(inst_cats)))

      if num_unique_cats > 1 and num_unique_cats < num_data:

        cat_info[inst_rc][inst_title] = inst_cats 


    # define metadata: names, categories with optional titles 
    meta_data[inst_rc] = []
    for i in range(len(names[inst_rc])):

      # names and categories are stored in tuple in pandas df 
      name_tuple = ()

      # get individual row/col name 
      inst_name = names[inst_rc][i]

      name_tuple = name_tuple + (inst_name,)

      all_titles = cat_titles[inst_rc]

      for inst_title in all_titles:

        if inst_title != 'ind' and inst_title !='id':


          if inst_title in cat_info[inst_rc]:

            # get individual category
            inst_cat_name = inst_title+ ': '+ cat_info[inst_rc][inst_title][i]

            name_tuple = name_tuple + (inst_cat_name,)

      # write the entire tuple 
      meta_data[inst_rc].append( name_tuple )

  mat = GCTObject.matrix 


  tmp_df = pd.DataFrame(data=mat, columns=meta_data['col'], 
    index=meta_data['row'])

  # # calc zscore of rows 
  # df_z = (tmp_df - tmp_df.mean())/tmp_df.std()

  df = {}
  # df['mat'] = df_z
  df['mat'] = tmp_df

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