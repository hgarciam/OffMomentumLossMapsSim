import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import linecache
import scipy.io
import glob
import operator
import sys
from matplotlib import rc

rc('text', usetex=True)
rc('xtick', labelsize=24) 
rc('ytick', labelsize=24)
 
## WARM LHC REGIONS (can be put into an external file, but for convenience we leave it here)
 
lhc_warm=np.array([[  0.00000000e+00,   2.25365000e+01],
       [  5.48530000e+01,   1.52489000e+02],
       [  1.72165500e+02,   1.92400000e+02],
       [  1.99484700e+02,   2.24300000e+02],
       [  3.09545428e+03,   3.15562858e+03],
       [  3.16774008e+03,   3.18843308e+03],
       [  3.21144458e+03,   3.26386758e+03],
       [  3.30990008e+03,   3.35497408e+03],
       [  3.40100558e+03,   3.45342858e+03],
       [  3.47644008e+03,   3.49406558e+03],
       [  3.50588528e+03,   3.56831858e+03],
       [  6.40540880e+03,   6.45791380e+03],
       [  6.46877850e+03,   6.85951380e+03],
       [  6.87037850e+03,   6.92353380e+03],
       [  9.73590702e+03,   9.82473052e+03],
       [  9.83083202e+03,   9.86173052e+03],
       [  9.87873202e+03,   9.93998552e+03],
       [  9.95054802e+03,   1.00434620e+04],
       [  1.00540245e+04,   1.01152780e+04],
       [  1.01322795e+04,   1.01639705e+04],
       [  1.01700720e+04,   1.02576030e+04],
       [  1.31049892e+04,   1.31298045e+04],
       [  1.31368892e+04,   1.31571237e+04],
       [  1.31768002e+04,   1.32716472e+04],
       [  1.33067527e+04,   1.33518257e+04],
       [  1.33869312e+04,   1.34817782e+04],
       [  1.35014547e+04,   1.35227845e+04],
       [  1.35298692e+04,   1.35546845e+04],
       [  1.63946378e+04,   1.64508713e+04],
       [  1.64569728e+04,   1.64872713e+04],
       [  1.64933728e+04,   1.68308713e+04],
       [  1.68369728e+04,   1.68672713e+04],
       [  1.68733728e+04,   1.69282948e+04],
       [  1.97348504e+04,   1.97606997e+04],
       [  1.97715644e+04,   2.02179087e+04],
       [  2.02287734e+04,   2.02529744e+04],
       [  2.30899797e+04,   2.31385770e+04],
       [  2.31503967e+04,   2.31713755e+04],
       [  2.31943870e+04,   2.32468100e+04],
       [  2.32928425e+04,   2.33379155e+04],
       [  2.33839480e+04,   2.34363710e+04],
       [  2.34593825e+04,   2.34800825e+04],
       [  2.34921940e+04,   2.35531160e+04],
       [  2.64334879e+04,   2.64583032e+04],
       [  2.64653879e+04,   2.64867177e+04],
       [  2.65063942e+04,   2.66012412e+04],
       [  2.66363467e+04,   2.66588832e+04]])
 
hllhc_warm=np.array([[  0.00000000e+00,   2.25000000e+01],
       [  8.31530000e+01,   1.36689000e+02],
       [  1.82965500e+02,   2.01900000e+02],
       [  2.10584700e+02,   2.24300000e+02],
       [  3.09545428e+03,   3.15562858e+03],
       [  3.16774008e+03,   3.18843308e+03],
       [  3.21144458e+03,   3.26386758e+03],
       [  3.30990008e+03,   3.35497408e+03],
       [  3.40100558e+03,   3.45342858e+03],
       [  3.47644008e+03,   3.49406558e+03],
       [  3.50588528e+03,   3.56831858e+03],
       [  6.40540880e+03,   6.45791380e+03],
       [  6.46877850e+03,   6.85951380e+03],
       [  6.87037850e+03,   6.92353380e+03],
       [  9.73590702e+03,   9.82473052e+03],
       [  9.83083202e+03,   9.86173052e+03],
       [  9.87873202e+03,   9.93998552e+03],
       [  9.95054802e+03,   1.00434620e+04],
       [  1.00540245e+04,   1.01152780e+04],
       [  1.01322795e+04,   1.01639705e+04],
       [  1.01700720e+04,   1.02576030e+04],
       [  1.31036000e+04,   1.31200300e+04],
       [  1.31238892e+04,   1.31471237e+04],
       [  1.31918002e+04,   1.32476472e+04],
       [  1.33067940e+04,   1.33520892e+04],
       [  1.34110312e+04,   1.34670082e+04],
       [  1.35114547e+04,   1.35357845e+04],
       [  1.35388592e+04,   1.35552845e+04],
       [  1.63946378e+04,   1.64508713e+04],
       [  1.64569728e+04,   1.64872713e+04],
       [  1.64933728e+04,   1.68308713e+04],
       [  1.68369728e+04,   1.68672713e+04],
       [  1.68733728e+04,   1.69282948e+04],
       [  1.97348504e+04,   1.97606997e+04],
       [  1.97715644e+04,   2.02179087e+04],
       [  2.02287734e+04,   2.02529744e+04],
       [  2.30899797e+04,   2.31385770e+04],
       [  2.31503967e+04,   2.31713755e+04],
       [  2.31943870e+04,   2.32468100e+04],
       [  2.32928425e+04,   2.33379155e+04],
       [  2.33839480e+04,   2.34363710e+04],
       [  2.34593825e+04,   2.34800825e+04],
       [  2.34921940e+04,   2.35531160e+04],
       [  2.64334879e+04,   2.64483032e+04],
       [  2.64569832e+04,   2.64759232e+04],
       [  2.65221932e+04,   2.65757332e+04],
       [  2.66363832e+04,   2.66588832e+04]])
 
 
