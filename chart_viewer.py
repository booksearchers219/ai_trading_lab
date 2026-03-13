import time
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

IMAGE_FILE = "bot_dashboard.png"
REFRESH_SECONDS = 300   # 5 minutes


def load_and_display():
    if not os.path.exists(IMAGE_FILE):
        print("Chart file not found:", IMAGE_FILE)
        return None

    img = mpimg.imread(IMAGE_FILE)

    plt.clf()
    plt.imshow(img)
    plt.axis("off")
    plt.title("Trading Chart (auto refresh every 5 minutes)")

    plt.draw()


def main():

    plt.ion()  # interactive mode
    plt.figure(figsize=(10, 6))

    while True:
        print("Refreshing chart...")
        load_and_display()
        plt.pause(1)

        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    main()

