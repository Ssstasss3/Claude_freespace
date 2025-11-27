Attribute VB_Name = "TanksGame"
Option Explicit

' Game constants
Const BOARD_WIDTH As Integer = 50
Const BOARD_HEIGHT As Integer = 30
Const GAME_SPEED As Integer = 100

' Game state
Dim gameRunning As Boolean
Dim player1 As Object
Dim player2 As Object
Dim bullets As Collection
Dim obstacles As Collection
Dim gameSheet As Worksheet

' Player type
Type Tank
    x As Integer
    y As Integer
    direction As Integer ' 0=right, 1=down, 2=left, 3=up
    health As Integer
    color As Long
    controls As String
End Type

Dim tank1 As Tank
Dim tank2 As Tank

Sub InitializeGame()
    Application.ScreenUpdating = False

    Set gameSheet = ThisWorkbook.Sheets("Game")
    gameSheet.Cells.Clear

    ' Setup game board
    With gameSheet
        .Cells.RowHeight = 15
        .Cells.ColumnWidth = 2

        ' Draw border
        Dim i As Integer
        For i = 1 To BOARD_WIDTH
            .Cells(1, i).Interior.Color = RGB(50, 50, 50)
            .Cells(BOARD_HEIGHT, i).Interior.Color = RGB(50, 50, 50)
        Next i
        For i = 1 To BOARD_HEIGHT
            .Cells(i, 1).Interior.Color = RGB(50, 50, 50)
            .Cells(i, BOARD_WIDTH).Interior.Color = RGB(50, 50, 50)
        Next i
    End With

    ' Initialize Player 1 (Blue)
    tank1.x = 5
    tank1.y = 15
    tank1.direction = 0
    tank1.health = 100
    tank1.color = RGB(0, 212, 255)
    tank1.controls = "WASDQ"

    ' Initialize Player 2 (Pink)
    tank2.x = 45
    tank2.y = 15
    tank2.direction = 2
    tank2.health = 100
    tank2.color = RGB(255, 0, 234)
    tank2.controls = "ARROWS"

    ' Create obstacles
    Set obstacles = New Collection
    AddObstacle 15, 10, 3, 3
    AddObstacle 35, 10, 3, 3
    AddObstacle 25, 15, 3, 3
    AddObstacle 10, 22, 4, 2
    AddObstacle 38, 22, 4, 2
    AddObstacle 23, 5, 5, 2

    Set bullets = New Collection

    DrawObstacles
    DrawTank tank1
    DrawTank tank2
    DrawUI

    Application.ScreenUpdating = True

    MsgBox "ТАНЧИКИ НА ДВОИХ" & vbCrLf & vbCrLf & _
           "Player 1 (Blue): W/A/S/D to move, Q to shoot" & vbCrLf & _
           "Player 2 (Pink): Arrow keys to move, Enter to shoot" & vbCrLf & vbCrLf & _
           "Press ESC to stop game", vbInformation, "Game Ready!"
End Sub

Sub AddObstacle(x As Integer, y As Integer, w As Integer, h As Integer)
    Dim obs As Object
    Set obs = CreateObject("Scripting.Dictionary")
    obs("x") = x
    obs("y") = y
    obs("w") = w
    obs("h") = h
    obstacles.Add obs
End Sub

Sub DrawObstacles()
    Dim obs As Object
    Dim i As Integer, j As Integer

    For Each obs In obstacles
        For i = obs("x") To obs("x") + obs("w") - 1
            For j = obs("y") To obs("y") + obs("h") - 1
                gameSheet.Cells(j, i).Interior.Color = RGB(80, 80, 100)
            Next j
        Next i
    Next obs
End Sub