# USER INPUT
 
pathtosim       = "../run*/"             # directories where data are stored
pathtoLPIs      = pathtosim+"LP*_BLP_out.s"
pathtoCollSum   = pathtosim+"coll_summary.dat"
SimulationName  = "Loss map LHC 2017"     # title of the simulation
collPosFileName = '../clean_input/CollPositions.b1.dat' # Collimator List (mandatory!)
dataFileName    = 'losses.dat'           # name of file where to save data
dataFileName    = None           # set it to None in case you don't want data to be saved in a file
beam4 = False
b4inB1RefSys = False
plotCounts = False
clhc = 26658.8832 # [m]
# in case lattices do not start at IP1, set this value to the original value of the
#    starting element as if IP1 was at 0.0
# NB: in case of B4, do not put here the value in the B1 ref sys
s0 = 0.0          # [m]
 
warm_parts=lhc_warm
 
##################################### INITIALIZATION #########################################################

print "Initialization..." 
 
## Collimator List (mandatory!)
 
copos=np.loadtxt(collPosFileName,dtype='str') 
 
if ( beam4 ):
    # B4: invert s-coordinate
    for j in range(len(warm_parts)):
        tmpMin = clhc-warm_parts[j,1]
        tmpMax = clhc-warm_parts[j,0]
        warm_parts[j,0] = tmpMin
        warm_parts[j,1] = tmpMax
    warm_parts = warm_parts[::][::-1]
 
 
##################################### PROCESSING OF APERTURE LOSSES ###########################################
 
print "Aperture losses..." 

######## SIMULATION 1
 
simu1ap = []
# aperture losses
for fname in glob.glob(pathtoLPIs):                          # loop over directories
    array=np.loadtxt(fname,ndmin=2)                          # ndmin=2: minimum 2 dimensions (single line files)
    if len(array)!=0:
        simu1ap.append(array[:,2])
simu1ap=[item for sublist in simu1ap for item in sublist]    # flatten array
 
if ( s0 != 0.0 ):
    for ii in range( len( simu1ap ) ):
        simu1ap[ii]+=s0
        if ( simu1ap[ii] > clhc ):
            simu1ap[ii]-=clhc
 
 
######## DIVIDE INTO COLD AND WARM LOSSES

losses_cluster1 = []
losses_cluster2 = []
count_losses_cluster1 = 0
count_losses_cluster2 = 0

aplosses = simu1ap

ap_losses_wc = np.zeros(shape=(len(aplosses),2))
 
for i in range(len(ap_losses_wc)):
    mark = 0
    for j in range(len(warm_parts)):
        if (warm_parts[j,0] < aplosses[i] and aplosses[i] < warm_parts[j,1]):
            mark = 1
    ap_losses_wc[i] = [aplosses[i],mark]
    if (ap_losses_wc[i][0] > 6930.0 and ap_losses_wc[i][0] < 7020.0):
	count_losses_cluster1 += 1
    if (ap_losses_wc[i][0] > 7020.0 and ap_losses_wc[i][0] < 7110.0):
	count_losses_cluster2 += 1

ap_losses_cold = []
ap_losses_warm = []
 
 
for i in range(len(ap_losses_wc)):
    if (ap_losses_wc[i,1] == 0):
        ap_losses_cold.append(ap_losses_wc[i,0])
    else:
        ap_losses_warm.append(ap_losses_wc[i,0])
 
ap_losses_cold1=ap_losses_cold
ap_losses_warm1=ap_losses_warm
 
ApertureLossesColdSample1=len(ap_losses_cold)
ApertureLossesWarmSample1=len(ap_losses_warm)
 

