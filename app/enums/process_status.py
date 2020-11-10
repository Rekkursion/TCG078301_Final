from enum import Enum


# the enum-class of statuses of the image-process
class ProcessStatus(Enum):
    LOADING = '載入或等待中 Loading or waiting'
    PROCESSING = '處理中 Processing'
    DONE = '處理完畢 Done'
    ERROR = '有錯誤發生 ERROR happened'

    # get the text-color of the designated process-status
    def get_text_color(self):
        if self == ProcessStatus.LOADING:
            return 67, 142, 243  # orange
        elif self == ProcessStatus.PROCESSING:
            return 253, 16, 19  # blue
        elif self == ProcessStatus.DONE:
            return 16, 109, 2  # green
        else:  # ERROR
            return 0, 0, 255  # red
