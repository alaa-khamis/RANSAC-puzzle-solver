import random
import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt

# Get SIFT keypoints and descriptor
def SIFT(img, sift):
    
    keypoints, descriptor = sift.detectAndCompute(img, None)
    
    return keypoints, descriptor

# Calculate and return NXM distance matrix between two descriptors
def calculate_distance_matrix(desc1, desc2):

    dist = np.zeros((len(desc1), len(desc2)))

    dot_product = np.dot(desc1, desc2.T)
    desc1_norm = np.sum(desc1 ** 2, axis=1)
    desc2_norm = np.sum(desc2 ** 2, axis=1)

    dist = np.sqrt(np.maximum(desc1_norm.reshape(-1, 1) - 2 * dot_product + desc2_norm, 0))

    return dist

# Find the matches
# Returns list of matches that pass the ratio test
def find_matches(dist, desc):

    matches = []

    for i, _ in enumerate(desc):
        
        distances = dist[i]
        sorted_indices = np.argsort(distances)
        
        closest_match_index = sorted_indices[0]
        second_closest_match_index = sorted_indices[1]
        
        closest_distance = distances[closest_match_index]
        second_closest_distance = distances[second_closest_match_index]

        if closest_distance < 0.8 * second_closest_distance:
            match = cv.DMatch(i, closest_match_index, closest_distance)
            matches.append(match)

    return matches

# Get the correct Warp and Transformation methods
def solver(type):

    transform = None
    warp = None

    if type == 3:
        transform = cv.getAffineTransform
        warp = cv.warpAffine
    else:
        transform = cv.getPerspectiveTransform
        warp = cv.warpPerspective

    return transform, warp

# RANSAC function
def RANSAC(iterations, kp1, kp2, matches, transform, type):

    inliers = -1
    best_transform = None
    threshold = 5       # Change if needed depndened on results

    for i in range(iterations):
        counter = 0

        random_matches = random.sample(matches, type)

        src_points = np.float32([kp1[random_matches[j].queryIdx].pt for j in range(type)])
        dst_points = np.float32([kp2[random_matches[j].trainIdx].pt for j in range(type)])

        temp_transform = transform(src_points, dst_points)

        for match in matches:
            match_src = kp1[match.queryIdx].pt
            match_dst = kp2[match.trainIdx].pt
            match_transformed = np.matmul(temp_transform, [match_src[0], match_src[1], 1])

            if type == 4 and match_transformed[2] != 0:
                match_transformed[0] = match_transformed[0] / match_transformed[2]
                match_transformed[1] = match_transformed[1] / match_transformed[2]

            residuals = np.sum(np.square(np.linalg.norm(match_transformed[:2] - match_dst)))

            if residuals < threshold:
                counter += 1

        if counter > inliers:
            inliers = counter
            best_transform = temp_transform

    return best_transform, inliers

# Check if we used all pieces
def check_puzzle(done, stop):

    if 0 not in [val for val in done.values()]:

        if -1 not in [val for val in done.values()]:
            return True, done, stop

    return False, done, stop

# Clear all the pieces that we didn't use in the last run
def clear_puzzle(done, stop):

    flag = True

    stop -= 1

    for key, val in done.items():
        if val == -1:
            flag = False
            done[key] = 0

    return flag, done, stop

# Get ratio of singular values of the transformation
def decompose_matrix(matrix):
    U, S, V = np.linalg.svd(matrix[:2, :2])

    ratio = S[0] / S[1]

    return ratio

