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

    # the maximum length of the name (title) of an opencv-window
    'MAX_LEN_OF_WIN_NAME': 500,

    # the threshold parameter of retinaface when doing detections
    'RETINAFACE_THRESHOLD': 0.3,

    # the scale parameter of retinaface when doing detections
    'RETINAFACE_SCALE': 1.0,

    # the path of anime-avatar files
    'ANIME_AVATAR_DIR': 'D:/rekkursion/pictures/datasets/anime_avatar/',

    # the path of real-avatar files
    'REAL_AVATAR_DIR': 'D:/rekkursion/pictures/datasets/real_avatar/',

    # the scaling factor when resizing the opencv windows activated by mouse-wheeling
    'SCALING_FACTOR_ON_CV_WIN': 1.1,

    # the sampling rate of mouse-moving event (face-framing) on opencv-windows
    'SAMPLING_RATE_OF_FRAMING_ON_CV_WIN': 5,

    # the path for globally storing loaded images
    'RECENTLY_LOADED_IMAGES_PATH': './res/loaded_img/',

    # the string format for converting date-time into string
    'DATE_TIME_STR_FORMAT': '%Y_%m_%d_%H_%M_%S'
}
