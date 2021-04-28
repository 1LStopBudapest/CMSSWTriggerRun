# This is to run trigger script in lxplus account

Log in to your lxplus account

Set up CMSSW area

```
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
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
cd CMSSWTriggerRun/condor/
```

Submit condor jobs
```
python condorScript.py
```
