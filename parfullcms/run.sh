#!/bin/sh -ex
source /opt/cms/slc6_amd64_gcc491/external/gcc/4.9.1-cms/etc/profile.d/init.sh
source /opt/cms/slc6_amd64_gcc491/external/xerces-c/2.8.0-cms/etc/profile.d/init.sh
source /opt/cms/slc6_amd64_gcc491/external/clhep/2.1.4.1-cms/etc/profile.d/init.sh
source /opt/cms/slc6_amd64_gcc491/external/geant4/10.00.p03/etc/profile.d/init.sh
source /opt/cms/slc6_amd64_gcc491/external/geant4-parfullcms/2014.01.27-ddloan/etc/profile.d/init.sh

source /opt/cms/slc6_amd64_gcc491/external/geant4-G4NEUTRONXS/1.4/etc/profile.d/init.sh
source /opt/cms/slc6_amd64_gcc491/external/geant4-G4SAIDDATA/1.1/etc/profile.d/init.sh
source /opt/cms/slc6_amd64_gcc491/external/geant4-G4EMLOW/6.35/etc/profile.d/init.sh
source /opt/cms/slc6_amd64_gcc491/external/geant4-G4PhotonEvaporation/3.0/etc/profile.d/init.sh

cd  /opt/cms/slc6_amd64_gcc491/external/geant4-parfullcms/2014.01.27-ddloan/share/ParFullCMS

sed -ibak "s;\(/run/beamOn \).*;\1$EVENTS;" mt.g4

export G4FORCENUMBEROFTHREADS=${G4FORCENUMBEROFTHREADS-max}
export G4LEDATA
export G4LEVELGAMMADATA
export G4SAIDXSDATA
export G4NEUTRONXSDATA

cat mt.g4
ParFullCMS mt.g4 2>&1 | tee /data/run.log
