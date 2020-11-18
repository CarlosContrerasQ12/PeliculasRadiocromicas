import numpy as np
import matplotlib.pyplot as plt
from pydicom import dcmread
import SimpleITK as sitk

def display_images(fixed_image_z, moving_image_z, fixed_npa, moving_npa):
    # Create a figure with two subplots and the specified size.
    plt.subplots(1,2,figsize=(10,8))
    
    # Draw the fixed image in the first subplot.
    plt.subplot(1,2,1)
    plt.imshow(fixed_npa[fixed_image_z,:,:],cmap=plt.cm.Greys_r);
    plt.title('fixed image')
    plt.axis('off')
    
    # Draw the moving image in the second subplot.
    plt.subplot(1,2,2)
    plt.imshow(moving_npa[moving_image_z,:,:],cmap=plt.cm.Greys_r);
    plt.title('moving image')
    plt.axis('off')
    
    plt.show()
    
def display_images_with_alpha(image_z, alpha, fixed, moving):
    img = (1.0 - alpha)*fixed[:,:,image_z] + alpha*moving[:,:,image_z] 
    plt.imshow(sitk.GetArrayViewFromImage(img),cmap=plt.cm.Greys_r);
    plt.axis('off')
    plt.show()
    
    
def start_plot():
    global metric_values, multires_iterations
    
    metric_values = []
    multires_iterations = [] 
    
    
# Callback invoked when the EndEvent happens, do cleanup of data and figure.
def end_plot():
    global metric_values, multires_iterations
    
    del metric_values
    del multires_iterations
    # Close figure, we don't want to get a duplicate of the plot latter on.
    plt.close()
    
#fig,ax=plt.subplots()
#line1,=ax.plot([],[], 'b*')    
#line2,=ax.plot([],'r')    
def plot_values(registration_method):
    global metric_values, multires_iterations
    
    metric_values.append(registration_method.GetMetricValue())                                       
    # Clear the output area (wait=True, to reduce flickering), and plot current data
    # Plot the similarity metric values
    #plt.plot(metric_values, 'r')
    #line2.set_data(metric_values)
    #line1.set_data(multires_iterations, [metric_values[index] for index in multires_iterations], 'b*')
    #fig.canvas.draw()
    #fig.canvas.flush_events()
    #plt.xlabel('Iteration Number',fontsize=12)
    #plt.ylabel('Metric Value',fontsize=12)
    #plt.show()
    
def update_multires_iterations():
    global metric_values, multires_iterations
    multires_iterations.append(len(metric_values))
    
mapaDosis1=np.load("PiramideDosis.npy") 
mapaDosis1=mapaDosis1/4.5   
ds = dcmread('piramide2.dcm')
mapaDosis2=ds.pixel_array/np.max(ds.pixel_array)   
fixed_image =  sitk.GetImageFromArray(mapaDosis2)
moving_image = sitk.GetImageFromArray(mapaDosis1)

initial_transform = sitk.CenteredTransformInitializer(fixed_image, 
                                                      moving_image, 
                                                      sitk.Euler2DTransform(), 
                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)

moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

registration_method = sitk.ImageRegistrationMethod()

registration_method.SetMetricAsMeanSquares()
registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
registration_method.SetMetricSamplingPercentage(0.01)
registration_method.SetInterpolator(sitk.sitkLinear)

registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
registration_method.SetOptimizerScalesFromPhysicalShift()

registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [4,2,1])
registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

registration_method.SetInitialTransform(initial_transform, inPlace=False)

registration_method.AddCommand(sitk.sitkStartEvent, start_plot)
registration_method.AddCommand(sitk.sitkEndEvent, end_plot)
registration_method.AddCommand(sitk.sitkMultiResolutionIterationEvent, update_multires_iterations) 
registration_method.AddCommand(sitk.sitkIterationEvent, lambda: plot_values(registration_method))

final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32), 
                                               sitk.Cast(moving_image, sitk.sitkFloat32))
imas=sitk.GetArrayFromImage(moving_resampled)  
plt.imshow(imas,cmap=plt.cm.gray)
plt.figure()
plt.imshow(mapaDosis2,cmap=plt.cm.gray)
plt.show()                                            
sitk.WriteImage(moving_resampled, 'movida.mha')
sitk.WriteTransform(final_transform, 'trnadoras.tfm')
