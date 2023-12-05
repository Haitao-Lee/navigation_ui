import numpy as np

''' CT扫描的测量单位是亨斯菲尔德单位(HU), 这是一种辐射密度的测量。CT扫描仪经过仔细校准 ,以准确地测量这一点。
    为了站在医生的角度看问题, 所以必须将dcm图像的值转换为HU值。'''

def get_pixels_hu(sitkarray, slices):
    #sys.exit(0)
    # print(np.array(slices).shape) #maybe different from 'num'
    [num,w,h] = sitkarray.shape
    #print(sitkarray[0])
    image = np.stack([sitkarray[i] for i in range(num)])
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)
    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    # Convert to Hounsfield units (HU)
    for slice_number in range(num): 
        #print(slices[slice_number].RescaleIntercept,slice_number)  
        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope 
        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)    
        image[slice_number] += np.int16(intercept)
    return np.array(image, dtype=np.int16)