import itertools

from pylibdmtx.pylibdmtx import encode
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

g_image_folder_name = r'generated_images' # r denotes a raw string, so \ is only a backslash
id_folder_name = r'id_images'
pw_folder_name = r'pw_images'
tag_folder_name = r'tag_images'

font_name = ImageFont.truetype("calibri.ttf", 16)
font_subtext = ImageFont.truetype("calibri.ttf", 11)

# Box size = 1"x2.63" = 96x252.48 pixels
tag_w, tag_h = (253, 95) # 96 pixels resulted in 1.02"

def create_tag(directory_in, filename, single_employee=-1):
    testing = single_employee >= 0

    if testing:
        image_folder_name = r'testing_generated_images'
    else:
        image_folder_name = g_image_folder_name

    final_directory = os.path.join(directory_in, image_folder_name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    id_directory = os.path.join(final_directory, id_folder_name)
    if not os.path.exists(id_directory):
        os.makedirs(id_directory)
    pw_directory = os.path.join(final_directory, pw_folder_name)
    if not os.path.exists(pw_directory):
        os.makedirs(pw_directory)
    tag_directory = os.path.join(final_directory, tag_folder_name)
    if not os.path.exists(tag_directory):
        os.makedirs(tag_directory)

    directory_tag_folder_str = f'{directory_in}\\{image_folder_name}\\{tag_folder_name}'
    directory = os.fsencode(directory_tag_folder_str)
    # print(directory_tag_folder_str)
    # print(directory)

    fields = []
    rows = []
    testing_rows = []

    if os.path.exists(directory_in + '\\' + filename):
        # print(f'file exists: {filename}')
        pass
    else:
        # print(f'file doesn\'t exist: {filename}')
        return


    # Open the CSV file and determine the number of columns (fields) of data
    with open(filename, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)  # (csvfile, delimiter=' ', quotechar='|')
        csv_fields = next(csvreader)

        if testing:
            rows.append(next(itertools.islice(csvreader, single_employee, None))) # just look at 11th employee rather than read entire csv
        else:
            for row in csvreader:
                rows.append(row)

    #     # get total number of rows
    #     print("Total no. of Employees: %d" % (csvreader.line_num - 1))
    #
    # # printing the field names
    # print('Field names are:' + ', '.join(field for field in csv_fields))


    # Determine the columns of the csv with the correct data
    ID_Column = None
    Last_Name_Column = None
    First_Name_Column = None
    for i in range(len(csv_fields)):
        if csv_fields[i] == 'Employee ID':
            ID_Column = i
        elif csv_fields[i] == 'Last Name':
            Last_Name_Column = i
        elif csv_fields[i] == 'First Name':
            First_Name_Column = i

    # Verify that the data was found
    if isinstance(ID_Column, int) and isinstance(Last_Name_Column, int) and isinstance(First_Name_Column, int):
        # Iterate through each employee
        for index, row in enumerate(rows):
            #     print(index, row)
            # row = rows[10]
            # print(f'{row[First_Name_Column]}_{row[Last_Name_Column]}') <- Samuel Clemens appears
            # Create Data Matrix for ID Number
            encoded = encode(row[ID_Column].encode('utf8'))
            # print(encoded.width, encoded.height, encoded.pixels)
            img_id = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
            img_id.save(
                f'{directory_in}\\{image_folder_name}\\{id_folder_name}\\{row[First_Name_Column]}_{row[Last_Name_Column]}_ID_DataMatrix.png')

            # Create Data Matrix for Password (M before the ID Number)
            encoded = encode(('M' + row[ID_Column]).encode('utf8'))

            img_pw = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
            img_pw.save(
                f'{directory_in}\\{image_folder_name}\\{pw_folder_name}\\{row[First_Name_Column]}_{row[Last_Name_Column]}_PW_DataMatrix.png')

            # Create the Employee Tag with the Data Matrices
            # Start with a white box (Background)
            img_tag = Image.new(mode='RGB', size=(tag_w, tag_h), color=(255, 255, 255))  # color = (153, 153, 255)) #

            # Retrieve the size of the ID matrix and paste the image on the tag background
            dm_w, dm_h = img_id.size
            img_tag.paste(img_id, (tag_w // 2 - dm_w, tag_h - dm_h))

            # Resize the password matrix to the same size as the ID matrix, paste the new image onto the tag
            # img_pw = img_pw.resize(img_id.size)
            dm_w, dm_h = img_pw.size
            img_tag.paste(img_pw, (tag_w - dm_w, tag_h - dm_h))

            # img_pw_new = img_pw.resize((img_id.size), Image.LANCZOS)
            # img_pw_new.save(f'{directory_in}\\{image_folder_name}\\{pw_folder_name}\\{row[First_Name_Column]}_{row[Last_Name_Column]}_PW_DataMatrix_new.png', quality=100)

            # Draw all text, first the employee name near the top, then the ID and password to the left of their matrices
            draw = ImageDraw.Draw(img_tag)
            draw.text((7, 8), f'{row[First_Name_Column]} {row[Last_Name_Column]}', (0, 0, 0), font=font_name)
            draw.text((7, tag_h - 20), "Username", (0, 0, 0), font=font_subtext)
            draw.text((tag_w // 2 + 7, tag_h - 20), "Password", (0, 0, 0), font=font_subtext)

            # print(img_tag.size)
            # img_tag = img_tag.resize(1.03125 * img_tag.size) # 1 1/32"

            img_tag = ImageOps.expand(img_tag, border=1, fill=(0, 0, 0))

            # Save the tag PNG
            img_tag_filename = f'{directory_in}\\{image_folder_name}\\{tag_folder_name}\\{row[First_Name_Column]}_{row[Last_Name_Column]}_tag.png'
            img_tag.save(img_tag_filename)


            if testing:
                # Looking into dissecting the encoded pixel from the generated data matrix. I'm focusing on the PW data matrix
                # encoded.width, encoded.height = 80, 80
                # encoded.pixel is a long string prefixed by "b" and the string is encircled by ' ', each pixel is either \xff or \x00 for 255 or 0

                myList = [[0 for _ in range(0,encoded.width)] for _ in range(0,encoded.height)]

                for i in range(encoded.height):
                    for j in range(encoded.width):
                        # print(i*encoded.height + j)
                        # myMatrix[j][i] = encoded.pixels[i*encoded.height + j]
                        myList[i][j] = (encoded.pixels[i*encoded.height + j])
                    # print(f'{i} - next---------------------------------')

                myMatrix = np.array(myList)
                # print(encoded.width, encoded.height, encoded.pixels)

                plt.figure()
                im = plt.imshow(myMatrix, interpolation='none', vmin=0, vmax=1, aspect='equal', cmap='grey')
                ax = plt.gca()

                # Major ticks
                ax.set_xticks(np.arange(0, 80, 5))
                ax.set_yticks(np.arange(2, 81, 2))

                # Labels for major ticks
                ax.set_xticklabels(np.arange(1, 81, 5))
                ax.set_yticklabels(np.arange(2, 81, 2))

                # Minor ticks
                ax.set_xticks(np.arange(-.5, 80, 1), minor=True)
                ax.set_yticks(np.arange(-.5, 80, 1), minor=True)

                # Gridlines based on minor ticks ('0.8' is read as greyscale)
                # https://matplotlib.org/stable/users/explain/colors/colors.html#colors-def
                ax.grid(which='minor', color='0.8', linestyle='-', linewidth=1)

                # Remove minor ticks
                ax.tick_params(which='minor', bottom=False, left=False)

                plt.show()

    return directory_tag_folder_str

if __name__ == "__main__":
    create_tag("C:\\pythonProject\\Employee_Tag_Generator", "Employee ID List.csv", single_employee=0)
