import numpy as np

from lenstronomy.Data.pixel_grid import PixelGrid

__all__ = ['KinBin']

class KinBin(object):
    """
    Class that summarizes the binned kinematic data.

    The KinBin() class is initialized with :
     - The information about the bins (bin positions, bin value, and bin signal-to-noise): bin_pos_ra, bin_pos_dec,
    bin_data, bin_SNR.
     - The information about the associated intial shape of the unbinned kinematic map: bin_mask gives the index of
    corresponding bin for each pixel), and ra_at_xy_0,dec_at_xy_0,transform_pix2angle,ra_shift,dec_shift are the usual
    PixelGrid characteritics.

    """

    def __init__(self, bin_pos_ra, bin_pos_dec, bin_data, bin_SNR, bin_mask, ra_at_xy_0=0, dec_at_xy_0=0,
                 transform_pix2angle=None, ra_shift=0, dec_shift=0):

        """
        :param bin_pos_ra: list, weighted ra center of each bin, ordered by bin index.
        :param bin_pos_dec: list, weighted dec center of each bin, ordered by bin index.
        :param bin_data: list, kinematic value of each bin, ordered by bin index.
        :param bin_SNR: list, signal-to-noise ratio associated to each bin, ordered by bin index.
        :param bin_mask: 2D array, mapping from the unbinned image to the binned one, each pixel value is the
         corresponding bin index.
        :param ra_at_xy_0: float, ra coordinate at pixel (0,0) (unbinned image)
        :param dec_at_xy_0: float, dec coordinate at pixel (0,0) (unbinned image)
        :param transform_pix2angle: 2x2 array, mapping of pixel (unbinned image) to coordinate
        :param ra_shift:  float, RA shift of pixel grid
        :param dec_shift: float, DEC shift of pixel grid

        """

        nx, ny = np.shape(bin_mask)
        self._nx = nx
        self._ny = ny
        if transform_pix2angle is None:
            transform_pix2angle = np.array([[1, 0], [0, 1]])

        self.PixelGrid =   PixelGrid(nx, ny, transform_pix2angle, ra_at_xy_0 + ra_shift, dec_at_xy_0 + dec_shift)

        self._x = bin_pos_ra
        self._y = bin_pos_dec
        self._data = bin_data
        self._snr = bin_SNR

        self._bin_mask = bin_mask

    def noise(self):
        """
        Calculate the sigma (noise) associated to each bin, using the signal and the signal-to-noise ratio.
        """
        self._noise = self._data/self._snr
        return self._noise
    def binned_image(self):
        """
        Creates the binned image of the kinemmatic
        """
        binned_image = np.zeros_like(bin_mask)
        for idx, value in enumerate(bin_data):
            binned_image[bin_mask==idx] = value
        return binned_image
