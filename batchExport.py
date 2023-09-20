import maya.cmds as cmds
import os

version = "1.0.0"
    
# Browse
def browse(*args):
    selected_folder = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption="Select Folder")
    if selected_folder:
        cmds.textField("folderTextField",e=1,tx=selected_folder[0])  
    else:
        print("No folder selected.")

# Export
def export(*args):
    folder_path = cmds.textField("folderTextField",q=1,text=True)   
    if folder_path=="":
       result = cmds.confirmDialog(title="Error", message="Folder is empty.", button=["OK"], defaultButton="OK")
    elif os.path.exists(folder_path)==False:
       result = cmds.confirmDialog(title="Error", message="Folder dose not exist.", button=["OK"], defaultButton="OK")
    else:
        type = cmds.optionMenu( "exportTypeMenu", q=1, value=True )    
        # get selected objects
        selected_objects = cmds.ls(selection=True)
        index = 0
        for obj in selected_objects:  
            cmds.select(obj)
            obj_name = obj.split("|")[-1]
            filePath = os.path.join(folder_path,obj_name)+"."+type          
            cmds.file(filePath, force=True, type="OBJexport", es=True, options="groups=0;ptgroups=0;materials=0;smoothing=1;normals=1")
            index += 1
            progress_percent = int(index/len(selected_objects)*100.0)                    
            cmds.progressBar("progressBox",e=1,progress=progress_percent) 
            
# UI         
def setupUI(): 
    if cmds.window("batchExportWindow", exists = True):
        cmds.deleteUI("batchExportWindow")
    
    batchExportWindow = cmds.window("batchExportWindow",t="Batch Export "+version,w=300,resizeToFitChildren=1) 
    
    cmds.columnLayout(adjustableColumn=True) 
    cmds.progressBar("progressBox",isInterruptable=True,h=20,maxValue=100) 
    cmds.text(label="", height=5)
  
    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout( numberOfColumns=3, columnWidth3=(50,1,100), columnAttach=[(1, 'left', 0), (2, 'both',0),(3, 'right', 0)],adjustableColumn=2 ) 
    cmds.text(label="Type:",font="boldLabelFont") 
    exportTypeMenu = cmds.optionMenu( "exportTypeMenu", h=26 )
    cmds.menuItem( label='obj' )
    cmds.menuItem( label='fbx' )
    cmds.menuItem( label='abc' )
    cmds.menuItem( label='usd' )
    cmds.setParent("..") 
    
    cmds.columnLayout(adjustableColumn=True) 
    cmds.rowLayout( numberOfColumns=3, columnWidth3=(50,1,1), columnAttach=[(1, 'left', 0), (2, 'both', 0),(3, 'right', 0)],adjustableColumn=2 ) 
    cmds.text(label="Folder:",font="boldLabelFont") 
    cmds.textField("folderTextField",tx="",h=28,font="smallObliqueLabelFont")  
    cmds.button("source_select_btn",label="Browse...",command=browse,w=60,h=24) 
    cmds.setParent("..") 
     
    cmds.text(label="",h=10) 
    
    
    cmds.columnLayout( adjustableColumn=True)
    cmds.button(label="Export",command=export,w=100,h=24) 
    
    cmds.showWindow(batchExportWindow) 
 
# Main
def batchExport():
    setupUI()      

batchExport()