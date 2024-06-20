from SheetAPI import locate_sample, get_cell, change_cell, update_percent
import MainWindow as MW


from PIL import Image, ImageOps, ImageTk                # For image manipulation when cv has problems
from pathlib import Path                                # for file manipulation
import shutil                                           # For moving files
import cv2                                              # For image manipulation when PIL has problems
import tkinter as tk                                    # GUI module
from tkinter import Tk, ttk, Button, Label, filedialog, Toplevel
import MainWindow
from colorama import Fore
import random
import os

home = str(Path(os.getcwd()).parent.parent)

############## Image Manipulation #################
def open_secondary_window(frame, filename):
    # Create a new window
    # secondary_window = tk.Frame(root)
    # secondary_window.pack()  # Position the frame within the main window
    # secondary_window = Toplevel(root)
    # secondary_window.geometry('400x400')
    app = MW.MainWindow(frame, path=filename)
    app.mainloop()
    
def find_and_outline_segment(large_image_path, small_image_path, outline_width):
    # Load images
    large_image = cv2.imread(large_image_path)
    small_image = cv2.imread(small_image_path)

    # Convert images to grayscale
    large_image_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    small_image_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    # Template matching
    result = cv2.matchTemplate(large_image_gray, small_image_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get the coordinates of the matched region
    top_left = max_loc
    h, w = small_image_gray.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Draw black outline around the matched region
    cv2.rectangle(large_image, top_left, bottom_right, (0, 0, 0), thickness=outline_width)

    return large_image, small_image

def display_images():
    global image_paths, recent, label_large, label_small, directory, large_image_area, images_frame
    
    
    # Choose a random image from the unlabeled directory
    if len(image_paths) == 0:
        root.destroy()
        print(Fore.GREEN + f"All images in {directory} have been classified!")
        return
        
    random_image = random.choice(image_paths)
    recent = random_image
    
    # Must redefine large image
    large_image = str(home_data + "/Sample_Images/" + random_image[random_image.index('Img'):random_image.index('Img') + 7] + ".tif")
    large_image_area = cv2.imread(large_image).shape[0] * cv2.imread(large_image).shape[1]
    
    # Find and outline the segment in the large image
    outlined_large_image, small_image = find_and_outline_segment(large_image, random_image, outline_width=5)
    
    # Convert images from BGR to RGB (for displaying with PIL)
    large_image_rgb = cv2.cvtColor(outlined_large_image, cv2.COLOR_BGR2RGB)
    small_image_rgb = cv2.cvtColor(small_image, cv2.COLOR_BGR2RGB)

    # Convert images to PIL format
    large_image_pil = Image.fromarray(large_image_rgb)
    image_copy = large_image_pil
    small_image_pil = Image.fromarray(small_image_rgb)
    
    # Convert PIL images to ImageTk format
    small_image_tk = ImageTk.PhotoImage(small_image_pil)

    images_frame = tk.Frame(root)
    images_frame.pack(side = tk.BOTTOM)
    
    # If the labels don't exist, make new ones; if they do, reconfigure them
    if label_large is None:
        label_large = tk.Frame(images_frame)
        label_large.config(width=400,height=400)
        label_large.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        label_small = tk.Label(images_frame, image=small_image_tk)
        label_small.image = small_image_tk
        label_small.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    else:
        for widget in label_large.winfo_children():
            widget.destroy()
        
        label_small.config(image=small_image_tk)
        label_small.image = small_image_tk  # Keep a reference to avoid garbage collection
    
    # Open the secondary window inside label_large
    # NOTE: The Zoom functionality is computationally expensive and may run slow
    # (or not at all) on slower computers. Consider previous versions
    open_secondary_window(label_large, image_copy)
    
############ Buttons and app functionality ######################
def update_spreadsheet(features, alteration_score, constituent):
    global recent, spreadsheet_path, large_image_area
    
    # 1. Get the segment area
    cvImga = cv2.imread(recent)
    area = cvImga.shape[0] * cvImga.shape[1]
    
    
    # 2. Get the image name for spreadsheet navigtion
    name_query = recent[recent.index('Img'):recent.index('Img') + 7]
    
    # 2.1. Query for the correct row of the sample
    sample_row = locate_sample(spreadsheet_path, name_query, sheet_num = 0)[0]
    
    # 2.2. Save a copy of the total area
    total_area_col = locate_sample(spreadsheet_path, 'Total_mapped_area', sheet_num = 0)[1]
    current_total_area = get_cell(sample_row, total_area_col, spreadsheet_path, sheet_num = 0)
    
    # Change the total area and update percent mapped
    change_cell(sample_row, total_area_col, spreadsheet_path, int(current_total_area) + int(area), sheet_num = 0)
    percent_mapped = (current_total_area + area)/large_image_area
    change_cell(sample_row, locate_sample(spreadsheet_path, '%Mapped', sheet_num = 0)[1], spreadsheet_path, percent_mapped, sheet_num = 0)
    
    # 3. Update the Constituent percentage distrib
    for classif in classifications_order:
        rating = None
        isSubject = False
        # Dont want to update this col!
        if classif == 'Total_mapped_area':
            continue
        # Update params
        if classif == constituent:
            isSubject = True
        r, c = sample_row, locate_sample(spreadsheet_path, classif, sheet_num = 0)[1]
        old_value = get_cell(r, c, spreadsheet_path, sheet_num = 0)
        new_value = update_percent(old_value, current_total_area, area, rating, isSubject)
        change_cell(r, c, spreadsheet_path, new_value, sheet_num = 0)
    
    # 5. Update the Alteration Score
    r, c = sample_row, locate_sample(spreadsheet_path, 'Alteration', sheet_num = 0)[1]
    old_value = get_cell(r, c, spreadsheet_path, sheet_num = 0)
    new_value = update_percent(old_value, current_total_area, area, rating = alteration_score, isSubject = False)
    change_cell(r, c, spreadsheet_path, new_value, sheet_num = 0)
    
    # Update the features percents: The features are technically already the incices of the cols :)
    for feature in features:
        r, c = sample_row, locate_sample(spreadsheet_path, feature, sheet_num = 1)[1]
        old_value = get_cell(r, c, spreadsheet_path, sheet_num = 1)
        change_cell(r, c, spreadsheet_path, update_percent(old_value, current_total_area, area, rating = None, isSubject = True), sheet_num = 1)
    
def classify():
    global image_paths, image, recent, classif
    
    # Move the file to the respective classification
    source_path = recent
    destination_path = home_data + '/Training_data/All_data/' + classif
    shutil.move(source_path, destination_path)

# Destroy previous labels. Needs function call stack to subvert mainloop resetting labels before branch
def clear_labels():
    global label_large, label_small
    label_large.config(image=None)
    label_large.image = None  # Keep a reference to avoid garbage collection
        
    label_small.config(image=None)
    label_small.image = None  # Keep a reference to avoid garbage collection
    
# Function to select a directory
def select_directory():
    global image_paths, large_image, label_large, label_small, directory, secondary_window, images_frame
    
    # Reset the image viewer if a new directory is selected
    if label_large is not None:
        # TK has built in delays which makes visuals hard
        for widget, widgit2 in zip(label_large.winfo_children(), label_small.winfo_children()):
            widget.destroy()
            widget2.destroy()
        images_frame.pack_forget()
        images_frame.destroy()
    
    directory = filedialog.askdirectory()
    if directory:
        image_paths = [os.path.join(directory, f) for f in os.listdir(directory)
                       if os.path.isfile(os.path.join(directory, f)) and
                       f.lower().endswith((".png", ".jpg", ".jpeg"))]
        label_large = None
        label_small = None
        display_images()

    
# Global variable to store the rating
def update_classif(value):
    global classif
    classif = value
    
def update_rating(value):
    global rating
    rating = value

def submit_action():
    global rating, classif
    if classif == 'Non-Sample':
        classify()
        display_images()
        classif, rating = None, None
        return
    # Corner case if form is uncomplete
    if rating == None or classif == None:
        return
    # Get features from the checkboxes
    checked_boxes = [checkboxes[i] for i, var in enumerate(checkbox_vars) if var.get() == 1]
    # Procedural updates
    update_spreadsheet(checked_boxes, rating, classif)
    classify()
    image_paths.remove(recent)
    display_images()
    # Reset these so incomplete forms aren't submitted
    classif, rating = None, None
    

# Initialize variables
directory = None
image_paths = []          # Keep track of the classified images
large_image = None        # The image from which segment is pulled
large_image_area = None   # It avoids like 1 call to cv but it more efficient
image = None              # Image segment -- Actually I'm pretty sure this var is only utilized once.
recent = None             # Keep a reference to the image segment
label_large = None        # Used for formatting
label_small = None        # Used for formatting images
classif = None            # The selected constituent
rating = None             # The selected alteration score
images_frame = None

# Just ensuring that we have this from outer scope. You can also specify the path explicitly
f = open(home + '/NAV_helper.txt', 'r')
home_data = f.read()
spreadsheet_path = home_data + '/Point_Counts.xlsx'
f.close()

# Create the main window
root = tk.Tk()
root.title("Facies Classification Captcha")

# Create all the buttons and frames to make everything pretty
text_frame = tk.Frame(root)
text_frame.pack(side = tk.TOP, padx=10, pady=10)
T = tk.Label(text_frame, text="Facies Classification", height=2, width=30).pack(side=tk.LEFT)
T2 = tk.Label(text_frame, text="Features", height=2, width=30).pack(side=tk.LEFT)
T3 = tk.Label(text_frame, text="Alteration Score", height=2, width=30).pack(side=tk.LEFT)

buttons_frame = tk.Frame(root)
buttons_frame.pack(side = tk.TOP, padx=10, pady=10)

frame_classificationbuttons = tk.Frame(buttons_frame)
frame_classificationbuttons.pack(side = tk.LEFT, padx=10, pady=10)

frame_checkbuttons = tk.Frame(buttons_frame)
frame_checkbuttons.pack(side=tk.LEFT, padx=10, pady=10)

# Lmao okay this is a terrible variable name, these are the buttons for alteration scoring
frame_buttons = tk.Frame(buttons_frame)
frame_buttons.pack(side=tk.LEFT, padx=10, pady=10)

# Two copies of this, one is used for spreadsheet references
classifications_order = ['Ooids', 'Mud', 'Bioclasts', 'Unknown',	'Total_mapped_area']
classifications = ['Bioclasts', 'Mud', 'Ooids', 'Non-Sample', 'Unknown']
for i in range(1, 6):
    button = tk.Button(frame_classificationbuttons, text=f"{classifications[i-1]}", fg = 'green', command=lambda value=classifications[i-1]: update_classif(value), width = 25)
    button.pack(fill = 'both', pady=2)

checkboxes = ['Organic Rich', 'Pore Space', 'Micritization-Cementation']
checkbox_vars = []
for i in range(1, 4):
    var = tk.IntVar()
    checkbox = ttk.Checkbutton(frame_checkbuttons, text=f"{checkboxes[i - 1]}", variable=var)
    checkbox.pack(anchor='w', pady=2)
    checkbox_vars.append(var)

alterations = ['Unaltered', 'Some Alteration (1-30%)', 'Patchy or Moderate Alteration (30-60%)', 'Patchy Nonalteration (60-80%)', 'Completely Altered']
# Add 4 regular buttons to the right
for i in range(1, 6):
    button = tk.Button(frame_buttons, text=f"{alterations[i - 1]}", fg = 'green', command=lambda value=i: update_rating(value), width = 25)
    button.pack(anchor='e', pady=2)
    
# Button to select directory
button_select = Button(root, text="Select Directory", fg = 'green', command=select_directory)
button_select.pack(pady=10, side=tk.BOTTOM)

# Add the submit button at the bottom
submit_button = tk.Button(root, text="Submit", fg = 'green', command=submit_action)
submit_button.pack(side=tk.TOP, pady=1)

root.mainloop()
