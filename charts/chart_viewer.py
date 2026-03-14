import time
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

IMAGE_FILE = "bot_dashboard.png"
REFRESH_SECONDS = 300  # 5 minutes


def main():

    plt.ion()

    fig, ax = plt.subplots()
    ax.axis("off")

    img = None
    im_obj = None

    while True:

        if os.path.exists(IMAGE_FILE):

            img = mpimg.imread(IMAGE_FILE)

            if im_obj is None:
                im_obj = ax.imshow(img)
            else:
                im_obj.set_data(img)

            fig.canvas.draw_idle()

        else:
            print("Waiting for chart.png...")

        plt.pause(1)
        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    main()
