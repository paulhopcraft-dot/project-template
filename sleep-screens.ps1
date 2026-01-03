# Sleep Screens - Turn off monitors, any input wakes them
(Add-Type '[DllImport("user32.dll")]public static extern int SendMessage(int hWnd,int hMsg,int wParam,int lParam);' -Name a -Pas)::SendMessage(-1,0x0112,0xF170,2)
