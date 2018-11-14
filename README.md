# Inpainting360
Applying inpainting to omnidirectional images


![Inpainting360diagram.png](docs/figures/Inpainting360diagram.png)
Viewport extraction method for object removal using inpainting


### Results of subjective quality evaluation

![Mos.png](docs/figures/Mos.png)
Mean opinion scores with 95% confidence intervals


### Third-party software used

| Abbreviation | Base algorithm name                                 | Viewport | Source code                                                                        |
| :----------- | :-------------------------------------------------- | :------- | :--------------------------------------------------------------------------------- |
| CSH          | Coherency sensitive hashing                         | No       | <span>http://github.com/PetterS/patch-inpainting \[Commit: 03cc575\]</span>        |
| CSH360       | Coherency sensitive hashing                         | Yes      | \- -                                                                               |
| Criminisi    | Exemplar-Based Image Inpainting                     | No       | <span>http://github.com/cheind/inpaint \[Commit: 864128c\]</span>                  |
| Criminisi360 | Exemplar-Based Image Inpainting                     | Yes      | \- -                                                                               |
| GIIwCA       | Generative Image Inpainting w/ Contextual Attention | No       | <span>http://github.com/JiahuiYu/generative_inpainting \[Commit: 6bfaa20\]</span> |
| GIIwCA360    | Generative Image Inpainting w/ Contextual Attention | Yes      | \- -                                                                               |
