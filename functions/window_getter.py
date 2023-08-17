import win32gui

def get_window(window_name_keywords):
    result = []
    def winEnumHandler(hwnd, ctx):
        for keyword in window_name_keywords:
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == keyword or keyword in win32gui.GetWindowText(hwnd):
                result.append(hwnd)
    win32gui.EnumWindows(winEnumHandler, None)
    return result

def bring_window_to_front(window_handle):
    win32gui.SetForegroundWindow(window_handle)
