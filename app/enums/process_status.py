from enum import Enum

from app.enums.strings import Strs


# the enum-class of statuses of the image-process
class ProcessStatus(Enum):
    LOADING = Strs.Status_Loading
    PROCESSING = Strs.Status_Processing
    DONE = Strs.Status_Done
    ERROR = Strs.Status_Error

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
