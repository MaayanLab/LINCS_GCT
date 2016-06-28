def main():
  import glob

  all_paths = glob.glob('gcts-vis/*.gct')

  for inst_filename in all_paths:

    name = inst_filename.split('/')[1].split('.gct')[0]

    print(name)

    try:
      inst_gct = load_file(inst_filename)
      # print('works')

    except:
      print('did not work')

    print('\n')

def load_file(filename):
  import pandas as pd
  import cmap.io.gct as gct
  import cmap.io.plategrp as grp

  GCTObject = gct.GCT(filename)
  GCTObject.read(verbose=False)

  return GCTObject

def gct_to_df(gct):
  # get the available meta data headers for the rows/cols
  # cat_titles =
  pass

main()


