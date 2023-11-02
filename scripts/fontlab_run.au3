; Define a flag to keep track of whether the "FontLab 8 Activation" dialog has been closed
Local $activationDialogClosed = False

; Loop until the "FontLab 8 Activation" dialog has been closed
While Not $activationDialogClosed
    ; Check for the "FontLab Crash Report" dialog and close it if found
    If WinExists("FontLab Crash Report") Then
        WinClose("FontLab Crash Report")
    EndIf
    
    ; Check for the "FontLab 8 Activation" dialog and close it if found
    If WinExists("FontLab 8 Activation") Then
        WinClose("FontLab 8 Activation")
        $activationDialogClosed = True  ; Set the flag to exit the loop
    EndIf
    
    ; Sleep for a short duration to prevent the script from consuming too much CPU
    Sleep(100)
WEnd
Exit
