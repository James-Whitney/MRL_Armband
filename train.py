from keras import models, layers, Input, utils, Model
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
import numpy as np
import sys
import csv

def randomize(a, b):
    shuffle = np.random.shuffle(np.arange(len(b)))
    a[0] = a[0][shuffle]
    
    for i in range(len(a)):
        a[i] = a[i][shuffle][0]

    return a, b[shuffle]

def build_network(train_data):

    # print(train_data.shape[2])
    channel_a_input = Input(shape=(train_data[0].shape[1], train_data[0].shape[2]), dtype='float32', name='channel_a')
    channel_a_Conv1D = layers.Conv1D(32, 5, activation='relu') (channel_a_input)
    channel_a_Conv1D = layers.Conv1D(32, 3, activation='relu') (channel_a_Conv1D)

    channel_b_input = Input(shape=(train_data[1].shape[1], train_data[1].shape[2]), dtype='float32', name='channel_b')
    channel_b_Conv1D = layers.Conv1D(32, 5, activation='relu') (channel_b_input)
    channel_b_Conv1D = layers.Conv1D(32, 3, activation='relu') (channel_b_Conv1D)

    channel_c_input = Input(shape=(train_data[2].shape[1], train_data[2].shape[2]), dtype='float32', name='channel_c')
    channel_c_Conv1D = layers.Conv1D(32, 5, activation='relu') (channel_c_input)
    channel_c_Conv1D = layers.Conv1D(32, 3, activation='relu') (channel_c_Conv1D)
    

    concatenate = layers.concatenate([channel_a_Conv1D, channel_b_Conv1D, channel_c_Conv1D], axis=-1)

    LSTM_hidden = layers.LSTM(64) (concatenate)

    hidden = layers.Dense(256, activation='relu') (LSTM_hidden)
    hidden = layers.Dense(64, activation='relu') (hidden)
    hidden = layers.Dense(32, activation='relu') (hidden)

    outputLayer = layers.Dense(6, activation='softmax') (hidden)

    model = Model([channel_a_input, channel_b_input, channel_c_input], outputLayer)

    print(model.summary())

    model.compile(
        optimizer='rmsprop',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model
    valid_gen = generator(train_data, train_labels, split, batch_size, True)


def generator(train_data, train_labels, valid_split, batch_size, isValid, min, max):
    
    split = int(len(train_labels) * (1.0 - valid_split))

    for i in range(len(train_data)):
        train_data[i] = train_data[i][:split] if isValid else train_data[i][split:]
        
    train_next = 0

    samplesList = []
    for dataset in train_data:
        samplesList.append([])

    while True:
        for i in range(len(samplesList)):
            samplesList[i] = list()
        labels = list()

        for i in range(len(train_labels)):
            for i in range(len(samplesList)):
                samplesList[i].append(train_data[i][train_next] + np.random.randint(min, max))

            labels.append(train_labels[train_next])
            train_next += 1
            if train_next == len(train_labels):
                train_next = 0

        for i in range(len(samplesList)):
            samplesList[i] = np.asarray(samplesList[i])

        yield samplesList, np.asarray(labels)


def main():
    epochs = 10
    batch_size = 80
    val_split = 0.2

    # load datasets
    with open('DATA/train_data2.dat', 'rb') as inputFile:
        train_data_np = np.load(inputFile)
    with open('DATA/train_labels.dat', 'rb') as inputFile:
        train_labels = np.load(inputFile)

    train_data = []
    for data_set in train_data_np:
        train_data.append(data_set)

    train_data, train_labels = randomize(train_data, train_labels)

    for dataset in train_data:
        print(dataset.shape)

    train_gen = generator(train_data, train_labels, val_split, batch_size, False, -100, 100)
    valid_gen = generator(train_data, train_labels, val_split, batch_size, True, -100, 100)

    model = build_network(train_data)

    model.fit_generator(
        train_gen,
        steps_per_epoch=batch_size,
        epochs=epochs,
        validation_data=valid_gen,
        validation_steps=batch_size,
        verbose=1)

    # model.fit(
    #     [train_data_a, train_data_b, train_data_c], train_labels,
    #     shuffle=False,
    #     epochs=epochs,
    #     batch_size=batch_size,
    #     validation_split=val_split)

    # train_data, train_labels = shuffle(train_data, train_labels, random_state=0)

    # train_data_a = []
    # train_data_b = []
    # train_data_c = []

    # # print(train_data[0])
    # for reading in train_data:

    #     a_series = []
    #     b_series = []
    #     c_series = []

    #     # train_data[i] = train_data[i].reshape(3, 50)
    #     for sample in reading:
    #         a_series.append([sample[0]])
    #         b_series.append([sample[1]])
    #         c_series.append([sample[2]])

    #     train_data_a.append(np.asarray(a_series))
    #     train_data_b.append(np.asarray(b_series))
    #     train_data_c.append(np.asarray(c_series))

    # train_data_a = np.asarray(train_data_a)
    # train_data_b = np.asarray(train_data_b)
    # train_data_c = np.asarray(train_data_c)

    # # print(train_data_a[0])
    # # exit()

    # train_data = [train_data_a, train_data_b, train_data_c]


    

    # print(train_data.shape)
    # print(train_labels.shape)


    # # checkpoint
    # checkpoint = ModelCheckpoint(
    #     "Model.h5",
    #     monitor='val_acc',
    #     verbose=1,
    #     save_best_only=True,
    #     mode='max')
    # callbacks_list = [checkpoint]

    

        # callbacks=callbacks_list)

    return


if __name__ == '__main__':
    main()
