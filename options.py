# Copyright (C) 2010  Alex Yatskov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from PyQt4 import QtGui, QtCore

from image import ImageFlags
from ui.options_ui import Ui_DialogOptions


class DialogOptions(QtGui.QDialog, Ui_DialogOptions):
    def __init__(self, parent, book):
        QtGui.QDialog.__init__(self, parent)
        self.book = book
        self.setupUi(self)
        self.connect(self, QtCore.SIGNAL('accepted()'), self.onAccept)
        self.moveOptionsToDialog()


    def onAccept(self):
        self.moveDialogToOptions()


    def moveOptionsToDialog(self):
        self.lineEditTitle.setText(self.book.title or 'Untitled')
        self.comboBoxDevice.setCurrentIndex(max(self.comboBoxDevice.findText(self.book.device), 0))
        self.checkboxOverwrite.setChecked(self.book.overwrite)
        self.checkboxOrient.setChecked(self.book.imageFlags & ImageFlags.Orient)
        self.checkboxResize.setChecked(self.book.imageFlags & ImageFlags.Resize)
        self.checkboxQuantize.setChecked(self.book.imageFlags & ImageFlags.Quantize)
        self.checkboxFrame.setChecked(self.book.imageFlags & ImageFlags.Frame)


    def moveDialogToOptions(self):
        title = self.lineEditTitle.text()
        device = self.comboBoxDevice.itemText(self.comboBoxDevice.currentIndex())
        overwrite = self.checkboxOverwrite.isChecked()

        imageFlags = 0
        if self.checkboxOrient.isChecked():
            imageFlags |= ImageFlags.Orient
        if self.checkboxResize.isChecked():
            imageFlags |= ImageFlags.Resize
        if self.checkboxQuantize.isChecked():
            imageFlags |= ImageFlags.Quantize
        if self.checkboxFrame.isChecked():
            imageFlags |= ImageFlags.Frame

        modified = (
            self.book.title != title or
            self.book.device != device or
            self.book.overwrite != overwrite or
            self.book.imageFlags != imageFlags
        )

        if modified:
            self.book.modified = True
            self.book.title = title
            self.book.device = device
            self.book.overwrite = overwrite
            self.book.imageFlags = imageFlags
