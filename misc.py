import util

import sys

from wxPython.wx import *

def init():
    global isWindows, isUnix, progPath
    
    isWindows = False
    isUnix = False

    if wxPlatform == "__WXMSW__":
        isWindows = True
    else:
        isUnix = True

    if "--test" in sys.argv:
        progPath = "."
    else:
        if isUnix:
            progPath = "/usr/local/blyte"
        else:
            progPath = r"C:\Program Files\Oskusoft\Blyte"

class MyColorSample(wxWindow):
    def __init__(self, parent, id, size):
        wxWindow.__init__(self, parent, id, size = size)

        EVT_PAINT(self, self.OnPaint)

    def OnPaint(self, event):
        dc = wxPaintDC(self)

        w, h = self.GetClientSizeTuple()
        br = wxBrush(self.GetBackgroundColour())
        dc.SetBrush(br)
        dc.DrawRectangle(0, 0, w, h)

# dialog that shows two lists of script names, allowing user to choose one
# from both. stores indexes of selections in members named 'sel1' and
# 'sel2' when OK is pressed. 'items' must have at least two items.
class ScriptChooserDlg(wxDialog):
    def __init__(self, parent, items):
        wxDialog.__init__(self, parent, -1, "Choose scripts",
                          style = wxDEFAULT_DIALOG_STYLE)

        self.SetClientSizeWH(325, 115);
        self.Center()
        
        panel = wxPanel(self, -1)
        
        vsizer = wxBoxSizer(wxVERTICAL)

        gsizer = wxFlexGridSizer(2, 2, 5, 0)

        self.addCombo("first", "Compare script", panel, gsizer, items, 0)
        self.addCombo("second", "to", panel, gsizer, items, 1)

        vsizer.Add(gsizer)

        hsizer = wxBoxSizer(wxHORIZONTAL)

        hsizer.Add(1, 1, 1)
        
        cancelBtn = wxButton(panel, -1, "Cancel")
        hsizer.Add(cancelBtn)
        
        okBtn = wxButton(panel, -1, "OK")
        hsizer.Add(okBtn, 0, wxLEFT, 10)

        vsizer.Add(hsizer, 0, wxEXPAND | wxTOP, 20)

        panel.SetSizer(vsizer)

        vmsizer = wxBoxSizer(wxVERTICAL)
        vmsizer.Add(panel, 1, wxEXPAND | wxALL, 10)
        
        self.SetSizer(vmsizer)

        EVT_BUTTON(self, cancelBtn.GetId(), self.OnCancel)
        EVT_BUTTON(self, okBtn.GetId(), self.OnOK)

    def addCombo(self, name, descr, panel, sizer, items, sel):
        al = wxALIGN_CENTER_VERTICAL | wxRIGHT
        if sel == 1:
            al |= wxALIGN_RIGHT
            
        sizer.Add(wxStaticText(panel, -1, descr), 0, al, 10)
        
        combo = wxComboBox(panel, -1, style = wxCB_READONLY)
        util.setWH(combo, w = 200)
        
        for s in items:
            combo.Append(s)

        combo.SetSelection(sel)
        
        sizer.Add(combo)

        setattr(self, name + "Combo", combo)

    def OnOK(self, event):
        self.sel1 = self.firstCombo.GetSelection()
        self.sel2 = self.secondCombo.GetSelection()
        
        self.EndModal(wxID_OK)

    def OnCancel(self, event):
        self.EndModal(wxID_CANCEL)

# CheckBoxDlg below handles lists of these
class CheckBoxItem:
    def __init__(self, text, selected = True, cdata = None):
        self.text = text
        self.selected = selected
        self.cdata = cdata

    # return dict which has keys for all selected items' client data.
    # takes a list of CheckBoxItem's as its parameter. note: this is a
    # static function.
    def getClientData(cbil):
        tmp = {}
        
        for i in range(len(cbil)):
            cbi = cbil[i]
            
            if cbi.selected:
                tmp[cbi.cdata] = None

        return tmp
    
    getClientData = staticmethod(getClientData)

