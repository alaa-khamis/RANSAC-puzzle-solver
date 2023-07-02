# RANSAC based puzzle solver

- By: <a href="https://alaa-khamis.github.io/">Alaa Khamis</a>

### Algorithm Overview

We employed a RANSAC-based algorithm to solve the puzzles. The algorithm functions as follows:

1. Data Pre-processing: All puzzle pieces, barring the first, are stored as a list of NumPy 2D arrays. Key points and descriptors for each image are computed using SIFT detection, while the first piece is warped to its correct position based on the given matrix.

2. Find Next Image: From the currently positioned pieces, the algorithm identifies the next unused image with the highest match count.

3. RANSAC Approximation: An iterative RANSAC process approximates the image transformation.

3. Transformation Acceptance/Denial: The algorithm checks transformation parameters to either accept or deny the transformation. If accepted, the image is warped and marked as done. If denied, the image is marked as not done and looped over again.

4. Loop Termination Check: The loop continues until all images with a match count exceeding a threshold (3 for affine and 4 for homography transformations) have been processed, or a pre-set retry count is depleted.

5. Result Storage: On loop termination, the coverage count and result are saved.

### Parameter Selection

Selection of transformation parameters hinged on several criteria:

1. Ratio Test
2. Residuals Threshold
3. Determinant
4. Singular Value Ratio of the SVD Decomposition of the Transformation Matrix.

In most scenarios, the default values (Ratio Test = 0.8, Residuals Threshold = 5, 0.1 < Determinant < 7 and SVD < 25) provided satisfactory results for puzzles 1-8 (both affine and homography). However, puzzles 9-10 necessitated adjustments:

Affine 9: Elevating the ratio value to 0.85 enabled more matches.
Affine 10 and Homography 9-10: Application of blur to the grayscaled image prior to SIFT key-point extraction and description vector generation improved match-finding, even for color-filtered images. The determinant and SVD bounds were also adjusted as per puzzle requirements.
Please note that these parameters were selected considering all puzzle pieces in general, not for individual images.


## Puzzle Examples:

### 1. Affine Puzzle #6

#### Original Pieces:
| Piece 1 | Piece 2 | Piece 3 | Piece 4 | Piece 5 |
|---------|---------|---------|---------|---------|
| ![Piece 1 Description](/puzzles/puzzle_affine_6/pieces/piece_1.jpg) | ![Piece 2 Description](/puzzles/puzzle_affine_6/pieces/piece_2.jpg) | ![Piece 3 Description](/puzzles/puzzle_affine_6/pieces/piece_3.jpg) | ![Piece 4 Description](/puzzles/puzzle_affine_6/pieces/piece_4.jpg) | ![Piece 5 Description](/puzzles/puzzle_affine_6/pieces/piece_5.jpg) |
| Piece 6 | Piece 7 | Piece 8 | Piece 9 | Piece 10 |
| ![Piece 6 Description](/puzzles/puzzle_affine_6/pieces/piece_6.jpg) | ![Piece 7 Description](/puzzles/puzzle_affine_6/pieces/piece_7.jpg) | ![Piece 8 Description](/puzzles/puzzle_affine_6/pieces/piece_8.jpg) | ![Piece 9 Description](/puzzles/puzzle_affine_6/pieces/piece_9.jpg) | ![Piece 10 Description](/puzzles/puzzle_affine_6/pieces/piece_10.jpg) |
| Piece 11 | Piece 12 | Piece 13 | Piece 14 | Piece 15 |
| ![Piece 11 Description](/puzzles/puzzle_affine_6/pieces/piece_11.jpg) | ![Piece 12 Description](/puzzles/puzzle_affine_6/pieces/piece_12.jpg) | ![Piece 13 Description](/puzzles/puzzle_affine_6/pieces/piece_13.jpg) | ![Piece 14 Description](/puzzles/puzzle_affine_6/pieces/piece_14.jpg) | ![Piece 15 Description](/puzzles/puzzle_affine_6/pieces/piece_15.jpg) |
| Piece 16 | Piece 17 | Piece 18 | Piece 19 | Piece 20 |
| ![Piece 16 Description](/puzzles/puzzle_affine_6/pieces/piece_16.jpg) | ![Piece 17 Description](/puzzles/puzzle_affine_6/pieces/piece_17.jpg) | ![Piece 18 Description](/puzzles/puzzle_affine_6/pieces/piece_18.jpg) | ![Piece 19 Description](/puzzles/puzzle_affine_6/pieces/piece_19.jpg) | ![Piece 20 Description](/puzzles/puzzle_affine_6/pieces/piece_20.jpg) |
| Piece 21 | Piece 22 | Piece 23 | Piece 24 | Piece 25 |
| ![Piece 21 Description](/puzzles/puzzle_affine_6/pieces/piece_21.jpg) | ![Piece 22 Description](/puzzles/puzzle_affine_6/pieces/piece_22.jpg) | ![Piece 23 Description](/puzzles/puzzle_affine_6/pieces/piece_23.jpg) | ![Piece 24 Description](/puzzles/puzzle_affine_6/pieces/piece_24.jpg) | ![Piece 25 Description](/puzzles/puzzle_affine_6/pieces/piece_25.jpg) |


