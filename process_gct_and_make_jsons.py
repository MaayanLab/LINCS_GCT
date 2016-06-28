def main():

  # minimally_proc_gct_to_df('gcts-vis')
  # minimally_proc_gct_to_df('gcts-orig')
  # minimally_proc_gct_to_df('gcts-failed-orig')

  filter_and_cluster_tsvs()

def filter_and_cluster_tsvs():
  '''
  This will filter and cluster the tsvs that are saved in the /txt directory,
  which have been made from the gcts.
  '''

  pass


def minimally_proc_gct_to_df(inst_directory):
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
  cat_titles['row'] = gct.get_rhd()
  # get the perturbagen description meta data field from the column data
  cat_titles['col'] = gct.get_chd()

  for inst_rc in ['row', 'col']:

    cat_info[inst_rc] = {}

    # tmp use ids, since they are unique
    if inst_rc == 'row':
      names[inst_rc] = gct.get_row_meta('id')
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

      num_unique_cats = len(list(set(inst_cats)))

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
