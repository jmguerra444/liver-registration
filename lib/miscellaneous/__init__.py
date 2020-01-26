'''
Some various functions
====
-Later add classes and maybe more stuff
'''

import vtk
from vtk.util import numpy_support

def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
    
    

def dcmread(path):
    """
    Returns the numpy numpy volume for the given path
    Stolen from https://pyscience.wordpress.com/2014/09/08/dicom-in-python-importing-medical-image-data-into-numpy-with-pydicom-and-vtk/
    """

    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(path)
    reader.Update()

    # Load dimensions using `GetDataExtent`
    _extent = reader.GetDataExtent()
    pixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]

    # Load spacing values
    pixelSpacing = reader.GetPixelSpacing()

    # Get the 'vtkImageData' object from the reader
    imageData = reader.GetOutput()
    # Get the 'vtkPointData' object from the 'vtkImageData' object
    pointData = imageData.GetPointData()
    # Ensure that only one array exists within the 'vtkPointData' object
    assert (pointData.GetNumberOfArrays()==1)
    # Get the `vtkArray` (or whatever derived type) which is needed for the `numpy_support.vtk_to_numpy` function
    arrayData = pointData.GetArray(0)
    # Convert the `vtkArray` to a NumPy array
    arrayDicom = numpy_support.vtk_to_numpy(arrayData)
    # Reshape the NumPy array to 3D using 'ConstPixelDims' as a 'shape'
    arrayDicom = arrayDicom.reshape(pixelDims, order='F')
    return arrayDicom