#### COLLIMATOR LOSSES
print "Printing collimator losses..." 
simu1co = []
totcollosses1=0                                                           # total # of lost particles at collim
for j in range(1,len(copos)):
    simu1co.append([int(copos[j][0]),float(copos[j][2]),0,0])

for fname in glob.glob(pathtoCollSum):
    array=np.loadtxt(fname,dtype='str')
    for j in range(len(array)):
        id=np.where(int(array[j][0])==np.array(simu1co)[:,0])[0][0]
        simu1co[id][2] = simu1co[id][2] + int(array[j][3])
        simu1co[id][3] = float(array[j][6])                               # write collimator length

        totcollosses1+=int(array[j][3])                                   # increase total lossnumber

#print len(simu1co)
#for k in range(1,len(simu1co)):
#    print simu1co[k][1], simu1co[k][2], simu1co[k][3]

#print simu1co[3][:]
#print simu1co[0][3]
#print simu1co[1][3]
#print simu1co[2][3]
#print simu1co[3][3]
################################## PLOT #################################
 

#### CREATE HISTOGRAM DATA
print "Creating histograms..."  

fig, (ax0) = plt.subplots(figsize=(12,7))
 
nbins=int(clhc/0.10)
if ( plotCounts ):
    ymax = 1.0E+08
    ymin = 0.1
else:
    ymax = 3.0
    ymin = 1.0E-07
# bar width=80% of bin width
width=0.80*clhc/nbins
binWidth=clhc/nbins
# total number of tracked particles
normfac = float(totcollosses1+ApertureLossesColdSample1+ApertureLossesWarmSample1)                
print ""           
print "Total losses along the ring =", normfac
print "Fraction of losses in collimators =", totcollosses1/normfac*100, "%"
print "Fraction of losses in cold regions =", ApertureLossesColdSample1/normfac*100, "%"
print "Fraction of losses in warm regions =", ApertureLossesWarmSample1/normfac*100, "%"
print "Losses in cluster 1 =", count_losses_cluster1/normfac*100, "%"
print "Losses in cluster 2 =", count_losses_cluster2/normfac*100, "%"
print "" 
 
## Cold Losses
 
#  - Generate histogram
hist_cold, bins = np.histogram(ap_losses_cold1, bins=nbins,range=(0,clhc))
#  - Remove empty entries
bins_cold = np.delete((bins[:-1] + bins[1:]) / 2,np.where(hist_cold==0)[0])
if ( plotCounts ):
    hist_cold = np.delete(hist_cold,np.where(hist_cold==0)[0])
else:
    hist_cold = np.delete(hist_cold,np.where(hist_cold==0)[0])/(binWidth*normfac)
#  - B4 ref system
if ( b4inB1RefSys ):
    bins_cold = clhc-bins_cold
#  - lossmap of cold elements
ax0.bar(bins_cold, hist_cold, width=width , color='dodgerblue', edgecolor='dodgerblue', label='Cold')
 
 
## Warm Losses
 
#  - Generate histogram
hist_warm, bins = np.histogram(ap_losses_warm1, bins=nbins,range=(0,clhc))
#  - Remove empty entries
bins_warm = np.delete( (bins[:-1] + bins[1:]) / 2, np.where(hist_warm==0)[0])
if ( plotCounts ):
    hist_warm = np.delete(hist_warm,np.where(hist_warm==0)[0])
else:
    hist_warm = np.delete(hist_warm,np.where(hist_warm==0)[0])/(binWidth*normfac)
#  - B4 ref system
if ( b4inB1RefSys ):
    bins_warm = clhc-bins_warm
#  - lossmap of warm elements
ax0.bar(bins_warm, hist_warm, width=width , color='orangered', edgecolor='orangered', label='Warm')
 
 
## Collimator Losses
#  - hack to get the correct label

if ( plotCounts ):
    ax0.bar(simu1co[0][1], simu1co[0][2], width=simu1co[0][3] , color='black', edgecolor='black', label='Collimator')
else:
    ax0.bar(simu1co[0][1], simu1co[0][2]/(normfac*simu1co[0][3]), width=simu1co[0][3] , color='black', edgecolor='black', label='Collimator')
#    ax0.bar(simu1co[0][1], simu1co[0][2]/(normfac*0.1), width=0.1 , color='black', edgecolor='black', label='Collimator')
#  - B4 ref system
if ( b4inB1RefSys ):
    for k in range(len(simu1co)):
        simu1co[k][1]=clhc-simu1co[k][1]
#  - lossmap of collimators
if ( plotCounts ):
    for k in range(1,len(simu1co)):
        if ( simu1co[k][3] > 0.0 ):
            ax0.bar(simu1co[k][1], simu1co[k][2], width=simu1co[k][3] , color='black', edgecolor='black')
