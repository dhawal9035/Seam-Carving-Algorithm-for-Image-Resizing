from pylab import *
from skimage import img_as_float
from skimage import filters
import numpy
import matplotlib.pyplot


def dual_gradient_energy(img):
    h, w = img.shape[:2]
    img = img_as_float(img)
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    rh_gradient = filters.sobel_h(R)
    gh_gradient = filters.sobel_h(G)
    bh_gradient = filters.sobel_h(B)
    rv_gradient = filters.sobel_v(R)
    gv_gradient = filters.sobel_v(G)
    bv_gradient = filters.sobel_v(B)

# Calculating the energy Matrix

    energy = (rh_gradient*rh_gradient) + (gh_gradient*gh_gradient) +\
             (bh_gradient*bh_gradient) + (rv_gradient*rv_gradient) +\
             (gv_gradient*gv_gradient) + (bv_gradient*bv_gradient)

# Copying the second column to first and second last column to last
# as first and last column return 0 due to sobel
    for i in range(h):
        for j in range(w):
            if j == 0:
                energy[i][j] = energy[i][j+1]
            if j == w-1:
                energy[i][j] = energy[i][j-1]
    return energy


def find_min_energy(img):
    h, w = img.shape[:2]
    energy = dual_gradient_energy(img)
    min_energy = numpy.zeros((h, w))
# Finding the minimum energy using a bottom up approach
    for i in range(h-2, -1, -1):
        for j in range(0, w):
            if j == 0:
                min_energy[i][j] =\
                    min(energy[i][j]+energy[i+1][j],
                        energy[i][j]+energy[i+1][j+1])
            elif j == w-1:
                min_energy[i][j] = \
                    min(energy[i][j]+energy[i+1][j],
                        energy[i][j]+energy[i+1][j-1])
            else:
                min_energy[i][j] = \
                    min(energy[i][j]+energy[i+1][j],
                        energy[i][j]+energy[i+1][j+1],
                        energy[i][j]+energy[i+1][j-1])
    return min_energy


def find_seam(img):
    h, w = img.shape[:2]
    min_energy = find_min_energy(img)
    seam = [0]
# Finding the minimum value in the first row of the matrix to backtrack
    minimum = min_energy[0][0]
    for i in range(0, w):
        if minimum > min_energy[0][i]:
            minimum = min_energy[0][i]
            seam[0] = i
# Calling the compute_seam function to calculate the seam
    seam = compute_seam(img, seam, minimum, min_energy)
    return seam


def compute_seam(img, seam, minimum, min_energy):
    h, w = img.shape[:2]
#    Backtracking the Minimum Energy matrix to find the
#    seam using a top down approach
    for i in range(1, h):
        if seam[i-1] == 0:
            if min_energy[i][seam[i-1]] > min_energy[i][seam[i-1]+1]:
                seam.append(seam[i-1]+1)
            else:
                seam.append(seam[i-1])
        elif seam[i-1] == w-1:
            if min_energy[i][seam[i-1]-1] > min_energy[i][seam[i-1]]:
                seam.append(seam[i-1])
            else:
                seam.append(seam[i-1]-1)
        else:
            if min_energy[i][seam[i-1]-1] < min_energy[i][seam[i-1]]\
                    and min_energy[i][seam[i-1]-1] < min_energy[i][seam[i-1]+1]:
                seam.append(seam[i-1]-1)
            elif min_energy[i][seam[i-1]-1] == min_energy[i][seam[i-1]]\
                    and min_energy[i][seam[i-1]-1] == min_energy[i][seam[i-1]+1]:
                seam.append(seam[i-1])
            elif min_energy[i][seam[i-1]] < min_energy[i][seam[i-1]-1]\
                    and min_energy[i][seam[i-1]] < min_energy[i][seam[i-1]+1]:
                seam.append(seam[i-1])
            else:
                seam.append(seam[i-1]+1)
    return seam


def plot_seam(img, seam):
    # orig_img = imread('D:\img\HJoceanSmall.png')
    orig_img = imread('D:\img\Facebook.jpg')
    orig_img = img_as_float(orig_img)
    energy = dual_gradient_energy(img)
    # orig_energy = dual_gradient_energy(orig_img)
    h, w = img.shape[:2]
    min_y = range(0, h)
    # subplot(1, 2, 1); imshow(orig_energy); title("Energy of Original Image")
    # subplot(1, 2, 2); imshow(energy); title("Energy of Image after seam removal")
    subplot(1, 2, 1); imshow(orig_img); title("Original Image")
    subplot(1, 2, 2); imshow(img); title("Image after seam removal")
    show()
    gray()
    imshow(energy)
    matplotlib.pyplot.scatter(seam, min_y, color="red")
    matplotlib.pyplot.show()


def remove_seam(img, seam):
    img = img_as_float(img)
    h, w, k = img.shape
    new_energy = numpy.zeros((h, w-1, k))
    flag = False

# Logic for removing the seam
    for i in range(h-1):
        for j in range(w):
            if j == seam[i]:
                flag = True
            else:
                if flag:
                    new_energy[i][j-1] = img[i][j]
                else:
                    new_energy[i][j] = img[i][j]
        flag = False
    return new_energy


def main():
    # img = imread('D:\img\HJoceanSmall.png')
    # img = imread('D:\img\City.jpg')
    img = imread('D:\img\Facebook.jpg')
    h, w = img.shape[:2]
    print h
    print w

    for i in range(20):
        dual_gradient_energy(img)
        find_min_energy(img)
        seam = find_seam(img)
        img = remove_seam(img, seam)

    plot_seam(img, seam)
if __name__ == '__main__':
    main()