# Main
if __name__ == "__main__":

    sift = cv.SIFT_create()

    covers = []
    keypoints = []
    descriptors = []
    images = []
    done = {}

    # Relative path to the directory for the results
    # Add folder for the files to be saved in
    result_file = './results/homography_9_results'

    num_of_pieces = sum(len(files) for _, _, files in os.walk(r'./puzzles/puzzle_homography_9/pieces'))

    # Build list of all images, their keypoints and descriptors
    for j in range(1, num_of_pieces):
        image = cv.imread('./puzzles/puzzle_homography_9/pieces/piece_' + str(j + 1) + '.jpg')

        images.append(image)

        done[j - 1] = 0

        covers.append(np.ones((image.shape[0], image.shape[1])))

        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        gray = cv.GaussianBlur(gray , (3,3) , 2)       # Gaussian blur helps with pictures that have been filtered

        kp, desc = SIFT(gray, sift)

        keypoints.append(kp)
        descriptors.append(desc)

    flag = False

    type = 4

    transform, warp = solver(type)

    size = (816, 490)

    cover = np.zeros(size[::-1])

    stop = 3

    # Warp the first piece of the puzzle into its place given in the 'transformation' matrix
    src = cv.imread('./puzzles/puzzle_homography_9/pieces/piece_1.jpg')
    
    transformation = np.loadtxt('./puzzles/puzzle_homography_9/warp_mat_1__H_490__W_816_.txt', dtype=float)
    
    src_cover = np.ones((src.shape[0], src.shape[1]))
    
    target = cv.warpPerspective(src, transformation, size, flags=2, borderMode=cv.BORDER_TRANSPARENT)

    cover += cv.warpPerspective(src_cover, transformation, size, flags=2, borderMode=cv.BORDER_TRANSPARENT)

    cv.imwrite(result_file + '/piece_1_relative.jpeg', target)

    used = 1

    while flag == False:

        flag, done, stop = check_puzzle(done, stop)

        if flag == True or stop == 0:
            break
        
        # Target is updated in every iteration, 
        # thus keypoints and descriptor need to be computed each time

        gray_target = cv.cvtColor(target, cv.COLOR_BGR2GRAY)

        gray_target = cv.GaussianBlur(gray_target, (3,3) , 2)

        target_kp, target_desc = SIFT(gray_target, sift)

        max_pic = -1
        max_matches = []

        # Find the image that matches our target the most
        for i in range(len(images)):

            if done[i] == 1 or done[i] == -1:
                continue

            distances = calculate_distance_matrix(descriptors[i], target_desc)
            matches = find_matches(distances, descriptors[i])

            if len(matches) > len(max_matches):
                max_pic = i
                max_matches = matches

        if len(max_matches) <= type:

            flag, done, stop = clear_puzzle(done, stop)

            if flag == True:
                break
            else:
                continue
        
        src = images[max_pic]

        temp_cover = covers[max_pic]

        ransac, inliers = RANSAC(1000, keypoints[max_pic], target_kp, max_matches, transform, type)

        # Determinant of the ransac transformation helps indicate whether the transformation is good or bad
        # In most cases a 0.1 < det < 8 is good
        det = np.linalg.det(ransac if type == 4 else np.vstack((ransac, [0,0,1])))

        # The singular value ratio assists in cases where determinant is good but transformation
        # Stretches the image a lot, a ratio < 25 is usually good
        svd_ratio = decompose_matrix(ransac)

        print("img = " + str(max_pic + 2) + ", matches = " + str(len(max_matches))+ ", inliers = " + str(inliers))
        print("det = "+ str(det) +",  svd = " + str(svd_ratio) +"\n")

        # Check the parameters to see if the transformation
        # is good or bad
        if det < 0.15 or det > 8 or svd_ratio > 30:
            done[max_pic] = -1
            continue

        # Warp the image into our target and add it in the pixels that are empty
        res = warp(src, ransac, size, flags=2, borderMode=cv.BORDER_TRANSPARENT)

        cv.imwrite(result_file + '/piece_'+ str(max_pic + 2) + '_relative.jpeg', res)

        mask = (cover == 0)
        target[mask] = res[mask]

        cover += warp(temp_cover, ransac, size, flags=2, borderMode=cv.BORDER_TRANSPARENT)

        done[max_pic] = 1

        used += 1

    # Plot the coverage count of the chosen pictures and save it
    plt.figure()
    plt.imshow(cover)
    plt.savefig(result_file + '/cover.jpeg')

    # Save final result
    cv.imwrite(result_file + '/solution_'+ str(used) + '_' + str(num_of_pieces) + '.jpeg', target)

