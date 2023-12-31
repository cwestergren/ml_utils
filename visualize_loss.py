import torch
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import math

def visualize_losses(validation_dataloader, model, n):
    """
    Visualizes 'n' images from the PyTorch validation dataloader using the model to predict and compute losses. 
    Images are displayed in a grid with a dot pattern overlay. The color intensity of the dots represents 
    the loss associated with each image, ranging from green (low loss) to red (high loss). The losses are normalized
    from highest to lowest within the batch.

    Parameters:
    validation_dataloader (DataLoader): The dataloader containing the validation dataset.
    model (nn.Module): The trained PyTorch model used for predictions.
    n (int): The number of images to visualize.

    Returns:
    None: This function does not return anything but displays a matplotlib plot.

    Example usage:
    visualize_losses(validation_dataloader, model, n=8)

    Notes:
    See LICENSE file for BSD3 license information.
    The function assumes cuda cores available, and i did not move cols/lines parameters to function arguments as i was lazy.
    There are probably some bugs, i only pushed what i have used myself.
    """
  
    model = model.to('cuda')
    model.eval()  

    images, losses = [], []
    criterion = torch.nn.CrossEntropyLoss(reduction='none')  

    with torch.no_grad(): 
        for inputs, labels in validation_dataloader:
            inputs, labels = inputs.to('cuda'), labels.to('cuda')
            outputs = model(inputs.float())
            losses_per_item = criterion(outputs, labels) 
            
            for i in range(inputs.size(0)):
                if len(images) >= n:
                    break
                images.append(inputs[i].cpu())
                losses.append(losses_per_item[i].item())

            if len(images) >= n:
                break

    images_losses = list(zip(images, losses))
    images_losses.sort(key=lambda x: x[1]) 
    images, losses = zip(*images_losses)

    max_loss = max(losses)
    min_loss = min(losses)
    norm_losses = [(loss - min_loss) / (max_loss - min_loss) if max_loss > min_loss else 0 for loss in losses]

    cmap = mcolors.LinearSegmentedColormap.from_list("", ["green", "yellow", "red"])

    num_cols = 8
    num_rows = math.ceil(n / num_cols)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 3, num_rows * 3))
    axes = axes.flatten() 

    # Define a dot pattern 
    dot_spacing = 10  
    dot_radius = 2 

    for idx, (img, loss) in enumerate(zip(images, norm_losses)):
        # Normalize image for display
        img = img.permute(1, 2, 0).numpy()  # permute to plt shape (WHC from CWH)
        img = (img - img.min()) / (img.max() - img.min())

        color = cmap(loss)  

        axes[idx].imshow(img)

        for i in range(0, img.shape[0], dot_spacing):
            for j in range(0, img.shape[1], dot_spacing):
                circle = plt.Circle((j, i), dot_radius, color=color, alpha=0.7)
                axes[idx].add_patch(circle)

        axes[idx].axis('off') 

    for idx in range(len(images), num_rows * 4):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.show()
    model.train() 
