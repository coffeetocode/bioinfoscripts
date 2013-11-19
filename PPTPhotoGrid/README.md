##Powerpoint Image Grid Inserter##

Script state:
 - [x] Script short description
 - [x] Script full description
 - [ ] Accepts command line params
 - [ ] Sample inputs
 - [ ] Sample outputs
 - [x] Commented

###Detailed usage: To Set up the Macro In Your Presentation###
1. Open your powerpoint file (or create a brand new one). 
2. In the "File" tab, select "Save As"
3. In the Save As dialog, click the "Save as Type" dropdown and select "PowerPoint Macro-Enabled Presentation (*.pptm)"
4. The title bar at the very top should now have .pptm at the end of the filename, indicating macros are enabled.
5. On the "View" tab, there should be a button on the far right for "Macros"; click it.
6. In the "Macro" dialog there will be a textbox for "Macro Name:". Type in: InsertGridOfImages
7. The "Create" button should become available; click OK
8. A new window will pop up allowing you to define the new macro. There will already be some text there ("sub InsertGridOfImages" through "end"); delete all the text. 
9. Copy the entire contents of ImageGrid.vbs and paste it in where you just delete the old macro code.
10. From the "File" menu, select "Save" (or Ctrl-S)
11. Close the Microsoft Visual Basic For Applications window. 
11. The macro is now ready to use

###Detailed usage: Using the macro###
1. Create a new blank slide where you'll want the photo grid inserted
2. On the "View" tab, click "Macros". The InsertGridOfImages macro will be available. Click "Run"
3. Select images you want to place in one row and click OK
4. In the next screen, provide the row number (starting with 0)
5. Click OK and photos will be automatically inserted, size, and positioned

The current values are chosen to support 4 rows of 5 columns; that can be changed by playing with the constants in the code

