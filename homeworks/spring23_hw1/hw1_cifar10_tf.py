"""
CS/DS 549 Spring 2023 Programming and Model Training Assignment

The goal is to define a better model and training hyperparameters to beat the minimum
required evaluation/validation accuracy of 0.82  at the very least, but also to compete
in the class challenge for best training results.

Only edit code between the comments:
#########################
# Edit code here
# vvvvvvvvvvvvvvvvvvvvvvv
<code>
# ^^^^^^^^^^^^^^^^^^^^^^^
"""
import wandb
from wandb.keras import WandbMetricsLogger

import tensorflow as tf
from tensorflow import keras
from keras import layers
import tensorflow_datasets as tfds
from matplotlib import pyplot as plt
from tensorflow.keras.applications.vgg16 import VGG16



if __name__ == '__main__':

    # Leave entity="bu-spark-ml" and project="hw1_spring2023"
    # put your BU username in the `group=` parameter
    wandb.init(
        project="hw1_spring2023",  # Leave this as 'hw1_spring2023'
        entity="bu-spark-ml",  # Leave this
        group="dskahill",  # <<<<<<< Put your BU username here
        notes="32-512 w 1000 dense, 75 epochs"  # <<<<<<< You can put a short note here
    )

    """
    Use tfds to load the CIFAR10 dataset and visualize the images and train.

    The datasets used are:
    https://www.tensorflow.org/datasets/catalog/cifar10
    https://www.tensorflow.org/datasets/catalog/cifar10_corrupted

    tfds.load() whill first check if the dataset is already downloaded to the
    path in `data_dir`. If not, it will download the dataset to that path..
    """
    # Load the CIFAR10 dataset
    print("Loading CIFAR10 dataset...")
    (ds_cifar10_train, ds_cifar10_test), ds_cifar10_info = tfds.load(
        'cifar10',
        split=['train', 'test'],
        #data_dir='/datasets/tensorflow_datasets',
        shuffle_files=True, # load in random order
        as_supervised=True, # Include labels
        with_info=True, # Include info
    )

    # Optionally uncomment the next 3 lines to visualize random samples from each dataset
    #fig_train = tfds.show_examples(ds_cifar10_train, ds_cifar10_info)
    #fig_test = tfds.show_examples(ds_cifar10_test, ds_cifar10_info)
    #plt.show()  # Display the plots

    def normalize_img(image, label):
        """Normalizes images: `uint8` -> `float32`."""
        return tf.cast(image, tf.float32) / 255., label

    # Prepare cifar10 training dataset
    ds_cifar10_train = ds_cifar10_train.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
    ds_cifar10_train = ds_cifar10_train.cache()     # Cache data
    ds_cifar10_train = ds_cifar10_train.shuffle(ds_cifar10_info.splits['train'].num_examples)
    ds_cifar10_train = ds_cifar10_train.batch(32)  # <<<<< To change batch size, you have to change it here
    ds_cifar10_train = ds_cifar10_train.prefetch(tf.data.AUTOTUNE)

    # Prepare cifar10 test dataset
    ds_cifar10_test = ds_cifar10_test.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
    ds_cifar10_test = ds_cifar10_test.batch(32)    # <<<<< To change batch size, you have to change it here
    ds_cifar10_test = ds_cifar10_test.cache()
    ds_cifar10_test = ds_cifar10_test.prefetch(tf.data.AUTOTUNE)

    #transfer learning code
    base = VGG16(weights='imagenet', include_top=False, input_shape=(32,32,3))
    base.trainable = False

    # Define the model here
    """ best model 1
    tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),
        
        tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(.5),
    """

    """ best model 2
    tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(.5),
    """
    model = tf.keras.models.Sequential([keras.Input(shape=(32, 32, 3)),
        tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),
        
        tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(256, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Dropout(.5),

        tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.Conv2D(512, kernel_size=(3,3), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(.5),

        layers.Flatten(),
        tf.keras.layers.Dense(1000, activation='relu'),
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        tf.keras.layers.Dense(10, activation="softmax")
    ])

    # Log the training hyper-parameters for WandB
    # If you change these in model.compile() or model.fit(), be sure to update them here.
    wandb.config = {
        #####################################
        # Edit these as desired
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        "learning_rate": 0.001,
        "optimizer": "adam",
        "epochs": 75,
        "batch_size": 32
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    }

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    history = model.fit(
        ds_cifar10_train,
        epochs=75,
        validation_data=ds_cifar10_test,
        callbacks=[WandbMetricsLogger()]
    )

    wandb.finish()
