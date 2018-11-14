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
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--image', default='', type=str,
                    help='The filename of equirectangular image')
parser.add_argument('--fov', default=90, type=int,
                    help='The field of view in degrees')
parser.add_argument('--yaw', default=0, type=int,
                    help='The yaw angle of the viewport')
parser.add_argument('--pitch', default=0, type=int,
                    help='The pitch angle of the viewport')
parser.add_argument('--height', default=1024, type=int,
                    help='The height of the viewport')
parser.add_argument('--width', default=1024, type=int,
                    help='The width of the viewport')


class Equirectangular:
    def __init__(self, img_name):
        self._img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        [self._height, self._width, _] = self._img.shape
        print(self._img.shape)

    def GetViewport(self, FOV, THETA, PHI, height, width):
        #
        # THETA is left/right angle, PHI is up/down angle, both in degree
        #

        equ_h = self._height
        equ_w = self._width
        equ_cx = (equ_w - 1) / 2.0
        equ_cy = (equ_h - 1) / 2.0

        wFOV = FOV
        hFOV = float(height) / width * wFOV

        w_len = np.tan(np.radians(wFOV / 2.0))
        h_len = np.tan(np.radians(hFOV / 2.0))

        x_map = np.ones([height, width], np.float32)
        y_map = np.tile(np.linspace(-w_len, w_len, width), [height, 1])
        z_map = -np.tile(np.linspace(-h_len, h_len, height), [width, 1]).T

        D = np.sqrt(x_map ** 2 + y_map ** 2 + z_map ** 2)
        xyz = np.stack((x_map, y_map, z_map), axis=2) / np.repeat(D[:, :, np.newaxis], 3, axis=2)

        y_axis = np.array([0.0, 1.0, 0.0], np.float32)
        z_axis = np.array([0.0, 0.0, 1.0], np.float32)
        [R1, _] = cv2.Rodrigues(z_axis * np.radians(THETA))
        [R2, _] = cv2.Rodrigues(np.dot(R1, y_axis) * np.radians(-PHI))

        xyz = xyz.reshape([height * width, 3]).T
        xyz = np.dot(R1, xyz)
        xyz = np.dot(R2, xyz).T
        lat = np.arcsin(xyz[:, 2])
        lon = np.arctan2(xyz[:, 1], xyz[:, 0])

        lon = lon.reshape([height, width]) / np.pi * 180
        lat = -lat.reshape([height, width]) / np.pi * 180

        lon = lon / 180 * equ_cx + equ_cx
        lat = lat / 90 * equ_cy + equ_cy
        persp = cv2.remap(self._img, lon.astype(np.float32), lat.astype(np.float32), cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_WRAP)
        return persp


def extract_viewport(image, fov, yaw, pitch, height, width):
    img = Equirectangular(image).GetViewport(fov, yaw, pitch, height, width)
    cv2.imwrite('./viewport.jpg', img)


if __name__ == '__main__':
    args = parser.parse_args()
    extract_viewport(args.image, args.fov, args.yaw, args.pitch, args.height, args.width)