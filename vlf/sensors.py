import numpy as np

class SampleField:
    def __init__(self, image, r=3):

        pix = np.array(image.convert("L"))
        self.np_img = pix
        #Size of mask
        #Sample radius
        a, b = r-1, r-1
        n = r*2-1
        self.size_of_mask = n

        y,x = np.ogrid[-a:n-a, -b:n-b]
        mask = x*x + y*y <= r*r

        mask = x**2+y**2 <= 2**2
        #print(mask)
        self.mask = mask

    def get_mean_from_point(self, point):
        x, y = int(point[0]), int(point[1])
        half_size = self.size_of_mask // 2
        #print(x, y)
        slice_of_picture = self.np_img[y-half_size:y+half_size+1, x-half_size:x+half_size+1]
        try:
            result = slice_of_picture[self.mask].mean()
        except IndexError:
            # Out of bounds request, near edge, no line near edge
            # So, expecting 0
            result = 0
        return result

    def get_any_from_point(self, point):
        x, y = int(point[0]), int(point[1])
        half_size = self.size_of_mask // 2
        #print(x, y)
        slice_of_picture = self.np_img[y-half_size:y+half_size+1, x-half_size:x+half_size+1]
        try:
            result = slice_of_picture.sum()
        except IndexError:
            # Out of bounds request, near edge, no line near edge
            # So, expecting 0
            result = 0
        return result
