def main():
  import glob

  all_paths = glob.glob('gcts-vis/*')

  for inst_filename in all_paths:

    name = inst_filename.split('/')[1].split('.gct')[0]
    print(name)

main()
