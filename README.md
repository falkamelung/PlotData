# plotdata
Scripts to plot GPS, Seismcity abd InSAR data

# Installation
- Set environment variables:
```
export SCRATCHDIR=~/Downloads/test
export PLOTDATA_HOME=~/tools/plotdata
export GPSDIR=~/Downloads/GPSdata
```
- Prepend to your $PATH:
```
export PATH=$PLOTDATA_HOME:$PATH
export PYTHONPATH=$PLOTDATA_HOME:$PYTHONPATH
```
- Get the InSAR and GPS data for Hawaii:
```
mkdir -p $SCRATCHDIR
cd $SCRATCHDIR
wget http://149.165.154.65/data/HDF5EOS/MaunaLoa/MaunaLoaSen.tar
tar xvf MaunaLoaSen.tar

mkdir -p $GPSDIR
cd $GPSDIR
wget http://149.165.154.65/data/HDF5EOS/MaunaLoa/GPSdata.tar
tar xvf GPSdata.tar 
```
- Clone code to your tools directory:
```
mkdir -p $PLOTDATA_HOME
cd $PLOTDATA_HOME/..
git clone https://github.com/geodesymiami/plotdata.git
```
- run testdata:
```
cd $SCRATCHDIR
plot_data.py --help
plot_data.py MaunaLoaSenDT87/mintpy_5_20 MaunaLoaSenAT124/mintpy_5_20 --period 20221127-20221219 --plot-type velocity --ref-point 19.55,-155.45
```
Run the Notebook `run_MaunaLoa.ipynb`.  You also can run in Jupyer Lab `plot_data.ipynb`. Adjust `cmd` line below the `main` function as needed.  
