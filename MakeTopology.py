#!/usr/bin/python

import wx

import wx
class MyFrame(wx.Frame):

    def __init__(self, parent=None, id=-1, title='MyTopology', name='TopFrame'):
        super(MyFrame, self).__init__(parent, id, title, name=name)




class MyApp(wx.App):
    def __init__(self, redirect=False, filename=None):
        super(MyApp, self).__init__(redirect, filename)

    def OnInit(self):
        self.frame = MyFrame(parent=None, id=-1, title='MakeTopology   by FortiADC QA', name='TopFrame')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        pass


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()













