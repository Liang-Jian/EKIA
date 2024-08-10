import os

def save_image(func):
    def wrapper(*args, **kwargs):
        image = func(*args, **kwargs)
        filename = kwargs.get('filename', 'image.png')
        if not os.path.exists('images'):
            os.makedirs('images')
        with open(os.path.join('images', filename), 'wb') as f:
            f.write(image)
        print(f'Saved image {filename}')
        return image
    return wrapper

@save_image
def generate_image(width=640, height=480, color=(255, 255, 255), filename='image.png'):
    # generate the image here
    pass



generate_image()




