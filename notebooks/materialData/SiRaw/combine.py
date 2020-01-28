import numpy as np

# load the data
li_data = np.load("Li.npy")
schinke_data = np.load("Schinke.npy")
# chop the overlapping kischkat data
truncated_data = li_data[li_data[:,0] > schinke_data[-1,0]]
print(truncated_data)
# combine
combined_data = np.concatenate((schinke_data, truncated_data), axis=0)
print(combined_data)
# save
np.save("Si.npy", combined_data)
