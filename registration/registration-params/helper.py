from utils import getData, log, screenshot, now, absolutePath
from shutil import copy
import os
import itertools
import h5py
import numpy as np
# local/our imports
import pystrum.pynd.ndutils as nd

def generateGrid(d):
    if (d == {}):
            return [""]

    result = []
    key = lambda x : list(d.keys())[x]
    
    p0 = p1 = p2 = p3 = p4 = ''
    l = len(d)

    for a0 in d[key(0)]:
        p0 = '{}="{}" '.format(key(0), a0)
        if l == 1 : result.append(p0)
        
        if l > 1:
            for a1 in d[key(1)]:
                p1 = '{}="{}" '.format(key(1), a1)
                if l == 2 : result.append(p0 + p1)

                if l > 2:
                    for a2 in d[key(2)]:
                        p2 = '{}="{}" '.format(key(2), a2)
                        if l == 3 : result.append(p0 + p1 + p2)

                        if l > 3:
                            for a3 in d[key(3)]:
                                p3 = '{}="{}" '.format(key(3), a3)
                                if l == 4 : result.append(p0 + p1 + p2 + p3)
                            
                                if l > 4:
                                    for a4 in d[key(4)]:
                                        p4 = '{}="{}" '.format(key(4), a4)
                                        result.append(p0 + p1 + p2 + p3 + p4)
    return result

def crop(limit):
    # Cuts from lower to upper slice, the slices in the range will be removed
    return "0 0 {}".format(limit)


def moveLandmarks(landmarks, translation):
    
    # Later do substraction to move it down if required

    points = [float(x) for x in landmarks.split()]
    tz = [float(x) for x in translation.split()]

    movedLandmarks = ""

    # tz = [33, 0, 0]
    for i in range(int(len(points) / 3)):
        movedLandmarks = movedLandmarks  + "  " \
                + str(tz[0] - points[i * 3 + 0]) + "    " \
                + str(tz[1] - points[i * 3 + 1]) + "    " \
                + str(tz[2] - points[i * 3 + 2])
    
    return movedLandmarks

def setup(study):
    # Make dirs
    os.makedirs(study.get("screenshotFolder"), exist_ok = True)
    os.makedirs(study.get("deformationsFolder"), exist_ok = True)
    
    # Add description
    log(study.get("workspaceFile"), study.get("descriptionFile"))
    log(study.get("description"), study.get("descriptionFile"))

    # Copy workspacefile
    copy(study.get("workspaceFile"), study.get("studyFolder"))

def filterLandmarks(landmarks, best):
    
    if not best:
        return landmarks
    
    new_landmarks = {}
    for p in landmarks:
        if (int(p) in best):
            new_landmarks[p] = landmarks[p]       
    
    return new_landmarks

def getSpecificGrid(key):

    grid = [""]

    if (key == "FFD_ADV"):
        grid = [
            'similarity="NCC" step_size="15" grid_size="5 5 5" smoothness="0" ',
            'similarity="NCC" step_size="10" grid_size="7 7 5" smoothness="0.001" ',
            'similarity="NCC" step_size="15" grid_size="7 7 5" smoothness="0" ',
            'similarity="SSD" step_size="15" grid_size="7 7 5" smoothness="0" ',
            'similarity="SSD" step_size="5" grid_size="5 5 5" smoothness="0" ',
            'similarity="LNCC" stepsize="10" grid_size="3 3 3" smoothness="0.001"',
            'similarity="MI" stepsize="5" grid_size="5 5 5" smoothness="0"'
        ]
    
    if (key == "DEA_ADV"):
        grid = [""]

    return grid

def getSpecificPatients(landmarks):
    lmks = landmarks.copy()
    selectedPatients =  ["008", "022", "036", "037", "040", "041", "046", "050", "056", "062", "067", "070", "075", "078", "079", "091", "094"]
    for l in landmarks:
        if not(l in selectedPatients):
            del(lmks[l])
    return lmks

def jacobian_determinant(disp):
    """
    jacobian determinant of a displacement field.
    NB: to compute the spatial gradients, we use np.gradient.

    Parameters:
        disp: 2D or 3D displacement field of size [*vol_shape, nb_dims],
              where vol_shape is of len nb_dims

    Returns:
        jacobian determinant (scalar)
    """

    # check inputs
    volshape = disp.shape[:-1]
    nb_dims = len(volshape)
    assert len(volshape) in (2, 3), 'flow has to be 2D or 3D'

    # compute grid
    grid_lst = nd.volsize2ndgrid(volshape)
    grid = np.stack(grid_lst, len(volshape))

    # compute gradients
    J = np.gradient(disp + grid)

    # 3D glow
    if nb_dims == 3:
        dx = J[0]
        dy = J[1]
        dz = J[2]
        # compute jacobian components
        Jdet0 = dx[..., 0] * (dy[..., 1] * dz[..., 2] - dy[..., 2] * dz[..., 1])
        Jdet1 = dx[..., 1] * (dy[..., 0] * dz[..., 2] - dy[..., 2] * dz[..., 0])
        Jdet2 = dx[..., 2] * (dy[..., 0] * dz[..., 1] - dy[..., 1] * dz[..., 0])
        return Jdet0 - Jdet1 + Jdet2

    else:
        # must be 2
        dfdx = J[0]
        dfdy = J[1]
        return dfdx[..., 0] * dfdy[..., 1] - dfdy[..., 0] * dfdx[..., 1]

def fieldInversability(filename):
    hf = h5py.File(filename, 'r')
    displacement = np.array(hf["Deformation field"][:])
    displacement = np.squeeze(displacement)
    displacement = np.transpose(displacement)
    det = jacobian_determinant(displacement)
    r = np.sum(det <= 0) / np.prod(det.shape)
    return r

def paramsToString(params):
    params = params.replace(" ", "_")
    params = params.replace("=", "_")
    params = params.replace('"', "")
    return params
