# some configuration pertains to the model training
configuration = {
    # the number of epochs when doing training
    'EPOCH': 25,

    # the batch size
    'BATCH_SIZE': 32,

    # the designated size of images
    'SIZE_OF_IMGS': (128, 128),

    # the names of classes
    'CLS_NAMES': ('2D', '3D'),

    # the path of anime-avatar files
    'ANIME_AVATAR_DIR': 'D:/rekkursion/pictures/datasets/anime_avatar/',

    # the path of real-avatar files
    'REAL_AVATAR_DIR': 'D:/rekkursion/pictures/datasets/real_avatar/'
}
