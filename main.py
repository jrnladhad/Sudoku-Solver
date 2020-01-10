import Helper
from imgaug import augmenters as iaa
import ComputerVision.augment as augment_fns
from Sudoku import Sudoku


def main():
    model = None
    # Augmentation transformations
    # Can play around with these and massively expand the training set
    seq = iaa.Sequential([
        iaa.Crop(px=(2, 5)),  # Crop images from each side by 0 to 4px (randomly directions)
        iaa.Pad(px=(0, 4)),  # Pad images for each side by 0 to 4px (random directions)
        iaa.GaussianBlur(sigma=0.5),  # Gaussian blur with a kernel of size sigma
        iaa.Dropout(p=0.2),  # Adds randomised pixel dropout
        iaa.PerspectiveTransform(scale=0.075, keep_size=True)
    ])

    # Randomly splits the total archive into a training and test. Input the number of desired training images
    Helper.random_train_test(80)

    Helper.auto_classify(dry=False)  # Classifies digit images using .dat descriptors without manipulation
    Helper.auto_classify(train_only=True, imgaug_seq=seq, dry=False)  # Manipulation using imgaug
    Helper.auto_classify(train_only=True, aug_fn=augment_fns.contrast, dry=False)  # Custom manipulation

    Helper.create_from_train_test()  # Creates a pickled data file from classified digit images for training
    Helper.train()  # Train a network based on the classification mode (config.ini)
    results = Helper.test_board_recognition()


if __name__ == '__main__':
    main()
