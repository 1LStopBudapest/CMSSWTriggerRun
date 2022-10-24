# This is to run trigger script in lxplus account

Log in to your lxplus account

Set up CMSSW area

```
cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv
```
Checkout scipt from github

```
git clone git@github.com:1LStopBudapest/CMSSWTriggerRun.git
git clone git@github.com:1LStopBudapest/Helper.git
```
The trigger scripts are inside CMSSWTriggerRun directory. One can check. 

Now to submit the condor jobs which runs over the nanoAOD data samples

Make CMSSW tar file

```
cd ../..
tar -zcvf CMSSW_10_2_22.tar.gz CMSSW_10_2_22
mv CMSSW_10_2_22.tar.gz CMSSW_10_2_22/src/CMSSWTriggerRun/condor/
cd CMSSW_10_2_22/src/CMSSWTriggerRun/condor/
```
Set up proxy

```
voms-proxy-init --voms cms --valid 168:00
```
It will create a proxy file in /tmp directory with format something like this x5..

please copy that file in your home directory
```
cp /tmp/ProxyFile ~/
```

Now Submit condor jobs
```
python condorScript.py --prxy ProxyFile --prxyPath Path-to-proxyfile
```
This condor script submit the jobs for each of era of a given year. One can add all the text files of different eras of a year and add a new samplename entry to the samples dictionary in FileList_ config file. Then if that samplename is given to the condorscript, it will run on all the files of a year.
But it can slow down the condor for overload and ever causes condor errors. Therefore its better to run condor for each era seperately.