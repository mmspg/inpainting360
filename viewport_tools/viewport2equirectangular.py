# Copyright (C) 2018 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland
#     Multimedia Signal Processing Group
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Mehmet Tuzmen, master student
# Organisation: Multimedia Signal Processing Group (MMSPG), EPFL


import cv2
import numpy as np
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--src', default='', type=str,
                    help='The filename of the original equirectangular image')
parser.add_argument('--viewport', default='', type=str,
                    help='The filename of the viewport')
parser.add_argument('--fov', default=90, type=int,
                    help='The field of view in degrees')
parser.add_argument('--yaw', default=0, type=int,
                    help='The yaw angle of the viewport')
parser.add_argument('--pitch', default=0, type=int,
                    help='The pitch angle of the viewport')


class Perspective:
    def __init__(self, img_name, FOV, THETA, PHI, input_img):
        self._img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        [self._height, self._width, _] = self._img.shape
        self.wFOV = FOV
        self.THETA = THETA
        self.PHI = PHI
        self.hFOV = float(self._height) / self._width * FOV
        self.input_img = cv2.imread(input_img, cv2.IMREAD_COLOR)
        img = Image.open(input_img)
        self.height_full = img.height
        self.width_full = img.width
        self.w_len = np.tan(np.radians(self.wFOV / 2.0))
        self.h_len = np.tan(np.radians(self.hFOV / 2.0))

    def GetEquirectangular(self):
        #
        # THETA is left/right angle, PHI is up/down angle, both in degree
        #

        x, y = np.meshgrid(np.linspace(-180, 180, self.width_full), np.linspace(90, -90, self.height_full))

        x_map = np.cos(np.radians(x)) * np.cos(np.radians(y))
        y_map = np.sin(np.radians(x)) * np.cos(np.radians(y))
        z_map = np.sin(np.radians(y))

        xyz = np.stack((x_map, y_map, z_map), axis=2)

        y_axis = np.array([0.0, 1.0, 0.0], np.float32)
        z_axis = np.array([0.0, 0.0, 1.0], np.float32)
        [R1, _] = cv2.Rodrigues(z_axis * np.radians(self.THETA))
        [R2, _] = cv2.Rodrigues(np.dot(R1, y_axis) * np.radians(-self.PHI))

        R1 = np.linalg.inv(R1)
        R2 = np.linalg.inv(R2)

        xyz = xyz.reshape([self.height_full * self.width_full, 3]).T
        xyz = np.dot(R2, xyz)
        xyz = np.dot(R1, xyz).T

        xyz = xyz.reshape([self.height_full, self.width_full, 3])
        inverse_mask = np.where(xyz[:, :, 0] > 0, 1, 0)

        xyz[:, :] = xyz[:, :] / np.repeat(xyz[:, :, 0][:, :, np.newaxis], 3, axis=2)

        lon_map = np.where((-self.w_len < xyz[:, :, 1]) & (xyz[:, :, 1] < self.w_len) & (-self.h_len < xyz[:, :, 2]) & (
                    xyz[:, :, 2] < self.h_len), (xyz[:, :, 1] + self.w_len) / 2 / self.w_len * self._width, 0)
        lat_map = np.where((-self.w_len < xyz[:, :, 1]) & (xyz[:, :, 1] < self.w_len) & (-self.h_len < xyz[:, :, 2]) & (
                    xyz[:, :, 2] < self.h_len), (-xyz[:, :, 2] + self.h_len) / 2 / self.h_len * self._height, 0)
        mask = np.where((-self.w_len < xyz[:, :, 1]) & (xyz[:, :, 1] < self.w_len) & (-self.h_len < xyz[:, :, 2]) & (
                    xyz[:, :, 2] < self.h_len), 1, 0)

        persp = cv2.remap(self._img, lon_map.astype(np.float32), lat_map.astype(np.float32), cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_WRAP)
        mask = mask * inverse_mask
        mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
        persp = persp * mask
        self.input_img = np.where(mask == 0, self.input_img, 0)
        mask = np.where(mask == 0, 1, mask)
        merge_image = (np.divide(persp, mask))
        merge_image += self.input_img
        return merge_image


def viewport2equirectangular(src, viewport, fov, yaw, pitch):
    img = Perspective(viewport, fov, yaw, pitch, src).GetEquirectangular()
    cv2.imwrite('./equirectangular_out.jpg', img)


if __name__ == '__main__':
    args = parser.parse_args()
    viewport2equirectangular(args.src, args.viewport, args.fov, args.yaw, args.pitch)
