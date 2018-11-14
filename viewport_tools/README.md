# Inpainting360: Viewport tools


### Equirectangular to viewport script
Run the equirectangular2viewport script as follows:
```
python equirectangular2viewport.py --image test_image.jpg --fov 90 --yaw 180 --pitch 0 --height 2048 --width 2048
```
The resulting viewport image is saved into the project directory.


### Viewport to equirectangular script
Run the viewport2equirectangular script as follows:
```
python viewport2equirectangular.py --src test_image.jpg --viewport viewport.jpg --fov 90 --yaw 180 --pitch 0
```
The resulting equirectangular image is saved into the project directory.


### Drawing the Inpainting Mask script
Run the inpainting_gui script as follows:
```
python inpaint.py --image image_name.jpg --pen_width 15
```
With the left mouse button, draw the inpainting mask and click inpaint.
The resulting mask image is saved into the project directory.
