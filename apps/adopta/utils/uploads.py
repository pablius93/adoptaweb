from datetime import datetime


def get_image_filename(instance, filename):
    extension = filename.split('.')[-1]
    now = datetime.now().strftime('%H%M%S%f')
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    return "uploads/images/{}/{}/{}/{}.{}".format(year, month, day, now, extension)


def get_thumbnail_filename(instance, filename):
    extension = filename.split('.')[-1]
    now = datetime.now().strftime('%H%M%S%f')
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    return "uploads/images/{}/{}/{}/thumb/{}.{}".format(year, month, day, now, extension)
