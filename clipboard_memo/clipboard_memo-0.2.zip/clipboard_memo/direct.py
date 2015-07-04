from clipboard_memo.main import ClipboardMemo

def direct_save():
    """Directly save memo when the keyboard shortcut is pressed"""
    c = ClipboardMemo()
    c.save()