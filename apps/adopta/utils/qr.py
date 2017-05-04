import qrcode
import os


def generate_qr(url, path):
    img = qrcode.make(url)
    img.save(path)
