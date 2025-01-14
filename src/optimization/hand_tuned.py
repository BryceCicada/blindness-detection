from src.constants import TEST_IMAGE_WIDTH
from src.constants import TEST_IMAGE_HEIGHT
from src.optimization.base import ExperimentGenerator
from src.optimization.experiment import Experiment
from src.preprocess.features import bens
from src.preprocess.features import enhance_fovea
from src.preprocess.normalize import crop_dark_borders
from src.preprocess.normalize import resize
from src.preprocess.normalize import eight_bit_normalization


EXPERIMENTS = [
    Experiment(
        description="Simple mnist cnn",
        pipeline_stages=[
            (
                "crop_dark_borders",
                {
                    "tol": 10
                }
            ),
            (
                "resize",
                {
                    "width": TEST_IMAGE_WIDTH,
                    "height": TEST_IMAGE_HEIGHT
                }
            ),
            (
                "bens",
                {
                    "image_weight": 4,
                    "blur_window": (0, 0),
                    "blur_sigma_x": 20,
                    "blur_weight": -4,
                    "bias": 128
                }
            ),
            (
                "eight_bit_normalization",
                {}
            )
        ],
        train_test_data_frames=["/home/jake/Data/aptos2019-blindness-detection/train.csv"],
        train_test_directories=["/home/jake/Data/aptos2019-blindness-detection/train_images"],
        model=("MnistExampleV01", {}),
        batch_size=100,
        optimzier=("SGD", {"lr": 0.001, "momentum": 0.9}),
        test_size=0.2,
        max_epochs=3
    ),
    Experiment(
        pipeline_stages=[
            (
                "crop_dark_borders",
                {
                    "tol": 10
                }
            ),
            (
                "resize",
                {
                    "width": TEST_IMAGE_WIDTH,
                    "height": TEST_IMAGE_HEIGHT
                }
            ),
            (
                "enhance_fovea",
                {
                    "radius": 11,
                    "border_tol": 25,
                    "blur_sigma": 4,
                    "fovea_aoi_size": 160,
                    "width": TEST_IMAGE_WIDTH,
                    "height": TEST_IMAGE_HEIGHT
                }
            ),
            (
                "bens",
                {
                    "image_weight": 4,
                    "blur_window": (0, 0),
                    "blur_sigma_x": 10,
                    "blur_weight": -4,
                    "bias": 128
                }
            ),
            (
                "eight_bit_normalization",
                {}
            )
        ],
        description="Development",
        train_test_data_frames=["/home/jake/Data/aptos2019-blindness-detection/train.csv"],
        train_test_directories=["/home/jake/Data/aptos2019-blindness-detection/train_images"],
        model=("MnistExampleV01", {}),
        batch_size=100,
        optimzier=("SGD", {"lr": 0.001, "momentum": 0.9}),
        test_size=0.2,
        max_epochs=3
    ),
]


class HandTunedExperiements(ExperimentGenerator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._experiments = EXPERIMENTS
        self._index = 0

    def __next__(self):
        if self._index <= len(self._experiments):
            return self._experiments[self._index]
        else:
            raise StopIteration

    def __iter__(self):
        self._index = 0
        return self