#### Solution:

| Piece 1 | Piece 2 | Piece 3 | Piece 4 | Piece 5 |
|---------|---------|---------|---------|---------|
| ![Piece 1 Description](/results/affine_6_results/piece_1_relative.jpeg) | ![Piece 2 Description](/results/affine_6_results/piece_2_relative.jpeg) | ![Piece 3 Description](/results/affine_6_results/piece_3_relative.jpeg) | ![Piece 4 Description](/results/affine_6_results/piece_4_relative.jpeg) | ![Piece 5 Description](/results/affine_6_results/piece_5_relative.jpeg) |
| Piece 6 | Piece 7 | Piece 8 | Piece 9 | Piece 10 |
| ![Piece 6 Description](/results/affine_6_results/piece_6_relative.jpeg) | ![Piece 7 Description](/results/affine_6_results/piece_7_relative.jpeg) | ![Piece 8 Description](/results/affine_6_results/piece_8_relative.jpeg) | ![Piece 9 Description](/results/affine_6_results/piece_9_relative.jpeg) | ![Piece 10 Description](/results/affine_6_results/piece_10_relative.jpeg) |
| Piece 11 | Piece 12 | Piece 13 | Piece 14 | Piece 15 |
| ![Piece 11 Description](/results/affine_6_results/piece_11_relative.jpeg) | ![Piece 12 Description](/results/affine_6_results/piece_12_relative.jpeg) | ![Piece 13 Description](/results/affine_6_results/piece_13_relative.jpeg) | ![Piece 14 Description](/results/affine_6_results/piece_14_relative.jpeg) | ![Piece 15 Description](/results/affine_6_results/piece_15_relative.jpeg) |
| Piece 16 | Piece 17 | Piece 18 | Piece 19 | Piece 20 |
| ![Piece 16 Description](/results/affine_6_results/piece_16_relative.jpeg) | ![Piece 17 Description](/results/affine_6_results/piece_17_relative.jpeg) | ![Piece 18 Description](/results/affine_6_results/piece_18_relative.jpeg) | ![Piece 19 Description](/results/affine_6_results/piece_19_relative.jpeg) | ![Piece 20 Description](/results/affine_6_results/piece_20_relative.jpeg) |
| Piece 21 | Piece 22 | Piece 23 | Piece 24 | Piece 25 |
| ![Piece 21 Description](/results/affine_6_results/piece_21_relative.jpeg) | ![Piece 22 Description](/results/affine_6_results/piece_22_relative.jpeg) | ![Piece 23 Description](/results/affine_6_results/piece_23_relative.jpeg) | ![Piece 24 Description](/results/affine_6_results/piece_24_relative.jpeg) | ![Piece 25 Description](/results/affine_6_results/piece_25_relative.jpeg) |

### Final Output:

![Solution](/results/affine_6_results/solution_25_25.jpeg)

#### Pieces Cover:
![Cover](/results/affine_6_results/cover.jpeg)

