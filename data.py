"""Reads FeTA data and organizes it for use.
"""
import os
import csv

import torch
import nibabel as nib

# Global variable for data path
data_path = "/home/mriva/Recherche/feta_2.0"

class FetaDataset(torch.utils.data.Dataset):
    def __init__(self, data_path, transform = None, target_transform = None):
        self.data_path = data_path

        # Transforms to be applied to the data and to the labels
        self.transform = transform
        self.target_transform = target_transform
        # we have 80 subjects and 7 classes+bg
        self.size = 80
        self.num_classes = 8
        # Storing gestational ages
        with open(os.path.join(self.data_path,"participants.tsv")) as f:
            read_tsv = csv.reader(f, delimiter="\t")
            # Skip header
            next(read_tsv)
            gas = [float(line[2]) for line in read_tsv]
        self.gestational_ages = gas

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        """Loads an item from the dataset and corresponding labelmap and GA"""
        # Preparing data item path
        item_path = "sub-{:>03}".format(index + 1)

        # Loading niftis
        image = nib.load(os.path.join(self.data_path, item_path, "anat","sub-{:>03}_rec-mial_T2w.nii.gz".format(index+1))).get_fdata()
        labelmap = nib.load(os.path.join(self.data_path, item_path, "anat","sub-{:>03}_rec-mial_dseg.nii.gz".format(index+1))).get_fdata()

        # Applying transforms
        image, labelmap = self.apply_transforms(image, labelmap)
        return image, labelmap, self.gestational_ages[index]

    def apply_transforms(self, image, labelmap):
        if self.transform is not None:
            image = self.transform(image)
        if self.target_transform is not None:
            labelmap = self.target_transform(labelmap)
        return image, labelmap

if __name__ == '__main__':
    set = FetaDataset(data_path)
    print(set[0])
    import matplotlib.pyplot as plt
    plt.imshow(set[0][0][128],cmap="gray")
    plt.show()
    plt.imshow(set[0][1][128])
    plt.show()
