# plotdata
Scripts to plot GPS, Seismcity abd InSAR data

# Installation
- Set a $SCRATCHDIR environment variable:
```
export SCRATCHDIR=~/Downloads/test
export PLOTDATA_HOME=~/tools
```
- Get the InSAR and GPS data for Hawaii:
```
mkdir -p $SCRATCHDIR
cd $SCRATCHDIR
wget http://149.165.154.65/data/HDF5EOS/MaunaLoa/MaunaLoaSen.tar
tar xvf MaunaLoaSen.tar

mkdir -p MLtry/data
tar xvf GPSdata.tar  -C MLtry/data
wget http://149.165.154.65/data/HDF5EOS/MaunaLoa/GPSdata.tar
```
- Clone code to your tools directory:
```
mkdir -p $PLOTDATA_HOME
git clone https://github.com/geodesymiami/plotdata.git
```
- run testdata:
```
cd $SCRATCHDIR
plot_data.py MaunaLoaSenDT87/mintpy_5_20 MaunaLoaSenAT124/mintpy_5_20 --period 20221127-20221219 --plot-type velocity --ref-point 19.55,-155.45
```
