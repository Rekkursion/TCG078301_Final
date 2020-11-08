from enum import Enum


# the enum-class of types of supported file (image & video)
class SupportedFileType(Enum):
    IMAGE = ('.jpg', '.jpeg', '.png', '.bmp')
    VIDEO = ('.mp4', '.avi')
    NO_SUPPORTED = ()

    # check if a certain filename is a supported file or not
    @staticmethod
    def is_supported(filename: str):
        r_idx = filename.rindex('.')
        ext = filename[r_idx:]
        for e in SupportedFileType:
            if ext in e.value:
                return e
        return SupportedFileType.NO_SUPPORTED
