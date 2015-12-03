#! ./local/bin/python

from vtk import (vtkSphereSource, vtkPolyDataMapper, vtkActor, vtkRenderer,
        vtkRenderWindow, vtkWindowToImageFilter, vtkPNGWriter, vtkVersion, vtkConeSource)


sphereSource = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphereSource.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.SetOffScreenRendering(1)
renderWindow.AddRenderer(renderer)

renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

renderWindow.Render()


windowToImageFilter = vtkWindowToImageFilter()
windowToImageFilter.SetInput(renderWindow)
writer = vtkPNGWriter()
writer.SetInputConnection(windowToImageFilter.GetOutputPort())

for i in xrange(10):
        renderer.GetActiveCamera().Azimuth(10)
        # renderWindow.Render()
        windowToImageFilter.Modified()
        windowToImageFilter.Update()
        writer.SetFileName("sphere_%s.png"%i)
        writer.Write()
