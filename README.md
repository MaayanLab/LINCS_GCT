--- 6-28-2016
I'm reprocessing the original gcts and Ander's manually processed vis-gcts. I'll
process the gcts (clean meta-data, limit the number of rows, normalize) and save
in tsv format (with tuple names/cats).

Then I'll make the jsons for clustergrammer and save them to the json directory.

The script

  process_gct_and_make_jsons.py

processes (cleans/filters) the gcts and makes the clustergrammer jsons.

--- 5-13-2016

The processed (zscored, filtered, and category filtering) GCTs can be saved as tsvs that have row/col labels. See load_gct.py and the function process_GCT_export_tsv() for an example.

--- 5-5-2016

  I'm setting up clustergrammer.py to read in files in GCT format. The restults
will be visualized in clustergrammer.js.

