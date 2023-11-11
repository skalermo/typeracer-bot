import imgaug.augmenters as iaa
import numpy as np
import cv2


class WaveWarp(iaa.meta.Augmenter):
    def __init__(self, amplitude: (float, float) = (2, 5), frequency: (float, float) = (0.1, 0.5)):
        super().__init__()
        self.amplitude = amplitude
        self.frequency = frequency

    def augment_image(self, image, hooks=None):
        amplitude = self.random_state.uniform(*self.amplitude)
        frequency = self.random_state.uniform(*self.frequency)
        return self._wave_warp(image, amplitude, frequency)

    @staticmethod
    def _wave_warp(image, amplitude, frequency):
        height, width, _ = image.shape
        distorted_image = np.copy(image)

        for y in range(width):
            for x in range(height):
                # Calculate the offset in the x-direction using a sine wave
                offset_x = amplitude * np.sin(2 * np.pi * frequency * y / height)

                # Apply the offset to the x-coordinate
                new_x = int(x + offset_x)

                if 0 <= new_x < height:
                    # Copy the pixel value from the original position to the distorted position
                    # distorted_image[y, x] = image[y, new_x]
                    distorted_image[x, y] = image[new_x, y]

        return distorted_image

    def get_parameters(self):
        return [self.amplitude, self.frequency]


class CustomLine(iaa.meta.Augmenter):
    def __init__(self, thickness: (int, int) = (1, 3)):
        super().__init__()
        self.thickness = thickness

    def augment_image(self, image, hooks=None):
        x1, y1, x2, y2 = self.random_state.random(4)
        height, width, _ = image.shape
        pt1 = (int(x1 * width), int(y1 * height))
        pt2 = (int(x2 * width), int(y2 * height))
        thickness = self.random_state.randint(*self.thickness)
        return cv2.line(image, pt1, pt2, color=(0, 0, 0, 255), thickness=thickness)

    def get_parameters(self):
        return [self.thickness]
