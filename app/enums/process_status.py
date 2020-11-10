from enum import Enum


# the enum-class of statuses of the image-process
class ProcessStatus(Enum):
    LOADING = '載入中 Loading'
    PROCESSING = '處理中 Processing'
    DISPLAYING = '顯示中 Displaying'
    CLOSED = '已關閉 Closed'
    ERROR = '有錯誤發生 ERROR happened'

    # get the text-color of the designated process-status
    def get_text_color(self):
        if self == ProcessStatus.LOADING:
            return 103, 206, 255  # orange
        elif self == ProcessStatus.PROCESSING:
            return 253, 16, 19  # blue
        elif self == ProcessStatus.DISPLAYING:
            return 22, 251, 5  # green
        elif self == ProcessStatus.CLOSED:
            return 200, 200, 200  # grey
        else:  # ERROR
            return 0, 0, 255  # red
