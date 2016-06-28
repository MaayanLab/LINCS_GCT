def main():

  # minimally_proc_gct_to_tsv('gcts-vis')
  # minimally_proc_gct_to_tsv('gcts-orig')
  # minimally_proc_gct_to_tsv('gcts-failed-orig')

  filter_and_cluster_tsvs()

def filter_and_cluster_tsvs():
  '''
  This will filter and cluster the tsvs that are saved in the /txt directory,
  which have been made from the gcts.
  '''

  import glob
  all_paths = glob.glob('txt/*.txt')

  # all_paths = all_paths[3:4]

  for inst_filename in all_paths:

    name = inst_filename.split('/')[1].split('.txt')[0]

    try:
      make_json_from_tsv(name)
    except:
      print('failed to make json from tsv')

def make_json_from_tsv(name):
  '''
  make a clustergrammer json from a tsv file
  '''
  from clustergrammer import Network

  print('\n' + name)

  net = Network()

  filename = 'txt/'+ name + '.txt'

  net.load_file(filename)

  df = net.dat_to_df()

  net.swap_nan_for_zero()

  # zscore first to get the columns distributions to be similar
  net.normalize(axis='col', norm_type='zscore', keep_orig=True)

  # filter the rows to keep the perts with the largest normalizes values
  net.filter_N_top('row', 1000)

  num_rows = net.dat['mat'].shape[0]
  num_cols = net.dat['mat'].shape[1]

  print('num_rows ' + str(num_rows))
  print('num_cols ' + str(num_cols))

  if num_cols < 50 or num_rows < 1000:

    views = ['N_row_sum']
    net.make_clust(dist_type='cos', views=views)
    export_filename = 'json/' + name + '.json'
    net.write_json_to_file('viz', export_filename)

  else:
    print('did not cluster, too many columns ')


def minimally_proc_gct_to_tsv(inst_directory):
  '''
  minimally process (clean meta data) gcts and save as tsv files
  '''
  import glob
  all_paths = glob.glob(inst_directory + '/*.gct')
  # all_paths = all_paths[0:1]

  for inst_filename in all_paths:

    name = inst_filename.split('/')[1].split('.gct')[0]

    print(name)

    try:
      inst_gct = load_file(inst_filename)
      inst_df = gct_to_df(inst_gct)

      # save
      filename = 'txt/' + name + '.txt'
      inst_df.to_csv(filename, sep='\t')

    except:
      print('did not work\n===============')

    print('\n')

def load_file(filename):
  '''
  load the gct file using cmap/Zichen python script
  '''
  import cmap.io.gct as gct
  import cmap.io.plategrp as grp

  GCTObject = gct.GCT(filename)
  GCTObject.read(verbose=False)

  return GCTObject

def gct_to_df(gct):
  '''
  normalize, filter, clean meta data, return/save as pandas df
  '''
  import pandas as pd

  print(gct.matrix.shape)

  meta_data = get_meta_data(gct)

  mat = gct.matrix

  df = pd.DataFrame(data=mat, columns=meta_data['col'],
    index=meta_data['row'])

  return df

def get_meta_data(gct):
  '''
  define the metadata/categories from the gcts
  '''
  # generate unique names
  # may have to append name and id since names are not in general unique
  names = {}
  meta_data = {}
  cat_info = {}

  # get the available meta data headers for the rows/cols
  cat_titles = {}
  # get hte gene symbol meta data field from the row data
  cat_titles['tmp_row'] = gct.get_rhd()
  # get the perturbagen description meta data field from the column data
  cat_titles['tmp_col'] = gct.get_chd()

  for inst_rc in ['row', 'col']:

    # remove all id categories
    cat_titles[inst_rc] = []
    for tmp_title in cat_titles['tmp_'+inst_rc]:

      # if 'ID' not in tmp_title:
      cat_titles[inst_rc].append(tmp_title)

    cat_info[inst_rc] = {}

    # print(inst_rc)

    # tmp use ids, since they are unique
    if inst_rc == 'row':

      if 'smName' in cat_titles['row']:
        tmp_names = gct.get_row_meta('smName')
      elif 'smallmolecule_smName' in cat_titles['row']:
        tmp_names = gct.get_row_meta('smallmolecule_smName')
      else:
        tmp_names = gct.get_row_meta('id')

      names[inst_rc] = tmp_names

    elif inst_rc == 'col':
      names[inst_rc] = gct.get_column_meta('id')

    # determine which categories (meta data) will be included
    # there must be more than one unique category and the number of unique
    # categories must not equal the number of data points
    for inst_title in cat_titles[inst_rc]:

      if inst_rc == 'row':
        inst_cats = gct.get_row_meta(inst_title)
      elif inst_rc == 'col':
        inst_cats = gct.get_column_meta(inst_title)

      num_data = len(inst_cats)

      unique_cats = list(set(inst_cats))

      # remove blank strings from list
      unique_cats = filter(None, unique_cats)

      num_unique_cats = len(unique_cats)

      if num_unique_cats > 1 and num_unique_cats < num_data:

        cat_info[inst_rc][inst_title] = inst_cats

    # define metadata tuples
    # this includes names and categories with optional titles
    meta_data[inst_rc] = []

    for i in range(len(names[inst_rc])):

      # names and categories are stored as tuples
      name_tuple = ()

      # get individual row/col name - making the names unique
      inst_name = names[inst_rc][i] + ' ' + str(i)

      name_tuple = name_tuple + (inst_name,)

      all_titles = cat_titles[inst_rc]

      for inst_title in all_titles:

        if inst_title != 'ind':

          if inst_title in cat_info[inst_rc]:

            # get individual category
            inst_cat_name = inst_title + ': ' + cat_info[inst_rc][inst_title][i]

            name_tuple = name_tuple + (inst_cat_name,)

      # save the entire tuple
      meta_data[inst_rc].append(name_tuple)

  return meta_data

main()
