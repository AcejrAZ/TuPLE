import wx


class slices_example(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                           title=u"Edit slice properties",
                           pos=wx.DefaultPosition, size=wx.Size(-1, 125),
                           style=wx.DEFAULT_DIALOG_STYLE)
        num_opts = ['1', '3', '5', '7', '9', '11', '13', '15']
        self.number = \
            wx.Choice(self, wx.ID_ANY,
                      wx.DefaultPosition, wx.DefaultSize, num_opts, 0)
        self.number.SetSelection(0)
        int_opts = ['0.25', '0.5', '0.75', '1.0', '1.25', '1.5', '1.75', '2.0']
        self.interval = \
            wx.Choice(self, wx.ID_ANY, 
                      wx.DefaultPosition, wx.DefaultSize, int_opts, 0)
        self.interval.SetSelection(0)
        self.number_text = \
            wx.StaticText(self, wx.ID_ANY, u"Number of Slices",
                          wx.DefaultPosition, wx.Size(-1, -1), 0)
        self.interval_text = \
            wx.StaticText(self, wx.ID_ANY, u"Interval (micron)",
                          wx.DefaultPosition, wx.Size(-1, -1), 0)
        self.zrange_text = \
            wx.StaticText(self, wx.ID_ANY, u"Z-Range(micron)",
                          wx.DefaultPosition, wx.Size(-1, -1), 0)
        self.zrange = \
            wx.StaticText(self, wx.ID_ANY, u"0.0",
                          wx.DefaultPosition, wx.Size(-1, -1), 0)
        sizer = wx.GridBagSizer(3, 3)
        sizer.Add(self.number_text, pos=(0,0))
        sizer.Add(self.interval_text, pos=(0,1))
        sizer.Add(self.zrange_text, pos=(0,2))
        sizer.Add(self.number, pos=(1,0))
        sizer.Add(self.interval, pos=(1,1))
        sizer.Add(self.zrange, pos=(1,2))
        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize();
        sizer.Add(m_sdbSizer1, pos=(2,0), span=(1,3), flag=wx.ALIGN_RIGHT)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre(wx.BOTH)
        self.number.Bind(wx.EVT_CHOICE, self._zrange_update)
        self.interval.Bind(wx.EVT_CHOICE, self._zrange_update)

    def _zrange_update(self, event):
        num = int(self.number.GetStringSelection())
        inter = float(self.interval.GetStringSelection())
        zrange = ( num - 1 ) * inter
        self.zrange.SetLabel(str(zrange))

if __name__ == '__main__':
    app = wx.App(False)
    dialog = slices_example(None)
    dialog.Show(True)
    app.MainLoop()
