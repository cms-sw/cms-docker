#!/bin/bash -ex
CMSREP="cmsrep.cern.ch"
if [ "$2" != "" ] ; then CMSREP="$2" ; fi
RELEASE_INST_DIR=/cvmfs/cms-ib.cern.ch
INVALID_ARCHS='slc6_amd64_gcc461 slc6_amd64_gcc810 slc7_aarch64_gcc493 slc7_aarch64_gcc530'
export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git.daily
ARCHS="$1"

if [ "$WORKSPACE" = "" ] ; then export WORKSPACE=$(/bin/pwd) ; fi
cd $WORKSPACE
rm -rf inst; mkdir inst; cd inst

ls /cvmfs/cms-ib.cern.ch >/dev/null 2>&1
ls /cvmfs/cms.cern.ch >/dev/null 2>&1

GET_CMD="curl -s -k -L -o"
if wget --help >/dev/null 2>&1 ; then GET_CMD="wget -q -O" ; fi
$GET_CMD bootstrap.sh http://${CMSREP}/cmssw/bootstrap.sh

if [ "${ARCHS}" = "" ] ; then
  $GET_CMD archs http://${CMSREP}/cgi-bin/repos/cms
  $GET_CMD cmsos https://raw.githubusercontent.com/cms-sw/cms-common/master/common/cmsos
  chmod +x cmsos
  HOST_CMS_ARCH=$(./cmsos 2>/dev/null)
  ARCHS=$(grep ">${HOST_CMS_ARCH}_" archs |  sed "s|.*>${HOST_CMS_ARCH}_|${HOST_CMS_ARCH}_|;s|<.*||")
  rm -f cmsos archs
fi

parch=""
touch $WORKSPACE/res.txt
for arch in ${ARCHS} ; do
  export SCRAM_ARCH=$arch
  cd $WORKSPACE/inst
  echo ${SCRAM_ARCH} >> $WORKSPACE/res.txt
  if [ $(echo ${INVALID_ARCHS} | tr ' ' '\n' | grep "^${arch}$" | wc -l) -gt 0 ] ; then
    echo ${SCRAM_ARCH}.SKIP >> $WORKSPACE/res.txt
    continue
  fi
  [ "${parch}" != "" ] && rm -rf ${parch}
  parch="${arch}"
  rm -rf ./$SCRAM_ARCH ; mkdir -p ./$SCRAM_ARCH
  cd ./$SCRAM_ARCH
  touch cmssw.rel
  $(source /cvmfs/cms.cern.ch/cmsset_default.sh >/dev/null 2>&1; scram -a $SCRAM_ARCH list -c CMSSW | grep -v '/cmssw-patch/' | grep ' CMSSW_' >cmssw.rel) || true
  cat cmssw.rel
  cmssw_ver=""
  boot_repo="cms"
  for v in $(grep ${RELEASE_INST_DIR}/ cmssw.rel | grep '_[0-9][0-9]*_X_' | awk '{print $3}' | tac) ; do
    if [ -e $v/build-errors ] ; then continue ; fi
    cmssw_ver=$(basename $v)
    boot_repo=cms.$(echo $v | cut -d/ -f4)
    break
  done
  if [ "${cmssw_ver}" = "" ] ; then
    cmssw_ver=$(grep /cvmfs/cms.cern.ch/ cmssw.rel | tail -1 | awk '{print $2}' || true)
  fi
  if ! sh -ex $WORKSPACE/inst/bootstrap.sh -server ${CMSREP} -r ${boot_repo} -a $SCRAM_ARCH setup ; then
    echo ${SCRAM_ARCH}.BOOT.ERR >> $WORKSPACE/res.txt
    continue
  fi
  echo ${SCRAM_ARCH}.BOOT.OK >> $WORKSPACE/res.txt
  if [ "${cmssw_ver}" = "" ] ; then
    echo "Warnings: No CMSSW version available for $SCRAM_ARCH"
    continue
  fi
  echo "Found release: ${cmssw_ver}"
  INSTALL_PACKAGES="$($WORKSPACE/inst/$SCRAM_ARCH/common/cmspkg -a $SCRAM_ARCH search gcc-fixincludes | sed 's| .*||' | grep 'gcc-fixincludes' | sort | tail -1)"
  INST_OPTS="-a $SCRAM_ARCH --debug install --ignore-size --jobs 2 -y"
  $WORKSPACE/inst/$SCRAM_ARCH/common/cmspkg $INST_OPTS cms+cmssw+${cmssw_ver}
  if [ "${INSTALL_PACKAGES}" != "" ] ; then
    $WORKSPACE/inst/$SCRAM_ARCH/common/cmspkg $INST_OPTS ${INSTALL_PACKAGES}
  fi
  export cmssw_ver
  (
    source $WORKSPACE/inst/$SCRAM_ARCH/cmsset_default.sh >/dev/null 2>&1
    scram -a $SCRAM_ARCH project ${cmssw_ver}
    cd ${cmssw_ver}
    eval `scram run -sh` >/dev/null 2>&1
    USE_GIT=false
    if git cms-addpkg FWCore/Version >/dev/null 2>&1 ; then USE_GIT=true ; fi
    for p in FWCore/PrescaleService FWCore/SharedMemory FWCore/Framework DataFormats/Common DataFormats/StdDictionaries CondFormats/HIObjects ; do
      [ -e $CMSSW_RELEASE_BASE/src/$p ] || continue
      if $USE_GIT  ; then
        git cms-addpkg $p
      else
        mkdir -p $CMSSW_BASE/src/$p
        rsync -a $CMSSW_RELEASE_BASE/src/$p/ $CMSSW_BASE/src/$p/
      fi
    done
    if scram build -j $(nproc) ; then
      echo ${SCRAM_ARCH}.${cmssw_ver}.OK >> $WORKSPACE/res.txt
    else
      echo ${SCRAM_ARCH}.${cmssw_ver}.ERR >> $WORKSPACE/res.txt
    fi
  )
  rm -rf $SCRAM_ARCH
done
[ "${parch}" != "" ] && rm -rf ${parch}
cd $WORKSPACE
rm -rf inst
cat $WORKSPACE/res.txt
if [ $(grep '\.ERR$' $WORKSPACE/res.txt | wc -l) -gt 0 ] ; then exit 1 ; fi
echo "ALL_OK"