Sub DrawTank(tank As Tank)
    ' Draw 3x3 tank
    Dim i As Integer, j As Integer

    For i = -1 To 1
        For j = -1 To 1
            If tank.x + i > 0 And tank.x + i <= BOARD_WIDTH And _
               tank.y + j > 0 And tank.y + j <= BOARD_HEIGHT Then
                gameSheet.Cells(tank.y + j, tank.x + i).Interior.Color = tank.color
            End If
        Next j
    Next i

    ' Draw barrel
    Select Case tank.direction
        Case 0 ' Right
            If tank.x + 2 <= BOARD_WIDTH Then
                gameSheet.Cells(tank.y, tank.x + 2).Interior.Color = tank.color
            End If
        Case 1 ' Down
            If tank.y + 2 <= BOARD_HEIGHT Then
                gameSheet.Cells(tank.y + 2, tank.x).Interior.Color = tank.color
            End If
        Case 2 ' Left
            If tank.x - 2 > 0 Then
                gameSheet.Cells(tank.y, tank.x - 2).Interior.Color = tank.color
            End If
        Case 3 ' Up
            If tank.y - 2 > 0 Then
                gameSheet.Cells(tank.y - 2, tank.x).Interior.Color = tank.color
            End If
    End Select
End Sub

Sub ClearTank(tank As Tank)
    Dim i As Integer, j As Integer

    For i = -2 To 2
        For j = -2 To 2
            If tank.x + i > 0 And tank.x + i <= BOARD_WIDTH And _
               tank.y + j > 0 And tank.y + j <= BOARD_HEIGHT Then
                If Not IsObstacle(tank.x + i, tank.y + j) And _
                   Not IsBorder(tank.x + i, tank.y + j) Then
                    gameSheet.Cells(tank.y + j, tank.x + i).Interior.ColorIndex = xlNone
                End If
            End If
        Next j
    Next i
End Sub

Function IsObstacle(x As Integer, y As Integer) As Boolean
    Dim obs As Object
    IsObstacle = False

    For Each obs In obstacles
        If x >= obs("x") And x < obs("x") + obs("w") And _
           y >= obs("y") And y < obs("y") + obs("h") Then
            IsObstacle = True
            Exit Function
        End If
    Next obs
End Function

Function IsBorder(x As Integer, y As Integer) As Boolean
    IsBorder = (x <= 1 Or x >= BOARD_WIDTH Or y <= 1 Or y >= BOARD_HEIGHT)
End Function

Function CanMoveTo(x As Integer, y As Integer) As Boolean
    CanMoveTo = Not IsBorder(x, y) And Not IsObstacle(x, y)
End Function

Sub MoveTank(ByRef tank As Tank, direction As Integer)
    Dim newX As Integer, newY As Integer
    newX = tank.x
    newY = tank.y

    tank.direction = direction

    Select Case direction
        Case 0: newX = newX + 1 ' Right
        Case 1: newY = newY + 1 ' Down
        Case 2: newX = newX - 1 ' Left
        Case 3: newY = newY - 1 ' Up
    End Select

    If CanMoveTo(newX, newY) Then
        ClearTank tank
        tank.x = newX
        tank.y = newY
        DrawTank tank
    End If
End Sub

Sub ShootBullet(tank As Tank)
    Dim bullet As Object
    Set bullet = CreateObject("Scripting.Dictionary")

    bullet("x") = tank.x
    bullet("y") = tank.y
    bullet("dx") = 0
    bullet("dy") = 0
    bullet("owner") = IIf(tank.color = tank1.color, 1, 2)

    Select Case tank.direction
        Case 0: bullet("dx") = 1 ' Right
        Case 1: bullet("dy") = 1 ' Down
        Case 2: bullet("dx") = -1 ' Left
        Case 3: bullet("dy") = -1 ' Up
    End Select

    bullets.Add bullet
End Sub

