# Copyright 2020 Stanford University, Los Alamos National Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from tensorflow.keras import backend
from tensorflow.keras.layers import Input, Flatten, Dense, Activation, Conv2D, MaxPooling2D, Concatenate, concatenate
from tensorflow.keras import optimizers

from flexflow.keras_exp.models import Model
from flexflow.keras.datasets import cifar10

import flexflow.core as ff
import numpy as np
import argparse
import gc
  
def top_level_task():
  backend.set_image_data_format('channels_first')
  num_classes = 10
  
  num_samples = 10000
  
  (x_train, y_train), (x_test, y_test) = cifar10.load_data(num_samples)
  
  x_train = x_train.astype('float32')
  x_train /= 255
  y_train = y_train.astype('int32')
  print("shape: ", x_train.shape)
  
  input_tensor1 = Input(shape=(3, 32, 32), dtype="float32")
  output_tensor1 = Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu")(input_tensor1)
  output_tensor1 = Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu")(output_tensor1)
  output_tensor1 = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding="valid")(output_tensor1)
  model1 = Model(input_tensor1, output_tensor1)
  
  input_tensor2 = Input(shape=(32, 14, 14), dtype="float32")
  output_tensor2 = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu")(input_tensor2)
  output_tensor2 = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu")(output_tensor2)
  output_tensor2 = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding="valid")(output_tensor2)
  output_tensor2 = Flatten()(output_tensor2)
  output_tensor2 = Dense(512, activation="relu")(output_tensor2)
  output_tensor2 = Dense(num_classes)(output_tensor2)
  output_tensor2 = Activation("softmax")(output_tensor2)
  model2 = Model(input_tensor2, output_tensor2)
  
  input_tensor3 = Input(shape=(3, 32, 32), dtype="float32")
  output_tensor3 = model1(input_tensor3)
  output_tensor3 = model2(output_tensor3)
  model = Model({3: input_tensor3}, output_tensor3)
  
  opt = optimizers.SGD(learning_rate=0.01)
  model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy', 'sparse_categorical_crossentropy'])
  print(model.summary())

  model.fit(x_train, y_train, epochs=1)

if __name__ == "__main__":
  print("Functional API, cifar10 cnn nested")
  top_level_task()
  gc.collect()