---

### 2. Homography Puzzle #5

#### Original Pieces:

| Piece 1 | Piece 2 | Piece 3 | Piece 4 |
|---------|---------|---------|---------|
| ![Piece 1 Description](/puzzles/puzzle_homography_5/pieces/piece_1.jpg) | ![Piece 2 Description](/puzzles/puzzle_homography_5/pieces/piece_2.jpg) | ![Piece 3 Description](/puzzles/puzzle_homography_5/pieces/piece_3.jpg) | ![Piece 4 Description](/puzzles/puzzle_homography_5/pieces/piece_4.jpg) |
| Piece 5 | Piece 6 | Piece 7 | Piece 8 |
| ![Piece 5 Description](/puzzles/puzzle_homography_5/pieces/piece_5.jpg) | ![Piece 6 Description](/puzzles/puzzle_homography_5/pieces/piece_6.jpg) | ![Piece 7 Description](/puzzles/puzzle_homography_5/pieces/piece_7.jpg) | ![Piece 8 Description](/puzzles/puzzle_homography_5/pieces/piece_8.jpg) |
| Piece 9 | Piece 10 | Piece 11 | Piece 12 |
| ![Piece 9 Description](/puzzles/puzzle_homography_5/pieces/piece_9.jpg) | ![Piece 10 Description](/puzzles/puzzle_homography_5/pieces/piece_10.jpg) | ![Piece 11 Description](/puzzles/puzzle_homography_5/pieces/piece_11.jpg) | ![Piece 12 Description](/puzzles/puzzle_homography_5/pieces/piece_12.jpg) |
| Piece 13 | Piece 14 | Piece 15 | Piece 16 |
| ![Piece 13 Description](/puzzles/puzzle_homography_5/pieces/piece_13.jpg) | ![Piece 14 Description](/puzzles/puzzle_homography_5/pieces/piece_14.jpg) | ![Piece 15 Description](/puzzles/puzzle_homography_5/pieces/piece_15.jpg) | ![Piece 16 Description](/puzzles/puzzle_homography_5/pieces/piece_16.jpg) |


#### Solution:

| Piece 1 | Piece 2 | Piece 3 | Piece 4 |
|---------|---------|---------|---------|
| ![Piece 1 Description](/results/homography_5_results/piece_1_relative.jpeg) | ![Piece 2 Description](/results/homography_5_results/piece_2_relative.jpeg) | ![Piece 3 Description](/results/homography_5_results/piece_3_relative.jpeg) | ![Piece 4 Description](/results/homography_5_results/piece_4_relative.jpeg) |
| Piece 5 | Piece 6 | Piece 7 | Piece 8 |
| ![Piece 5 Description](/results/homography_5_results/piece_5_relative.jpeg) | ![Piece 6 Description](/results/homography_5_results/piece_6_relative.jpeg) | ![Piece 7 Description](/results/homography_5_results/piece_7_relative.jpeg) | ![Piece 8 Description](/results/homography_5_results/piece_8_relative.jpeg) |
| Piece 9 | Piece 10 | Piece 11 | Piece 12 |
| ![Piece 9 Description](/results/homography_5_results/piece_9_relative.jpeg) | ![Piece 10 Description](/results/homography_5_results/piece_10_relative.jpeg) | ![Piece 11 Description](/results/homography_5_results/piece_11_relative.jpeg) | ![Piece 12 Description](/results/homography_5_results/piece_12_relative.jpeg) |
| Piece 13 | Piece 14 | Piece 15 | Piece 16 |
| ![Piece 13 Description](/results/homography_5_results/piece_13_relative.jpeg) | ![Piece 14 Description](/results/homography_5_results/piece_14_relative.jpeg) | ![Piece 15 Description](/results/homography_5_results/piece_15_relative.jpeg) | ![Piece 16 Description](/results/homography_5_results/piece_16_relative.jpeg) |

### Final Output:

![Solution](/results/homography_5_results/solution_16_16.jpeg)

#### Pieces Cover:
![Cover](/results/homography_5_results/cover.jpeg)