# plotdata
Scripts to plot GPS, Seismcity abd InSAR data

# Installation
- Set a $SCRATCHDIR environment variable (required):
```
export SCRATCHDIR=~/Downloads/test
```
- Get the InSAR, GPS data and clone the repo:
```
mkdir $SCRATCHDIR
cd $SCRATCHDIR
wget http://149.165.154.65/data/HDF5EOS/MaunaLoa/MaunaLoaSen.tar
untar MaunaLoaSen.tar
untar GPSdata.tar

wget http://149.165.154.65/data/HDF5EOS/MaunaLoa/GPSdata.tar
git clone https://github.com/geodesymiami/plotdata.git
```
