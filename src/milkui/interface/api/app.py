def exit(app):
    app.exit()

def set_full_screen(app):
    app.set_full_screen(app.main_window)

def exit_full_screen(app):
    app.exit_full_screen()

def toggle_full_screen(app):
    if app.is_full_screen:
        app.exit_full_screen()
    else:
        app.set_full_screen(app.main_window)