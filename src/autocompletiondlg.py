# -*- coding: utf-8 -*-
import gutil
import misc
import util

import wx
# 다이어로그 형태로 보여주는 자동완성
# 이 부분은 추후 python 3.x 버전때 wxPython 4.xx 로 바뀔 예정임.
class AutoCompletionDlg(wx.Dialog):
    def __init__(self, parent, autoCompletion):
        wx.Dialog.__init__(self, parent, -1, u"자동완성",
                           style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.autoCompletion = autoCompletion
        # 다이얼로그 값들 정함.
        vsizer = wx.BoxSizer(wx.VERTICAL) 

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        hsizer.Add(wx.StaticText(self, -1, u"요소:"), 0,
                   wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        
        self.elementsCombo = wx.ComboBox(self, -1, style = wx.CB_READONLY)

        for t in autoCompletion.types.itervalues():
            self.elementsCombo.Append(t.ti.name, t.ti.lt)

        wx.EVT_COMBOBOX(self, self.elementsCombo.GetId(), self.OnElementCombo)

        hsizer.Add(self.elementsCombo, 0)

        vsizer.Add(hsizer, 0, wx.EXPAND)

        vsizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        self.enabledCb = wx.CheckBox(self, -1, u"자동완성 활성화")
        wx.EVT_CHECKBOX(self, self.enabledCb.GetId(), self.OnMisc)
        vsizer.Add(self.enabledCb, 0, wx.BOTTOM, 10)

        vsizer.Add(wx.StaticText(self, -1, u"기본 아이템:"))

        self.itemsEntry = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE |
                                      wx.TE_DONTWRAP, size = (400, 200))
        wx.EVT_TEXT(self, self.itemsEntry.GetId(), self.OnMisc)
        vsizer.Add(self.itemsEntry, 1, wx.EXPAND)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        hsizer.Add((1, 1), 1)

        cancelBtn = gutil.createStockButton(self, u"취소")
        hsizer.Add(cancelBtn, 0, wx.LEFT, 10)

        okBtn = gutil.createStockButton(self, u"확인")
        hsizer.Add(okBtn, 0, wx.LEFT, 10)

        vsizer.Add(hsizer, 0, wx.EXPAND | wx.TOP, 10)

        util.finishWindow(self, vsizer)

        self.elementsCombo.SetSelection(0)
        self.OnElementCombo()

        wx.EVT_BUTTON(self, cancelBtn.GetId(), self.OnCancel)
        wx.EVT_BUTTON(self, okBtn.GetId(), self.OnOK)

    def OnOK(self, event):
        self.autoCompletion.refresh()
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnElementCombo(self, event = None):
        self.lt = self.elementsCombo.GetClientData(self.elementsCombo.
                                                     GetSelection())
        t = self.autoCompletion.getType(self.lt)

        self.enabledCb.SetValue(t.enabled)

        self.itemsEntry.Enable(t.enabled)
        self.itemsEntry.SetValue("\n".join(t.items))

    def OnMisc(self, event = None):
        t = self.autoCompletion.getType(self.lt)

        t.enabled = bool(self.enabledCb.IsChecked())
        self.itemsEntry.Enable(t.enabled)

        # this is cut&pasted from autocompletion.AutoCompletion.refresh,
        # but I don't want to call that since it does all types, this does
        # just the changed one.
        tmp = []
        for v in misc.fromGUI(self.itemsEntry.GetValue()).split("\n"):
            v = util.toInputStr(v).strip()

            if len(v) > 0:
                tmp.append(v)

        t.items = tmp
