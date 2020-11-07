import tensorflow
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from utils.help_func import *
from model_training.model import RekkModel


# do the process of building, training, and saving the model up
def do_process():
    with tensorflow.device('/cpu:0'):
        # step 1. load the images as data
        animes = load_imgs_from_dir(cfg['ANIME_AVATAR_DIR'])
        reals = load_imgs_from_dir(cfg['REAL_AVATAR_DIR'])
        print('num of animes:', animes.shape[0])
        print('num of  reals:', reals.shape[0])
        # step 2. split the data
        x_train, y_train, x_test, y_test = split_data(animes, reals, 0.7)
        # step 3. categorize the label data
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)
        # step 4. create the CNN model
        model = RekkModel((cfg['SIZE_OF_IMGS'][0], cfg['SIZE_OF_IMGS'][1], 3), 2)
        # step 5. train the built model
        model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=cfg['EPOCH'])
        # step 6. predict the testing-data to evaluate the trained model
        print('\nEvaluation:')
        loss, accuracy = model.evaluate(x_test, y_test, cfg['BATCH_SIZE'], 1)
        print('loss:', loss, '| accuracy:', accuracy, end='\n\n')
        # step 7. save the weights of the trained model
        model.save_weights('./pretrained_model/rekk_model.h5')
        print('The model has been trained and saved successfully.')
        print('END of training')
        return model


# main
if __name__ == '__main__':
    init_gpus()
    do_process()
