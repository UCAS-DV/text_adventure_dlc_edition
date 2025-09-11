#init commit
import matplotlib.pyplot as plt #pip install matplotlib
import matplotlib.image as mpimg

# Displays Image
def display_image(image_path='images/World_map.png'):
    img = mpimg.imread(image_path)
    plt.imshow(img)
    plt.axis('off')  # Hide axes
    plt.title('World Map')  # Optional title
    plt.show()
