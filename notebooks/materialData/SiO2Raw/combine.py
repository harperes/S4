import numpy as np

# load the data
lemarchand_data = np.load("Lemarchand.npy")
kischkat_data = np.load("Kischkat.npy")
# chop the overlapping kischkat data
truncated_data = kischkat_data[kischkat_data[:,0] > lemarchand_data[-1,0]]
# combine
combined_data = np.concatenate((lemarchand_data, truncated_data), axis=0)
# save
np.save("SiO2.npy", combined_data)
