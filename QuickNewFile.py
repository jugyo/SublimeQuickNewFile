import sublime, sublime_plugin
import os
from glob import iglob

class QuickNewFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.start_directory = self.window.folders()[0]
        self.traverse(self.start_directory)

    def traverse(self, directory):
        dirs_and_files = self.find_dirs_and_files(directory)
        if os.path.abspath(directory) != self.start_directory:
            dirs_and_files = [".."] + dirs_and_files

        def on_done(index):
            if index == 0:
                self.new_file(directory)
            elif index >= 1:
                dir = os.path.join(directory, dirs_and_files[index - 1])
                self.traverse(dir)

        items = ['+ New File'] + dirs_and_files

        sublime.set_timeout(lambda: self.window.show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, 1), 1)

    def find_dirs_and_files(self, directory):
        filepaths = [f for f in iglob(os.path.join(directory, '*'))]
        dirs = [os.path.basename(f) + "/" for f in filepaths if os.path.isdir(f)]
        return dirs

    def new_file(self, directory):
        def on_done(text):
            self.window.open_file(os.path.join(directory, text))

        self.window.show_input_panel("File Name:", '', on_done, None, None)