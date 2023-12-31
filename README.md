# ml_utils
My PyTorch/SKLearn utils

Some random util functions i have built. Will be slowly augmented with new stuff.

## visualize_loss.py
Visualizes loss as dot patterns ontop of a PyTorch dataloader batch. The point is to, for a cross-entropy classifier, identify items that stick out with high loss (i opted for loss over accuracy as the a classifier with more than two classes. Note that the output graph is sorted in order of low->high loss.

Example image from Daniel Bourke's dataset for FoodVision.
![image](https://github.com/cwestergren/ml_utils/assets/5159567/7cea6469-05a1-40e2-ae3b-ad5062f83504)