Sub UpdateBullets()
    Dim bullet As Object
    Dim i As Integer
    Dim toRemove As New Collection

    For i = bullets.Count To 1 Step -1
        Set bullet = bullets(i)

        ' Clear old position
        If Not IsObstacle(bullet("x"), bullet("y")) And _
           Not IsBorder(bullet("x"), bullet("y")) Then
            gameSheet.Cells(bullet("y"), bullet("x")).Interior.ColorIndex = xlNone
        End If

        ' Update position
        bullet("x") = bullet("x") + bullet("dx")
        bullet("y") = bullet("y") + bullet("dy")

        ' Check collisions
        If IsBorder(bullet("x"), bullet("y")) Or IsObstacle(bullet("x"), bullet("y")) Then
            bullets.Remove i
        ElseIf CheckBulletHit(bullet) Then
            bullets.Remove i
        Else
            ' Draw bullet
            gameSheet.Cells(bullet("y"), bullet("x")).Interior.Color = RGB(255, 255, 0)
        End If
    Next i
End Sub

Function CheckBulletHit(bullet As Object) As Boolean
    CheckBulletHit = False

    ' Check hit on tank1
    If bullet("owner") <> 1 Then
        If Abs(bullet("x") - tank1.x) <= 1 And Abs(bullet("y") - tank1.y) <= 1 Then
            tank1.health = tank1.health - 20
            CheckBulletHit = True
            If tank1.health <= 0 Then
                EndGame "Player 2 (Pink) WINS!"
            End If
            DrawUI
        End If
    End If

    ' Check hit on tank2
    If bullet("owner") <> 2 Then
        If Abs(bullet("x") - tank2.x) <= 1 And Abs(bullet("y") - tank2.y) <= 1 Then
            tank2.health = tank2.health - 20
            CheckBulletHit = True
            If tank2.health <= 0 Then
                EndGame "Player 1 (Blue) WINS!"
            End If
            DrawUI
        End If
    End If
End Function

Sub DrawUI()
    With gameSheet
        .Cells(BOARD_HEIGHT + 2, 1).Value = "Player 1 HP:"
        .Cells(BOARD_HEIGHT + 2, 7).Value = tank1.health & "%"
        .Cells(BOARD_HEIGHT + 2, 7).Font.Color = tank1.color
        .Cells(BOARD_HEIGHT + 2, 7).Font.Bold = True

        .Cells(BOARD_HEIGHT + 3, 1).Value = "Player 2 HP:"
        .Cells(BOARD_HEIGHT + 3, 7).Value = tank2.health & "%"
        .Cells(BOARD_HEIGHT + 3, 7).Font.Color = tank2.color
        .Cells(BOARD_HEIGHT + 3, 7).Font.Bold = True
    End With
End Sub

Sub StartGame()
    InitializeGame
    gameRunning = True
    GameLoop
End Sub

Sub GameLoop()
    Do While gameRunning
        UpdateBullets
        DoEvents
        Application.Wait (Now + TimeValue("0:00:00") + TimeSerial(0, 0, 0) + TimeValue("0:00:00.1"))
    Loop
End Sub

Sub EndGame(winner As String)
    gameRunning = False
    MsgBox winner, vbExclamation, "GAME OVER!"
End Sub

Sub StopGame()
    gameRunning = False
End Sub

' Keyboard event handler - needs to be set up in worksheet
Sub HandleKey(KeyCode As Integer, shift As Boolean)
    If Not gameRunning Then Exit Sub

    Select Case KeyCode
        ' Player 1 controls (WASD)
        Case 87: MoveTank tank1, 3 ' W - Up
        Case 83: MoveTank tank1, 1 ' S - Down
        Case 65: MoveTank tank1, 2 ' A - Left
        Case 68: MoveTank tank1, 0 ' D - Right
        Case 81: ShootBullet tank1  ' Q - Shoot

        ' Player 2 controls (Arrows)
        Case 38: MoveTank tank2, 3 ' Up arrow
        Case 40: MoveTank tank2, 1 ' Down arrow
        Case 37: MoveTank tank2, 2 ' Left arrow
        Case 39: MoveTank tank2, 0 ' Right arrow
        Case 13: ShootBullet tank2  ' Enter - Shoot

        ' ESC to quit
        Case 27: StopGame
    End Select
End Sub
