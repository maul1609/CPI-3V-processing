foc_crit=12 # critical value of focus for an image
min_len=100 # minimum length for particle images
dt=10  # resolution on time-step for concentrations (take with a pince of salt)
ds=10  # resolution for size bins
vel=100    # air speed - assumed fixed, used in calcTimeseriesDriver
find_particle_edges=True # output the boundary of the particles
command_line_path=True # use the commandline to define the path of files
process_sweep1_if_exist=True # if the *.roi files have been extracted once,
                              #still do if True
process_roi_driver=True
process_image_stats=True
export_images=True
output_timeseries=True
num_cores=50

path1='/models/mccikpc2/CPI-analysis/C081/3VCPI/'
            # path to raw data
filename1=['20180213065852.roi','20180213092819.roi','20180213055057.roi','20180213060933.roi']
            # list of filenames to process

filename1=['20180213025037.roi']        
        
outputfile='timeseries.mat'


from os import environ
environ["OMP_NUM_THREADS"]="1"
environ["OPENBLAS_NUM_THREADS"]="1"
environ["MKL_NUM_THREADS"]="1"
environ["VECLIB_MAXIMUM_THREADS"]="1"
environ["NUMEXPR_NUM_THREADS"]="1"
import gc
from multiprocessing import set_start_method, Pool, Manager
from multiprocessing.pool import ThreadPool

def runJobs():
    global path1
    global filename1
    # get the files / path from commandline input
    if command_line_path:
        import sys
        path1=sys.argv[1]
        #path1='/Users/mccikpc2/Dropbox (The University of Manchester)/data/'
        #path1='/tmp/test/2DSCPI/'
        from os import listdir
        #from os.path import isfile, join
        filename1 = [f for f in listdir(path1) if f.endswith(".roi")]
        filename1.sort()
        del sys, listdir

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if process_roi_driver:
        from ROIDataDriver import ROIDataDriver
        # extract ROI data from files and prcess with backgrounds
        (t_range)= \
        ROIDataDriver(path1,filename1,dt,process_sweep1_if_exist)
        del ROIDataDriver
        # Garbage collection:
        gc.collect()
        del gc.garbage[:]
    #--------------------------------------------------------------------------

    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if process_image_stats:
        from imageStatsDriver import imageStatsDriver
        # find image properties, edge detection, etc
        imageStatsDriver(path1,filename1,find_particle_edges,num_cores)

        #del imageStatsDriver
    #--------------------------------------------------------------------------


    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if export_images:
        # export images
        from exportImagesDriver import exportImagesDriver
        exportImagesDriver(path1,filename1,foc_crit,min_len)
        del exportImagesDriver
    #--------------------------------------------------------------------------


    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if output_timeseries:
        # calculate number concentrations one day at a time?
        from calcTimeseriesDriver import calcTimeseriesDriver
        calcTimeseriesDriver(path1,filename1,foc_crit,dt,ds,vel,outputfile)
    #--------------------------------------------------------------------------

    

if __name__ == "__main__":


    print("Setting context")
    set_start_method('spawn',force=True)

    #p=Pool(processes=num_cores, maxtasksperchild=1)
    #m = Manager()
    #l = m.Lock()
    
    
    runJobs()


