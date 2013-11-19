' Prompts for a set of image files and inserts them into the active slide as a row of 100x100 images
' Currently lots of hardcoded aspects, see InsertAndSizePicture to change size and spacing
' Manually change "row" in InsertGridOfImages to place additional rows
'
' License: WTFPL
' pst@coffeetocode.net


Private Function InsertAndSizePicture(imageFilePath As String, row As Integer, col As Integer) As Integer
    ' Initial code borrowed from http://www.pptfaq.com/FAQ00329_Insert_a_picture_at_the_correct_size.htm

    Dim topGutter As Integer
    Dim leftGutter As Integer
    Dim horizontalSpacing As Integer
    Dim verticalSpacing As Integer
    Dim imgWidth As Integer
    Dim imgHeight As Integer
    topGutter = 50
    leftGutter = 100
    verticalSpacing = 15
    horizontalSpacing = 15
    imgWidth = 100
    imgHeight = 100

    Dim oPicture As Shape
    Dim FullPath As String
    Dim oSl As Slide

    ' Set this to the full path to picture.
    FullPath = imageFilePath

    Set oSl = ActiveWindow.Selection.SlideRange(1)

    ' Insert the picture at an arbitrary size;
    ' PowerPoint requires you to supply *some* height and width for the picture
    Set oPicture = oSl.Shapes.AddPicture(FileName:=FullPath, _
       LinkToFile:=msoFalse, _
       SaveWithDocument:=msoTrue, _
       Left:=0, Top:=0, _
       Width:=imgWidth, Height:=imgHeight)

    ' Rescale the picture to its "natural" slze
    'With oPicture
    '   .ScaleHeight 1, msoTrue
    '   .ScaleWidth 1, msoTrue
    'End With

    With ActivePresentation.PageSetup
       'oPicture.Left = (.SlideWidth \ 5) - (oPicture.Width \ 5)
       'oPicture.Top = (.SlideHeight \ 5) - (oPicture.Height \ 5)
       'oPicture.Left = (1 + col) * (.SlideWidth \ 11)
       'oPicture.Top = row * (.SlideHeight \ 8)
       oPicture.Left = leftGutter + (imgWidth * col) + (horizontalSpacing * col - 1)
       oPicture.Top = topGutter + (imgHeight * row) + (verticalSpacing * row - 1)
       
       
       'oPicture.Select
    End With

    Set oPicture = Nothing
    Set oSl = Nothing
    InsertAndSizePicture = 1

End Function

Private Function PickFiles() As Collection
   'Initial code from http://msdn.microsoft.com/en-us/library/aa432103(v=office.12).aspx
   Dim ret As Collection
   Set ret = New Collection

   Set fDialog = Application.FileDialog(msoFileDialogFilePicker)

   With fDialog

      ' Allow user to make multiple selections in dialog box
      .AllowMultiSelect = True
            
      ' Set the title of the dialog box.
      .Title = "Please select one or more files"

      ' Clear out the current filters, and add our own.
      .Filters.Clear
      .Filters.Add "JPEG Files", "*.JPG"
      .Filters.Add "PNG Files", "*.PNG"
      .Filters.Add "Bitmap Files", "*.BMP"
      .Filters.Add "All Files", "*.*"

      ' Show the dialog box. If the .Show method returns True, the
      ' user picked at least one file. If the .Show method returns
      ' False, the user clicked Cancel.
      If .Show = True Then

         'Loop through each file selected and add it to our list box.
         For Each varFile In .SelectedItems
         '   'Me.FileList.AddItem varFile
         '   MsgBox varFile
             ret.Add (varFile)
         Next

      Else
         MsgBox "You clicked Cancel in the file dialog box."
      End If
      
   End With
   
   'For Each varFile In ret
   '    'Me.FileList.AddItem varFile
   '    MsgBox varFile
   'Next
   
   
   Set PickFiles = ret
End Function

Sub InsertGridOfImages()
    
    Dim foo As Integer
    Dim files As Collection
    
    Set files = PickFiles()
    
    Dim row As Integer
    Dim col As Integer
    'Row should be an odd number (for spacing)
    row = 0
    col = 0
    
    row = InputBox("Place images on which row (Starting at 0)?", "asdasd")
    
    For Each myFile In files
        'MsgBox (myFile.Path)
        foo = InsertAndSizePicture((myFile), row, col)
        col = col + 1
    Next

End Sub
