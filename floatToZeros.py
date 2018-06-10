import numpy as np

# with open('DATA/train_labels.dat', 'rb') as inputFile:
#    train_labels_floats = np.load(inputFile)

# train_labels_ints = train_labels_floats.astype(int)

# with open('DATA/train_labels.dat', 'wb') as outputFile:
#    np.save(outputFile, train_labels_ints)

# with open('DATA/train_data2.dat', 'rb') as inputFile:
#    train_data = np.load(inputFile)

# train_data_a = []
# train_data_b = []
# train_data_c = []

# # print(train_data[0])
# for reading in train_data:

#    a_series = []
#    b_series = []
#    c_series = []

#    # train_data[i] = train_data[i].reshape(3, 50)
#    for sample in reading:
#       a_series.append([sample[0]])
#       b_series.append([sample[1]])
#       c_series.append([sample[2]])

#    train_data_a.append(np.asarray(a_series))
#    train_data_b.append(np.asarray(b_series))
#    train_data_c.append(np.asarray(c_series))

# train_data_a = np.asarray(train_data_a)
# train_data_b = np.asarray(train_data_b)
# train_data_c = np.asarray(train_data_c)

# train_data = np.asarray([train_data_a, train_data_b, train_data_c])

# with open('DATA/train_data3.dat', 'wb') as outputFile:
#    np.save(outputFile, train_data)

with open('DATA/train_data2.dat', 'rb') as inputFile:
   train_data = np.load(inputFile)
   train_a = train_data[0]
   train_b = train_data[1]
   train_c = train_data[2]