else:
    for k in range(1,len(simu1co)):
        if ( simu1co[k][3] > 0.0 ):
            ax0.bar(simu1co[k][1], simu1co[k][2]/(normfac*simu1co[k][3]), width=simu1co[k][3] , color='black', edgecolor='black')
 
 
## PLOT PROPERTIES
 
ax0.set_yscale('log', nonposy='clip')
ax0.set_xlim(0,clhc)
ax0.set_ylim(ymin,ymax)
ax0.set_xlabel(r'$s$ [m]',fontsize=22)
if ( plotCounts ):
    ax0.set_ylabel(r'counts ()',fontsize=22)
else:
    ax0.set_ylabel(r'Local cleaning inefficiency $\eta$ (1/m)',fontsize=22)
ax0.xaxis.grid(True)
ax0.yaxis.grid(False)
ax0.grid()

plt.xlim(6400,7300)
ax0.legend(fontsize = 20, loc=1)
plt.savefig('LM_LHC_IR3.png')

plt.xlim(0,27000)
ax0.text(500, 3e-1, 'IP1', fontsize=22)
ax0.text(3300, 3e-1, 'IP2', fontsize=22)
ax0.text(6700, 3e-1, 'IP3', fontsize=22)
ax0.text(9500, 3e-1, 'IP4', fontsize=22)
ax0.text(12500, 3e-1, 'IP5', fontsize=22)
ax0.text(16000, 3e-1, 'IP6', fontsize=22)
ax0.text(19500, 3e-1, 'IP7', fontsize=22)
ax0.text(23000, 3e-1, 'IP8', fontsize=22)

#ax0.legend(fontsize = 18, loc=1, borderaxespad=0.)
ax0.legend(fontsize = 18, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=3, mode="expand", borderaxespad=0.)
#ax0.set_title(SimulationName)
 
# save plot
#$plt.savefig('LM_LHC.png',bbox_inches='tight')
plt.savefig('LM_LHC.png')

 
plt.show()
 
# in case, save data in txt file:
if ( dataFileName is not None ):
    print ' saving histograms in file %s ...' % ( dataFileName )
    oFile = open( dataFileName, 'w' )
    oFile.write( '# normalisation: %i \n' % ( normfac ) )
    oFile.write( '# cold/warm nbins, bin width [m]: %i %.8e \n' % ( nbins, binWidth ) )
    #
    oFile.write( '\n\n' )
    oFile.write( '# cold losses - total: %i \n' % ( ApertureLossesColdSample1 ) )
    if ( plotCounts ):
        oFile.write( '# s_mean [m], counts [] \n' )
        for tmpBin,tmpVal in zip(bins_cold,hist_cold):
            oFile.write( '%13.4f %13i \n' % (tmpBin,tmpVal) )
    else:
        oFile.write( '# s_mean [m], pdf [m-1] \n' )
        for tmpBin,tmpVal in zip(bins_cold,hist_cold):
            oFile.write( '%13.4f %13.4E \n' % (tmpBin,tmpVal) )
    #
    oFile.write( '\n\n' )
    oFile.write( '# warm losses - total: %i \n' % ( ApertureLossesWarmSample1 ) )
    if ( plotCounts ):
        oFile.write( '# s_mean [m], counts [] \n' )
        for tmpBin,tmpVal in zip(bins_warm,hist_warm):
            oFile.write( '%13.4f %13i \n' % (tmpBin,tmpVal) )
    else:
        oFile.write( '# s_mean [m], pdf [m-1] \n' )
        for tmpBin,tmpVal in zip(bins_warm,hist_warm):
            oFile.write( '%13.4f %13.4E \n' % (tmpBin,tmpVal) )
    #
    oFile.write( '\n\n' )
    oFile.write( '# collimator losses - total: %i \n' % ( totcollosses1 ) )
    if ( plotCounts ):
        oFile.write( '# s_min [m], s_max[m], counts [] \n' )
        for k in range(len(simu1co)):
            if ( simu1co[k][3] > 0.0 ):
                oFile.write( '%13.4f %13.4f %13i \n' % (
                    simu1co[k][1]-0.5*simu1co[k][3], simu1co[k][1]+0.5*simu1co[k][3], simu1co[k][2] ) )
    else:
        oFile.write( '# s_min [m], s_max[m], pdf [m-1] \n' )
        for k in range(len(simu1co)):
            if ( simu1co[k][3] > 0.0 ):
                oFile.write( '%13.4f %13.4f %13.4E \n' % (
                    simu1co[k][1]-0.5*simu1co[k][3], simu1co[k][1]+0.5*simu1co[k][3], simu1co[k][2]/(normfac*simu1co[k][3] ) ) )
    #
    oFile.close()
 
# done
print '...done.'
