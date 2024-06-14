# INSTALLATION AND INSTRUCTIONS FOR USE
This captcha style classifier seeks to reduce bias in microfacies classifications of high resolution images of handsample and thin section samples. Classifications also generate training data for an ML 
classifier (Not yet coded). I have pulled methods from various packages and other independent sources cited in the code. The code is open source and free to use and modify with credit.

I should say I've basically copied this ReadMe from a tutorial by Dr. Nils C. Prieur (https://github.com/yellowchocobo). He writes cool geoscience code!

## Contents
1. [Installation](#Installation)
   1. [Installing with Conda](#Installing-with-Conda-Environment)
   2. [Installing without Conda](#Installing-without-Conda-(Requires-Jupyter-lab-with-python-3.9-or-later))
3. [Instructions For Use](#Instructions-For-Use)
   1. [Documentation of Relevant Classes](#Documentation-of-Relevant-Classes-Within-Project)
   2. [Documented Errors](#Documented-Errors)


## Installation <a name="Installation"></a>

### Installing with Conda Environment (Preferred) <a name="Installing-with-Conda-Environment"></a>

With conda installed, run the following code in terminal line by line (except the comments)

    # create environment geo with python version 3.9 installed on
    % conda create -n geo python=3.9
    
    # activate environment, you can now install the different packages in your newly created environment.
    % conda activate geo

    # installing opencv should be faster this way but it may take upwards of 10 mins
    % conda install --yes -c anaconda pillow
    % conda install --yes -c conda-forge opencv
    % conda install --yes -c conda-forge jupyterlab

    # first change directory to a place where you want to save all of your github repos
    % cd Desktop   # Or wherever else

    # Clone the repo to specified location
    % git clone https://github.com/ColteRodriguez/Microfacies-Capcha-style-Classifier.git
    
    # If you want to export this environment (if let's say you want to set it up on another computer)
    % conda env export > environment_geo.yml
    % conda env create -f environment_geo.yml # you can now create the same exact environment from the file

    # Open the code
    % cd project_home
    % jupyter lab # Opens the project in jupyter lab for browser and you can start running code!
    
### Installing without Conda (Requires Jupyter lab with python 3.9 or later) <a name="Installing-without-Conda-(Requires-Jupyter-lab-with-python-3.9-or-later)"></a>

<p>
1. Download the project zip (clicking on the green code button in the upper right corner)
2. Open the zip and move project_home to wherever you want it. (I like it in desktop for convenience)
3. Install necesary packages in terminal These should be the only ones you need to install from terminal. 
  All the others can be pip installed in a jupyter lab code chunk as needed:

    cd Desktop  # Or wherever you moved project_home
    pip install pillow
    pip install opencv-python   # This will take ages

    # Now you can just open project_home in Jupyter lab and navigate to the code!

## Instructions For Use <a name="Instructions-For-Use"></a>


### Documentation of Relevant Classes Within Project <a name="Documentation-of-Relevant-Classes-Within-Project"></a>

### Bulk Documentation: Further Comments on Public Methods 
1. [grab_random_image()](#A)
2. [create_subdirectories()](#B)
3. [recursive_subdivide()](#C)
4. [find_children()](#D)
5. [extract_subarray()](#E)
   
#### grab_random_image(folder_path = String) <a name="A"></a>

- **Returns:**
   A full file path to an image in Sample_Images as a string

- **Affects:**
   Writes the file name to FS_helper.txt in order to make draws exclusive and keep track of segmented images

- **Inherits**:
   Functionality from os for directory navigation and text file manipulation
  
- **Errors**:
  'FileNotFoundError' || Occurs when an invalid or incomplete path is passed
  No or non-image return || Occurs when the Sample Images folder is not passed as an argument
  
#### create_subdirectories(path = String) <a name="B"></a>

- **Returns:**
   None

- **Affects:**
   Creates subdirectories to store image segments and classifications at the specified path (preferably an external drive path)

- **Inherits**:
   Functionality from os for directory navigation console text coloring from Fore for warning message

- **Errors**:
   'FileNotFoundError' || Occurs when an invalid or incomplete path is passed
  
  #### recursive_subdivide(node = Node, k = int, minPixelSize = int, img = String) <a name="C"></a>

- **Returns:**
   None

- **Affects:**
   Divides Image into quadrants (Nodes -- (see class Node)) to store in a Qtree

- **Inherits**:
   Functionality from math. This method is globally acessible but technically useless outside of the scope of class QTree as an instance method

#### find_children(node = Node): <a name="D"></a>

- **Returns:**
   An array of Node objects

- **Affects:**
   None

- **Inherits**:
   None. This method is globally acessible but technically useless outside of the scope of class QTree as an instance method

#### extract_subarray(array = int[][], start_row = int, start_col = int, height = int, width = int): <a name="E"></a>

- **Returns:**
   A 2d array of indices which are a subset of the argument array and defined by the row, col, height, and width arguments

- **Affects:**
   None

- **Inherits**:
   None. This method may be interchanged with extract subarray from the opencv module.

#### extract_subarray(array = int[][], start_row = int, start_col = int, height = int, width = int): <a name="E"></a>

- **Returns:**
   A 2d array of indices which are a subset of the argument array and defined by the row, col, height, and width arguments

- **Affects:**
   None

- **Inherits**:
   None. This method may be interchanged with extract subarray from the opencv module.


### Documented Errors <a name="Documented-Errors"></a>


    

    
    

    
