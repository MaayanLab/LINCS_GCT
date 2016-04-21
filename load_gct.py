  
def main():
  import glob
  all_paths = glob.glob('gcts/*')

  for inst_filename in all_paths[:1]:
    
    print('\n'+inst_filename)
    try:
      load_file(inst_filename)
    except:
      print('failed')

def load_file(filename):

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

  for inst_rc in ['row', 'col']:

    for inst_title in cat_titles[inst_rc]:

      if inst_rc == 'row':
        inst_cats = GCTObject.get_row_meta(inst_title)

      elif inst_rc == 'col':
        inst_cats = GCTObject.get_column_meta(inst_title)
    

      # print('\nfound '+ str(len(inst_cats)) + ' categories for ' + inst_title)
      # print(inst_cats)


      ## ind is an index 

      ## row id is the name of the row
      ## col id is some id-number, I want to use smName (probably)




main()