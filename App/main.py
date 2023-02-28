import os
import PySimpleGUI as sg
import subprocess
import layout
import datetime
import A3D
import STL
import PySimpleGUI as sg
import math

default_font = "Arial 13 normal"
bold_font = "Arial 13 bold"

# Create Window
window = sg.Window('Access3D Generator', layout.layout, icon='Images\icon.ico', element_justification='c', margins=(0,0), font=default_font)

checked = 'Images\inputCheckbox_1.png'
unchecked = 'Images\inputCheckbox_0.png'
data = {0:unchecked, 1:checked}

# Initiate variables
file_input = ""
file_output = ""
file_valid = True

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
            history=True,
            initial_folder="A3D_Sample_files", )
        if selected != "":
            if (A3D.initiateFile(selected) == True): # Valid A3D file
                file_input = selected
                if file_input != "" and file_output != "":
                    window['button_configure'].update(visible=True)
                print('new browse input: ' + file_input)
                window['invalidFile'].update(visible=False)
                window['text_input'].update("Selected A3D File: " + os.path.basename(file_input))
                window['browse_input'].update("Change")
                window['image_inputFile'].update('Images\inputFile_done.png')
                file_valid = True
            else: # Invalid A3D file
                file_input = selected
                window['button_configure'].update(visible=False)
                window['invalidFile'].update(visible=True)
                window['text_input'].update("Invalid A3D File: " + os.path.basename(file_input))
                window['browse_input'].update("Replace")
                window['image_inputFile'].update('Images\inputFile_error.png')
                file_valid = False
    if file_input == "" and file_valid == True:
        window['text_input'].update("Select A3D File:")
        window['browse_input'].update("Browse")
        window['image_inputFile'].update('Images\inputFile.png')
        
    # Select Output Location
    if event == "browse_output":
        selected = sg.popup_get_folder(
            "Choose Output Location",
            no_window = True,
            initial_folder="Output", )
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
    if file_input != "" and file_output != "" and file_valid == True:
        window['button_configure'].update(visible=True)
    if event == 'button_configure':
        window['column_initial'].update(visible=False)
        window['column_configure'].update(visible=True)

        A3D.initiateFile(file_input)
        list = A3D.extractFields(A3D.getStart(),A3D.getEnd())
        for x in range(len(list)):
            id = ""
            desc = ""
            title = ""
            type = ""
            config_line = ""

            for y in range(len(list[x])):
                if y == 0:
                    id = (str((list)[x][y]))
                elif y == 1:
                    title = (str((list)[x][y]))
                elif y == 2:
                    desc += (str((list)[x][y]))
                elif y == 3:    
                    type += (str((list)[x][y]))
            
            if (str(list[x][3]))==('boolean'):
                if len(A3D.formatString(desc)) < 46:
                    lineheight = math.ceil(len(A3D.formatString(desc)) / 56 )
                else:
                    lineheight = 1
                config_line = sg.Image('Images\inputCheckbox_0.png', enable_events=True, metadata=False, key=('CHECK', x)), sg.Text(A3D.formatString(title), pad=((15,0),(0,0)), font=bold_font, text_color="#263238"),sg.Text(A3D.formatString(desc), pad=8, font=default_font, text_color="#455A64", size=(45,lineheight)),
            elif (str(list[x][3]))==('integer'):
                if len(A3D.formatString(desc)) < 46:
                    lineheight = math.ceil(len(A3D.formatString(desc)) / 56 )
                else:
                    lineheight = 1
                config_line = sg.Image('Images\inputRounded_l.png', pad=(0,0)),sg.Input("0", key=A3D.formatString(id), size=7, background_color="#BBDEFB", text_color="#263238", pad=(0,0), font=bold_font, justification="center"),sg.Image('Images\inputRounded_r.png', pad=(0,0)), sg.Text(A3D.formatString(title), pad=((15,0),(0,0)), font=bold_font, text_color="#263238"),sg.Text(A3D.formatString(desc), pad=8, font=default_font, text_color="#455A64",  size=(45,lineheight)),
            window.extend_layout(window['config_column'], [config_line])

        STL.draw_STL(window['fig_cv'].TKCanvas, STL.prepare_STL('Output\Test2.stl'))

    # Return to initial
    if event == 'button_back':
        window['column_initial'].update(visible=True)
        window['column_configure'].update(visible=False)

    # Export STL File
    if event == 'button_export':
        outputFile = (file_output + '/' + os.path.basename(file_input)[:-4] + '_'+ ((datetime.datetime.now()).strftime("%Y %m %d")).replace(" ","-") + "_" + ((datetime.datetime.now()).strftime("%H %M %S")).replace(" ","-") )
        openScadString = ('openscad -o ' + outputFile + '_output.stl')

        # Append variables
        for x in range(len(list[x])+1):
            # put variables in string
            openScadString = (openScadString + ' -D\"' + (A3D.formatString(str(A3D.fieldList[x][0]))) + "=")
            if (str(A3D.fieldList[x][3])=='boolean'):
                openScadString = (openScadString + "true\"")
            elif (str(A3D.fieldList[x][3])=='integer'):
                openScadString = (openScadString + values[A3D.formatString(str(A3D.fieldList[x][0]))] +'\"')
                
        openScadString = (openScadString + ' ' + file_input)
        process = subprocess.Popen(openScadString)     
        process.wait()
        savedFile = outputFile + '_output.stl'
        STL.draw_STL(window['fig_cv'].TKCanvas, STL.update_STL(savedFile)) 

    if isinstance(event, tuple) and event[0]=='CHECK':
        state = not window[event].metadata
        window[event].metadata = state
        window[event].update(filename=data[state])

window.close()