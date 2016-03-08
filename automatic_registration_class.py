__author__ = 'vonbiebp'
from skimage.feature import (match_descriptors, ORB, plot_matches)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import skimage.io as io
from skimage.measure import ransac
from skimage.transform import ProjectiveTransform
from matplotlib.pyplot import savefig
import time

'''
The images need to be read in with the skimage.io module
The process then is as follows:
1) Import two images with io.imread()
2) Initiate the ImageRegistrationTool class with the two images
3) Call the get_translation_tool() method within the class and save the "tool" & "inliers"
            - This uses a skimage funtion, so we don't actually use "inliers", but
                that's how they do it...
4) Call the translate_rois() method with the "tool" as an input as well as the point
            to be tranlated.
            example: matcher.translate_rois(tool, src_point)

            - This returns the translated point that fits the destination image
Notes:
    - The number of n-keypoints in the get_translation_tool() method determines
        accuracy/robustness & how long it takes:

        higher # = more robust but takes longer

    - One challenge may be to make sure different coordinate system conventions don't
    get mixed up, some functions say top-left is 0,0  AND some sometimes bottom-left is 0,0

'''

class ImageRegistrationTool:
    '''
    This class will allow you to register/align two images automatically, and then return a
    transformation matrix that can be used to transform any coordinate from
    the source image to the destination image.
    *****It does not actually return a transformation matrix, but rather a scikit image object,
    which has the transformation matrix as an attribute and can use that to transform any coordinates.
    '''
    def __init__(self, src_image, dst_image):
        self.src_image = src_image
        self.dst_image = dst_image

    def get_translation_tool(self, n_keypoints=1000):

        # Convert images to grayscale
        src_image = rgb2gray(self.src_image)
        dst_image = rgb2gray(self.dst_image)

        # Initiate an ORB class object which can extract features & descriptors from images.
        # Set the amount of features that should be found (more = more accurate)
        descriptor_extractor = ORB(n_keypoints=n_keypoints)

        # Extract features and descriptors from source image
        descriptor_extractor.detect_and_extract(src_image)
        self.keypoints1 = descriptor_extractor.keypoints
        descriptors1 = descriptor_extractor.descriptors

        # Extract features and descriptors from destination image
        descriptor_extractor.detect_and_extract(dst_image)
        self.keypoints2 = descriptor_extractor.keypoints
        descriptors2 = descriptor_extractor.descriptors

        # Matches the descriptors and gives them rating as to how similar they are
        self.matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)

        # Selects the coordinates from source image and destination image based on the
        # indices given from the match_descriptors function.
        src = self.keypoints1[self.matches12[:, 0]][:, ::-1]
        dst = self.keypoints2[self.matches12[:, 1]][:, ::-1]

        # Filters out the outliers and generates the transformation matrix based on only the inliers
        model_robust, inliers = \
            ransac((src, dst), ProjectiveTransform,
                min_samples=4, residual_threshold=2)

        # This returns the object "model_robust" which contains the tranformation matrix and
        # uses that to translate any coordinate point from source to destination image.
        return model_robust, inliers

    def translate_rois(self, model_robust, src_point):
        '''
        :param model_robust:
        :param src_point: This should be in the form of [x,y]
        :return:
        '''

        dst_point = model_robust(src_point)
        return dst_point

'''
#################################################
#################################################

# Below is an example of how this class works!

#################################################
#################################################

# This is used to time how long the process takes
start_time = time.time()

#Read in images
src_image = io.imread("source_image.jpg")
dst_image = io.imread("destination_image.jpg")

# initiate matcher instance
matcher = ImageRegistrationTool(src_image, dst_image)

# extract matrix translating tool
tool, inliers = matcher.get_translation_tool()

# testing coordinate

# translate testing coordinates from src_image to dst_image
dst_point = matcher.translate_rois(tool, src_point)


##################################################################
##################################################################

#**********BELOW IS JUST FOR VISUALIZATION & TESTING**************

##################################################################
##################################################################

# Display the two images and the translated point

src_points = [[68,96], [68,15]]

dst_points = []

for item in src_points:
    dst_points.append(matcher.translate_rois(tool, item)[0].tolist())

print dst_points

f1 = plt.imshow(src_image)
plt.plot(*zip(*src_points), marker="o", color='r', ls='')
plt.show()

f2 = plt.imshow(dst_image)
plt.plot(*zip(*dst_points), marker="x", color='r', ls='')
plt.show()


# This repeats the process 50 times to see how often the function gets it right.
for i in range(50):
    matcher = ImageRegistrationTool(src_image, dst_image)
    tool, inliers = matcher.get_translation_tool()
    dst_points = []
    for item in src_points:
        dst_points.append(matcher.translate_rois(tool, item)[0].tolist())
    f2 = plt.imshow(dst_image)
    plt.plot(*zip(*dst_points), marker="x", color='r', ls='')
savefig('1000keypoints-smaller_image_timed.png')

print("--- %s seconds ---" % (time.time() - start_time))
'''
