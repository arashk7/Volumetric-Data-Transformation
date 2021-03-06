import numpy as np
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD

from test_hand_h5.AkTools import excel_write, calc_error

import h5py



def ak_train(num_epoch):
    h5f = h5py.File('hand_train_32_S3.h5', 'r')
    X = h5f['X'].value
    Y = h5f['Y'].value

    h5f = h5py.File('hand_test_32_S3.h5', 'r')
    X_test = h5f['X'].value
    Y_test = h5f['Y'].value

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(11, activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd)

    min = 100
    for i in range(num_epoch):
        model.fit(X, Y, batch_size=30, epochs=1, verbose=0)
        p = model.predict(X_test, batch_size=30, verbose=0)
        err = calc_error(p, 30)
        print("epoch ", i,": error = ", err, "%")
        if err < min:
            model.save('model_S3.h5')
            print("new minimum")
            min = err


        model = load_model('model_S3.h5')
    print("finish train")
    p = model.predict(X_test,batch_size=30,verbose=0)
    precent = calc_error(p, 30)
    print ("error is: ", precent)

# excel_write('test.xls', p)
# print(p)
