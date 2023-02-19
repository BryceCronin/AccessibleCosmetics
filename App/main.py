import os
import PySimpleGUI as sg
import subprocess
import layout
import datetime

# Create Window
window = sg.Window('Access3D Generator', layout.layout, icon='Images\icon.ico', element_justification='c')

# Initiate variables
file_input = ""
file_output = ""

# Event Loop to process 'events' and get the 'values' of the inputs
while True:
    event, values = window.read()

    # Close App
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

    # Input A3D File
    if event == "browse_input":
        selected = sg.popup_get_file(
            "Select A3D File",
            file_types=((('A3D Files Only', '*.A3D'),)),
            no_window = True,
            history=True )
        if selected != "":
            file_input = selected
            print('new browse input: ' + file_input)
            window['text_input'].update("Selected A3D File: " + os.path.basename(file_input))
            window['browse_input'].update("Change")
            window['image_inputFile'].update('Images\inputFile_done.png')
    if file_input == "":
        window['text_input'].update("Select A3D File:")
        window['browse_input'].update("Browse")
        window['image_inputFile'].update('Images\inputFile.png')
        
    # Select Output Location
    if event == "browse_output":
        selected = sg.popup_get_folder(
            "Choose Output Location",
            no_window = True, )
        if selected != "":
            file_output = selected
            print('new browse output: ' + file_output)  
            window['text_output'].update("Selected Output Folder: ..." + file_output[-20:])
            window['browse_output'].update("Change")
            window['image_selectFolder'].update('Images\selectFolder_done.png')
    if file_output == "":
        window['text_output'].update("Select Output Folder:")
        window['browse_output'].update("Browse")
        window['image_selectFolder'].update('Images\selectFolder.png')

    # Continue to configure
    if file_input != "" and file_output != "":
        window['button_configure'].update(visible=True)
    if event == 'button_configure':
        window['column_initial'].update(visible=False)
        window['column_configure'].update(visible=True)

    # Return to initial
    if event == 'button_back':
        window['column_initial'].update(visible=True)
        window['column_configure'].update(visible=False)

    # Export STL File
    if event == 'button_export':
        outputFile = (file_output + '/' + os.path.basename(file_input)[:-4] + '.stl')
        if (os.path.isfile(outputFile)):
            outputFile = (file_output + '/' + os.path.basename(file_input)[:-4] + '_' + ((datetime.datetime.now()).strftime("%H %M %S")).replace(" ","-") )
        openScadString = ('openscad -o ' + outputFile + '_output.stl -D"vartest2=5" ' + file_input)
        print(openScadString )
        subprocess.Popen(openScadString)

    # Read A3D File
    if event == 'button_readA3D':
        print('Attempting to read A3D file...')

        A3D_file = ((open(file_input)))
        A3D_lines = (A3D_file.readlines()) # Each line in a list
        A3D_lineCount = len(A3D_lines) # Number of lines
        A3D_start = -1 # Line number of A3D-Start
        A3D_end = - 1 # Line number of A3D-End

        # Get Line number of A3D-Start
        for x in range(A3D_lineCount):
            search = A3D_lines[x].find("A3D-Start")
            if search != -1:
                A3D_start = x
                break
            else:
                A3D_start = -1

        # Get Line number of A3D-End
        for x in range(A3D_lineCount):
            search = A3D_lines[x].find("A3D-End")
            if search != -1:
                A3D_end = x
                break
            else:
                A3D_end = -1

        print('Starts at line ' + str(A3D_start+1))
        print('Ends at line ' + str(A3D_end+1))

        for x in range (A3D_start,A3D_end):
            print(x)
            # todo: convert each line of the A3D notation into buttons on the form


window.close()