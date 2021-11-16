# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
# from paraview.simple import *
# import os
import numpy as np
import vtk.numpy_interface.dataset_adapter as dsa

# find source
caseName = 'case2_1kk'
case = FindSource(caseName)
reader = GetActiveSource()
times = reader.TimestepValues
# create a new 'Calculator'
calculator1 = Calculator(Input=case)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.ResultArrayName = 'posX'
calculator1.Function = 'coordsX'

# create a new 'Threshold'
threshold1 = Threshold(Input=calculator1)
threshold1.Scalars = ['POINTS', 'posX']
threshold1.ThresholdRange = [-0.03999999910593033, 1.600000023841858]

# Properties modified on threshold1
threshold1.ThresholdRange = [0.05, 1.6]


dataList = []
for i in range(len(times)):
    time = times[i]
    print(time)
    
    T =  0 
    xT = 0 
    zT = 0 
    xxT =0 
    zzT =0 
    xc = 0
    zc = 0

    # create a new 'Python Calculator'
    pythonCalculator1 = PythonCalculator(Input=threshold1)
    # Properties modified on pythonCalculator1
    pythonCalculator1.Expression = '(T - min(T)) / (max(T) - min(T))'
    pythonCalculator1.ArrayName = 'dimT'

    # create a new 'Threshold'
    threshold2 = Threshold(Input=pythonCalculator1)
    threshold2.Scalars = ['POINTS', 'dimT']
    threshold2.ThresholdRange = [0.1, 1]
    
    # create a new 'Calculator'
    calculator2 = Calculator(Input=threshold2)
    # Properties modified on calculator
    calculator2.ResultArrayName = 'xT'
    calculator2.Function = 'coordsX*dimT'
    # create a new 'Calculator'
    calculator3 = Calculator(Input=calculator2)
    # Properties modified on calculator
    calculator3.ResultArrayName = 'zT'
    calculator3.Function = 'coordsZ*dimT'

    # create a new 'Calculator'
    calculator4 = Calculator(Input=calculator3)
    # Properties modified on calculator
    calculator4.ResultArrayName = 'xxT'
    calculator4.Function = 'coordsX*coordsX*dimT'

    # create a new 'Calculator'
    calculator5 = Calculator(Input=calculator4)
    # Properties modified on calculator
    calculator5.ResultArrayName = 'zzT'
    calculator5.Function = 'coordsZ*coordsZ*dimT'

    # create a new 'Integrate Variables'
    integrateVariables1 = IntegrateVariables(Input=calculator5)
    Show(integrateVariables1)
    
    # read integrated emission point
    data = servermanager.Fetch(integrateVariables1)
    data = dsa.WrapDataObject(data)
   
    T = data.PointData['dimT']
    xT = data.PointData['xT']
    zT = data.PointData['zT']
    xxT = data.PointData['xxT']
    zzT = data.PointData['zzT']
    
    xc = xT[0]/T[0]
    zc = zT[0]/T[0]
    
    sigmaX = (xxT[0]-2*xc*xT[0]+xc*xc*T[0])/T[0]
    sigmaZ = (zzT[0]-2*zc*zT[0]+zc*zc*T[0])/T[0]


    # create a new 'Calculator'
    calculator6 = Calculator(Input=threshold2)
    # Properties modified on calculator
    calculator6.ResultArrayName = 'X'
    calculator6.Function = 'coordsX'

    # create a new 'Calculator'
    calculator7 = Calculator(Input=calculator6)
    # Properties modified on calculator
    calculator7.ResultArrayName = 'Y'
    calculator7.Function = 'coordsY'
    
    # create a new 'Calculator'
    calculator8 = Calculator(Input=calculator7)
    # Properties modified on calculator
    calculator8.ResultArrayName = 'Z'
    calculator8.Function = 'coordsZ'

    # create a new 'Python Calculator'
    pythonCalculator2 = PythonCalculator(Input=calculator8)
    # Properties modified on pythonCalculator2
    pythonCalculator2.Expression = 'max(X)'
    pythonCalculator2.ArrayName = 'maxX'
    pythonCalculator2.UpdatePipeline()

    # create a new 'Python Calculator'
    pythonCalculator3 = PythonCalculator(Input=pythonCalculator2)
    # Properties modified on pythonCalculator
    pythonCalculator3.Expression = 'max(Y)'
    pythonCalculator3.ArrayName = 'maxY'
    pythonCalculator3.UpdatePipeline()

    # create a new 'Python Calculator'
    pythonCalculator4 = PythonCalculator(Input=pythonCalculator3)
    # Properties modified on pythonCalculator
    pythonCalculator4.Expression = 'max(Z)'
    pythonCalculator4.ArrayName = 'maxZ'
    pythonCalculator4.UpdatePipeline()
    
    # create a new 'Python Calculator'
    pythonCalculator5 = PythonCalculator(Input=pythonCalculator4)
    # Properties modified on pythonCalculator
    pythonCalculator5.Expression = 'min(Y)'
    pythonCalculator5.ArrayName = 'minY'
    pythonCalculator5.UpdatePipeline()
    
    pythonCalculator6 = PythonCalculator(Input=pythonCalculator5)
    # Properties modified on pythonCalculator
    pythonCalculator6.Expression = 'min(Z)'
    pythonCalculator6.ArrayName = 'minZ'
    pythonCalculator6.UpdatePipeline()
    
    maxX = servermanager.Fetch(pythonCalculator2)
    maxX = dsa.WrapDataObject(maxX)
    maxX = maxX.PointData['maxX']
    maxY = servermanager.Fetch(pythonCalculator3)
    maxY = dsa.WrapDataObject(maxY)
    maxY = maxY.PointData['maxY']
    maxZ = servermanager.Fetch(pythonCalculator4)
    maxZ = dsa.WrapDataObject(maxZ)
    maxZ = maxZ.PointData['maxZ']

    minY = servermanager.Fetch(pythonCalculator5)
    minY = dsa.WrapDataObject(minY)
    minY = minY.PointData['minY']
    minZ = servermanager.Fetch(pythonCalculator6)
    minZ = dsa.WrapDataObject(minZ)
    minZ = minZ.PointData['minZ']
    
    xRange = maxX[0]
    xRange = str(xRange)
    xRange = xRange.replace('[', '').replace(']','')
    yRange = maxY[0] -minY[0]
    yRange = str(yRange)
    yRange = yRange.replace('[', '').replace(']','')
    zRange = maxZ[0] - minZ[0]
    zRange = str(zRange)
    zRange = zRange.replace('[', '').replace(']','')
   
    sd = [time, float(xRange), float(yRange), float(zRange), T[0], xT[0], zT[0], xxT[0], zzT[0], xc, zc, sigmaX, sigmaZ]
    dataList.append(sd)
    print(sd)

    Delete(pythonCalculator6)
    Delete(pythonCalculator5)
    Delete(pythonCalculator4)
    Delete(pythonCalculator3)
    Delete(pythonCalculator2)
    Delete(calculator8)
    Delete(calculator7)
    Delete(calculator6)
    Delete(integrateVariables1)
    Delete(calculator5)
    Delete(calculator4)
    Delete(calculator3)
    Delete(calculator2)
    Delete(calculator2)
    Delete(threshold2)
    Delete(pythonCalculator1)
    # # get animation scene
    animationScene1 = GetAnimationScene()
    
    animationScene1.GoToNext()


np.savetxt('./' + caseName + '.dat', dataList)
### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
