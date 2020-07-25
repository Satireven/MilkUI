def info(window, title='Milk', message='Hello World'):
    return window.info_dialog(title, message)

def question(window, title='Milk', message='Yes or No?'):
    return window.question_dialog(title, message)

def confirm(window, title='Milk', message='Are you sure you want to?'):
    return window.confirm_dialog(title, message)

def error(window, title='Milk', message='Oops!'):
    return window.error_dialog(title, message)

# def stack_trace(window, message, content, title='Milk',retry=False):
#     return window.stack_trace_dialog(title, message, content, retry)

def open_file(window, title='Open File', initial_directory=None, file_types=None, multiselect=False):
    return window.open_file_dialog(title, initial_directory, file_types, multiselect)

def save_file(window, suggested_filename, title='Save File', file_types=None):
    return window.save_file_dialog(title, suggested_filename, file_types)

def select_folder(window, title='Select Folder', initial_directory=None, multiselect=False):
    return window.select_folder_dialog(title, initial_directory, multiselect)
