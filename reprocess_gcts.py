def main():
  import glob

  all_paths = glob.glob('gcts-vis/*.gct')

  for inst_filename in all_paths:

    name = inst_filename.split('/')[1].split('.gct')[0]

    print(name)

    # try:
    df = load_file(inst_filename)
    print('works')

    # except:
    #   print('did not work')

    print('\n')

def load_file(filename):
  import pandas as pd
  import cmap.io.gct as gct
  import cmap.io.plategrp as grp

  GCTObject = gct.GCT(filename)
  GCTObject.read(verbose=False)

  print(GCTObject.matrix.shape)

main()


