import time
start_time = time.time()

from clustergrammer import Network
net = Network()

net.load_file('txt/rc_two_cats.txt')
# net.load_file('txt/tmp.txt')

views = ['N_row_sum','N_row_var']

net.make_clust(dist_type='cos',views=views , dendro=True, sim_mat=True)

net.write_json_to_file('viz', 'json/mult_view.json')
net.write_json_to_file('sim_row', 'json/mult_view_sim_row.json')
net.write_json_to_file('sim_col', 'json/mult_view_sim_col.json')

elapsed_time = time.time() - start_time

print('\n\nelapsed time')
print(elapsed_time)
