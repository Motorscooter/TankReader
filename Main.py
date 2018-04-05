# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 12:23:17 2018

@author: scott.downard
"""


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import Mainwindow
from FileRead import *
from bokeh.plotting import figure, output_file, show
from bokeh.models import Legend, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs, DataTable, TableColumn
import bokeh.io as bk
import bokeh.plotting
#Object that runs GUI.
class InflatorApp(QtWidgets.QMainWindow, Mainwindow.Ui_mainwindow):

#Initialize widgets.    
    def __init__(self,parent=None):
        filterlist = ['Raw','60','180']
        unitsList = ['Psi','kPa']
        super(InflatorApp, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnCount(5)        
        self.filterBox.addItems(filterlist)
        self.openFile.clicked.connect(self.browse_folder)
        self.unitBox.addItems(unitsList)        
        self.graphbtn.clicked.connect(self.report)
#        self.export_2.clicked.connect(self.exportexcel)
        self.data_dict = {}        
    def browse_folder(self):        
        directory = QtWidgets.QFileDialog.getOpenFileNames(self,'Select Files to Open',"", 'AIFT Files (*.aift)')        
        dirList = directory[0]
        if directory:
            self.tableWidget.clear()
            self.test_list = []
            
            group_list = []
            tempdata = fileRead(dirList)
            for key in tempdata:
                if key in self.data_dict.keys():
                    self.data_dict[key] = tempdata[key]
                    tempdata.pop(key, None)                    
            self.data_dict.update(tempdata)
             
            for keys in self.data_dict:
                self.test_list.append(keys)
            self.colorList = ['#000000' for x in range(len(self.test_list))]
            for i in range(len(self.test_list)):
                group_list.append(str(i+1))
            self.tableWidget.setRowCount(len(self.test_list))
            self.tableWidget.setHorizontalHeaderLabels(['File Name','Test Name','Group #','Line Color', "Delete"])
            i = 0         
            for k in self.test_list:
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(k)))
                self.tableWidget.item(i,0).setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                header = self.tableWidget.horizontalHeader()
                header.setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
                self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(k)))
                comboBox = QtWidgets.QComboBox()                                   
                comboBox.addItems(group_list)
                comboBox.setCurrentIndex(i)
                self.tableWidget.setCellWidget(i,2,comboBox) 
                self.btncolor = QtWidgets.QPushButton()
                self.btncolor.clicked.connect(self.clickedColor)
                self.btncolor.setStyleSheet("background-color: black")
                self.tableWidget.setCellWidget(i,3,self.btncolor)
                self.btnDel = QtWidgets.QPushButton()
                self.btnDel.clicked.connect(self.deleteData)
                self.btnDel.setText("Remove")
                self.tableWidget.setCellWidget(i,4,self.btnDel)
                i +=1

#Delete unwanted files from dictionary. (Not from folder)
    def deleteData(self):
        button = QtWidgets.qApp.focusWidget()
        index = self.tableWidget.indexAt(button.pos())
        namedel = self.tableWidget.item(index.row(),0).text()
        self.data_dict.pop(namedel,None)
        self.tableWidget.removeRow(index.row())
#Button function for selection color with color picker. 
    def clickedColor(self):
        button = QtWidgets.qApp.focusWidget()
        color = QtWidgets.QColorDialog.getColor()
        button.setStyleSheet("QWidget { background-color: %s}" % color.name())
        index = self.tableWidget.indexAt(button.pos())
        self.colorList[index.row()] = color.name()
        self.data_dict[self.tableWidget.item(index.row(),0).text()]['Color'] = color.name()
    def report(self):
        directory = QtWidgets.QFileDialog.getSaveFileName(self,"Select Where to Save")
        if directory:
            if self.data_dict:
                group_list = []
                
                avgDict = {}
                testLen = len(self.data_dict.keys())
                for i in range(testLen):
                    self.data_dict[self.tableWidget.item(i,0).text()]['Title'] = self.tableWidget.item(i,1).text()
                    self.data_dict[self.tableWidget.item(i,0).text()]['Group'] = int(self.tableWidget.cellWidget(i,2).currentText())
                filtersize = self.filterBox.currentText()
                plotTitle = self.titlebox.text()
                units = self.unitBox.currentText()
                for i in range(len(self.test_list)):
                    group_list.append(self.tableWidget.cellWidget(i,2).currentText())
                groupDict = {i:group_list.count(i) for i in group_list}
                if filtersize != 'Raw':
                    for key in self.data_dict:
                        self.data_dict[key]['YData'] = filterProcessing(self.data_dict[key]['RawYData'],int(filtersize),self.data_dict[key]['Sample Rate'])
                        if units == 'kPa':
                            self.data_dict[key]['YData'] = self.data_dict[key]['YData'] * 6.89476
                            self.data_dict[key]['VertUnits'] = units
                else:
                    for key in self.data_dict:
                        self.data_dict[key]['YData'] = self.data_dict[key]['RawYData']
                for key in self.data_dict:
                    if self.data_dict[key]['Group'] in avgDict:
                      avgDict[self.data_dict[key]['Group']]['XGData'].append(self.data_dict[key]['XData'])
                      avgDict[self.data_dict[key]['Group']]['YGData'].append(self.data_dict[key]['YData'])
                    else:
                      avgDict[self.data_dict[key]['Group']] = {}
                      avgDict[self.data_dict[key]['Group']]['XGData'] = []
                      avgDict[self.data_dict[key]['Group']]['YGData'] = []
                      avgDict[self.data_dict[key]['Group']]['Title'] = self.data_dict[key]['Title']
                      avgDict[self.data_dict[key]['Group']]['Color'] = self.data_dict[key]['Color']
                      avgDict[self.data_dict[key]['Group']]['XGData'].append(self.data_dict[key]['XData'])
                      avgDict[self.data_dict[key]['Group']]['YGData'].append(self.data_dict[key]['YData'])
                      avgDict[self.data_dict[key]['Group']]['Points'] = self.data_dict[key]['NumofPoints']
                      
                avgsumx = 0
                avgsumy = 0
                for key in avgDict:
                    avgDict[key]['avgY'] = []
                    avgDict[key]['avgX'] = []
                    for i in range(avgDict[key]['Points']):
                        for axist in avgDict[key]['XGData']:
                            avgsumx += axist[i]
                        for ayist in avgDict[key]['YGData']:
                            avgsumy += ayist[i]
                        avgx = avgsumx/len(avgDict[key]['XGData'])
                        avgy = avgsumy/len(avgDict[key]['YGData'])
                        avgDict[key]['avgY'].append(avgy)
                        avgDict[key]['avgX'].append(avgx)                        
                        avgsumx = 0
                        avgsumy = 0

# =============================================================================
# Calculate variable for the data table.
#                ttfgList = []
                pmaxList = []
                gtxList = []
                eventList = []
                title = []
                for key in self.data_dict:
#                    ttfgList.append(ttfgCalc(self.data_dict[key]['RawYData'],self.data_dict[key]['XData']))
                    pmaxList.append(pMax(self.data_dict[key]['YData']))
                    gtxList.append(gtx(self.data_dict[key]['YData'],self.data_dict[key]['XData']))
                    eventList.append(eventStart(self.data_dict[key]['YData'],self.data_dict[key]['XData']))
                    title.append(self.data_dict[key]['Title'])
# =============================================================================
                output_file(directory[0]+'.html')
                p1 = figure(width = 1200, height = 600, title = plotTitle)
                legendSet = []
                for key in self.data_dict:
                     a = p1.line(self.data_dict[key]['XData'],self.data_dict[key]['YData'],line_color = self.data_dict[key]['Color'], line_width = 4, alpha = 1, muted_color = self.data_dict[key]['Color'],muted_alpha=0)
                     legendSet.append((self.data_dict[key]['Title'],[a]))
                legend = Legend(items = legendSet, location=(0,0))
                legend.click_policy = "mute"
                p1.add_layout(legend,'right')   
                p1.legend.orientation = "vertical"
                p1.legend.padding = 1
                p1.xaxis.axis_label = "Time (mSec)"
                p1.yaxis.axis_label = "Pressure (" + units +")"
                tab1 = Panel(child=p1, title=plotTitle)

                self.data = dict(TestTitle = title,
#                            TTFG = ttfgList,
                            Gtx = gtxList, MaxPressure = pmaxList,
                            StartofEvent = eventList)
                source = ColumnDataSource(self.data)
                
                columns = [TableColumn(field= "TestTitle", title="Test Name"),
#                           TableColumn(field= "TTFG" ,title="TTFG"),
                           TableColumn(field= "Gtx",title = "Gtx(20-40)"),
                           TableColumn(field = "StartofEvent" ,title = "Start of Event @P10"),
                           TableColumn(field = "MaxPressure", title = "Maximum Pressure")]
                data_table = DataTable(source = source, columns = columns, width = 700, height = 300) 
                tab2 = Panel(child=data_table, title= plotTitle + ' Data Table')
                
                if self.average.isChecked():
                    p2 = figure(width = 1200, height = 600, title = 'Average' + plotTitle)
                    legendSet = []
                    for key in avgDict:
                         b = p2.line(avgDict[key]['avgX'],avgDict[key]['avgY'],line_color = avgDict[key]['Color'], line_width = 4, alpha = 1, muted_color = avgDict[key]['Color'],muted_alpha=0)
                         legendSet.append((avgDict[key]['Title'],[b]))
                    legend = Legend(items = legendSet, location=(0,0))
                    legend.click_policy = "mute"
                    p2.add_layout(legend,'right')   
                    p2.legend.orientation = "vertical"
                    p2.legend.padding = 1
                    p2.xaxis.axis_label = "Time (mSec)"
                    p2.yaxis.axis_label = "Pressure (" + units +")"
                    tab3 =  Panel(child=p2, title='Average '+ plotTitle)
                    tabs = Tabs(tabs = [tab1,tab3,tab2])
                    show(tabs)
                else:
                    tabs = Tabs(tabs=[tab1,tab2])
                    show(tabs)  
                    
                    

        
                                                
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = InflatorApp()
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()