# shows one or two (one is cbil2 = None) checklistbox widgets with
# contents from cbil1 and possibly cbil2, which are lists of
# CheckBoxItems. size is the size of the dialog as an (x,y) tuple.
# btns[12] are bools for whether or not to include helper buttons.
# port[12] are the portions that the listboxes are given. cdata[12] are
# the optional client data lists. if OK is pressed, the incoming lists'
# items' selection status will be modified.
class CheckBoxDlg(wxDialog):
    def __init__(self, parent, title, size, cbil1, descr1, btns1, port1 = 1,
                 cbil2 = None, descr2 = None, btns2 = None, port2 = None):
        wxDialog.__init__(self, parent, -1, title,
                          style = wxDEFAULT_DIALOG_STYLE)

        self.SetClientSizeWH(*size);
        self.Center()

        panel = wxPanel(self, -1)
        
        vsizer = wxBoxSizer(wxVERTICAL)

        self.cbil1 = cbil1
        self.list1 = self.addList(descr1, panel, vsizer, cbil1, btns1, port1,
                                  True)
        
        if cbil2 != None:
            self.cbil2 = cbil2
            self.list2 = self.addList(descr2, panel, vsizer, cbil2, btns2,
                                      port2, False, 20)

        hsizer = wxBoxSizer(wxHORIZONTAL)

        hsizer.Add(1, 1, 1)
        
        cancelBtn = wxButton(panel, -1, "Cancel")
        hsizer.Add(cancelBtn)
        
        okBtn = wxButton(panel, -1, "OK")
        hsizer.Add(okBtn, 0, wxLEFT, 10)

        vsizer.Add(hsizer, 0, wxEXPAND | wxTOP, 10)

        panel.SetSizer(vsizer)

        vmsizer = wxBoxSizer(wxVERTICAL)
        vmsizer.Add(panel, 1, wxEXPAND | wxALL, 10)
        
        self.SetSizer(vmsizer)

        EVT_BUTTON(self, cancelBtn.GetId(), self.OnCancel)
        EVT_BUTTON(self, okBtn.GetId(), self.OnOK)

        okBtn.SetFocus()
        
    def addList(self, descr, panel, sizer, items, doBtns, portion, isFirst,
                pad = 0):
        sizer.Add(wxStaticText(panel, -1, descr), 0, wxTOP, pad)

        if doBtns:
            hsizer = wxBoxSizer(wxHORIZONTAL)

            if isFirst:
                funcs = [ self.OnSet1, self.OnClear1, self.OnToggle1 ]
            else:
                funcs = [ self.OnSet2, self.OnClear2, self.OnToggle2 ]

            tmp = wxButton(panel, -1, "Set")
            hsizer.Add(tmp)
            EVT_BUTTON(self, tmp.GetId(), funcs[0])

            tmp = wxButton(panel, -1, "Clear")
            hsizer.Add(tmp, 0, wxLEFT, 10)
            EVT_BUTTON(self, tmp.GetId(), funcs[1])

            tmp = wxButton(panel, -1, "Toggle")
            hsizer.Add(tmp, 0, wxLEFT, 10)
            EVT_BUTTON(self, tmp.GetId(), funcs[2])

            sizer.Add(hsizer, 0, wxTOP | wxBOTTOM, 5)
        
        tmp = wxCheckListBox(panel, -1)

        for i in range(len(items)):
            it = items[i]

            tmp.Append(it.text)
            tmp.Check(i, it.selected)
            
        sizer.Add(tmp, portion, wxEXPAND)

        return tmp

    def storeResults(self, cbil, ctrl):
        for i in range(len(cbil)):
            cbil[i].selected = bool(ctrl.IsChecked(i))

    def setAll(self, ctrl, state):
        for i in range(ctrl.GetCount()):
            ctrl.Check(i, state)
        
    def toggle(self, ctrl):
        for i in range(ctrl.GetCount()):
            ctrl.Check(i, not ctrl.IsChecked(i))

    def OnSet1(self, event):
        self.setAll(self.list1, True)
        
    def OnClear1(self, event):
        self.setAll(self.list1, False)
        
    def OnToggle1(self, event):
        self.toggle(self.list1)
        
    def OnSet2(self, event):
        self.setAll(self.list2, True)
        
    def OnClear2(self, event):
        self.setAll(self.list2, False)
        
    def OnToggle2(self, event):
        self.toggle(self.list2)

    def OnOK(self, event):
        self.storeResults(self.cbil1, self.list1)

        if hasattr(self, "list2"):
            self.storeResults(self.cbil2, self.list2)
        
        self.EndModal(wxID_OK)

    def OnCancel(self, event):
        self.EndModal(wxID_CANCEL)
