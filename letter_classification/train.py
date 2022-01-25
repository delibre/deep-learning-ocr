import glob
import sys

from sklearn.model_selection import train_test_split

import tensorflow.keras as keras 
from keras.models import Model
from keras.layers import Dense, Input
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten
from keras import backend as k
import pandas as pd
import numpy as np


if __name__ == '__main__':
   if len(sys.argv) != 2:
      raise ValueError('you must pass a path for the model to be saved')

   dfs = list()
   for filepath in glob.glob('fonts/*.csv'):
      print(filepath)
      dfs.append(pd.read_csv(filepath))

   print('concatenating')
   fonts = pd.concat(dfs, axis=0)
   del dfs
   print('concatenated', fonts.shape[0])

   print('filtering')
   fonts_ascii = fonts.loc[fonts['m_label'] < 128]
   del fonts
   X = fonts_ascii.iloc[:, 12:]
   print('filtered', X.shape[0])

   print('processing')
   X = np.array(X, dtype=np.uint8)
   y = np.array(fonts_ascii['m_label'], dtype=np.uint8)
   del fonts_ascii

   x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

   img_rows, img_cols=20, 20
   
   if k.image_data_format() == 'channels_first':
      x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
      x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
      inpx = (1, img_rows, img_cols)
   
   else:
      x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
      x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
      inpx = (img_rows, img_cols, 1)
      

   x_train = x_train.astype('float32')
   x_test = x_test.astype('float32')
   x_train /= 255
   x_test /= 255

   y_train = keras.utils.to_categorical(y_train)
   y_test = keras.utils.to_categorical(y_test)
   print('processed')

   inpx = Input(shape=inpx)
   layer1 = Conv2D(32, kernel_size=(3, 3), activation='relu')(inpx)
   layer21 = Conv2D(64, (3, 3), activation='relu')(layer1)
   layer22 = Conv2D(64, (3, 3), activation='relu')(layer21)
   layer3 = MaxPooling2D(pool_size=(3, 3))(layer22)
   layer4 = Dropout(0.5)(layer3)
   layer5 = Flatten()(layer4)
   layer6 = Dense(250, activation='sigmoid')(layer5)
   layer7 = Dense(y_train.shape[1], activation='softmax')(layer6)

   model = Model([inpx], layer7)
   model.compile(optimizer=keras.optimizers.Adam(),
               loss=keras.losses.categorical_crossentropy,
               metrics=['accuracy'])

   try:
      model.fit(x_train, y_train, epochs=30, batch_size=500)
   except KeyboardInterrupt:
      print('interrupted')
   finally:
      score = model.evaluate(x_test, y_test, verbose=0)
      print('loss=', score[0])
      print('accuracy=', score[1])

      model.save(sys.argv[1])
      print('model saved')
