from PIL import Image


def thumbnailer(path, sizes, finalpath):
    try:
        passed_image = Image.open(path)
        for size in sizes:
            image = passed_image.thumbnail((size, 100 * 10 ** 20))
            image.save(finalpath)
            print(f'Saved image of size: {size}')
    except IOError:
        print(f'Reached IOError')
