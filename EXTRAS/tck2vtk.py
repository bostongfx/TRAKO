import vtk
import nibabel as nib

#
# Inspired by https://mail.python.org/pipermail/neuroimaging/2019-July/002006.html
# but using Nibabel now for loading (much better!)
#
def convert(input, output, force=True, only_points=True):


    loaded_trk = nib.streamlines.load(input, lazy_load=False)

    streamlines = loaded_trk.streamlines

    polydata = vtk.vtkPolyData()

    lines = vtk.vtkCellArray()
    points = vtk.vtkPoints()

    ptCtr = 0
       
    for i in range(0,len(streamlines)):
        # if((i % 10000) == 0):
        #         print(str(i) + "/" + str(len(streamlines)))
        
        
        line = vtk.vtkLine()
        line.GetPointIds().SetNumberOfIds(len(streamlines[i]))
        for j in range(0,len(streamlines[i])):
            points.InsertNextPoint(streamlines[i][j])
            linePts = line.GetPointIds()
            linePts.SetId(j,ptCtr)
            
            ptCtr += 1
            
        lines.InsertNextCell(line)
                               
    polydata.SetLines(lines)
    polydata.SetPoints(points)

    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(output)
    writer.SetInputData(polydata)
    writer.Write()


