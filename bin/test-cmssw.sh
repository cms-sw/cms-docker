#!/bin/bash -ex
RELEASE_INST_DIR=/cvmfs/cms-ib.cern.ch
if [ "$WORKSPACE" = "" ] ; then export WORKSPACE=$(/bin/pwd) ; fi
cd $WORKSPACE

ls /cvmfs/cms-ib.cern.ch >/dev/null 2>&1
ls /cvmfs/cms.cern.ch >/dev/null 2>&1
GET_CMD="wget -q -O"
if wget --help >/dev/null 2>&1 ; then
  $GET_CMD cmsos https://raw.githubusercontent.com/cms-sw/cms-common/master/common/cmsos
else
  GET_CMD="curl -s -k -L -o"
  $GET_CMD cmsos https://raw.githubusercontent.com/cms-sw/cms-common/master/common/cmsos
fi
chmod +x cmsos
HOST_CMS_ARCH=$(./cmsos 2>/dev/null)
$GET_CMD bootstrap.sh http://cmsrep.cern.ch/cmssw/bootstrap.sh

#INVALID_ARCHS='slc6_amd64_gcc461 slc6_amd64_gcc810 slc7_aarch64_gcc493 slc7_aarch64_gcc530'
export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git.daily
week=week$(ls -d ${RELEASE_INST_DIR}/nweek-* | head -1 | sed 's|.*\(.\)$|\1%2|' | bc)
rpm_repo="cms.$week"
rm -rf inst; mkdir inst; cd inst
$GET_CMD archs http://cmsrep.cern.ch/cgi-bin/repos/${rpm_repo}
FAILED=""
PASSED=""
parch=""
for arch in $(grep ">${HOST_CMS_ARCH}_" archs |  sed "s|.*>${HOST_CMS_ARCH}_|${HOST_CMS_ARCH}_|;s|<.*||") ; do
  cd $WORKSPACE/inst
  if [ $(echo ${INVALID_ARCHS} | tr ' ' '\n' | grep "^${arch}$" | wc -l) -gt 0 ] ; then
    echo "Skip: Invalid architecture ${arch}"
    continue
  fi
  [ "${parch}" != "" ] && rm -rf ${parch}
  parch="${arch}"
  [ -e $WORKSPACE/${arch}.OK ] && continue
  export SCRAM_ARCH=$arch
  rm -rf ./$SCRAM_ARCH ; mkdir -p ./$SCRAM_ARCH
  cd ./$SCRAM_ARCH
  touch cmssw.rel
  $(source /cvmfs/cms.cern.ch/cmsset_default.sh >/dev/null 2>&1; scram -a $SCRAM_ARCH list -c CMSSW | grep -v '/cmssw-patch/' | grep ' CMSSW_' >cmssw.rel) || true
  cat cmssw.rel
  boot_repo=${rpm_repo}
  cmssw_ver=""
  for v in $(grep ${RELEASE_INST_DIR}/${week}/ cmssw.rel | grep '_[0-9][0-9]*_X_' | awk '{print $3}') ; do
    if [ -e $v/build-errors ] ; then continue ; fi
    cmssw_ver=$(basename $v)
  done
  if [ "${cmssw_ver}" = "" ] ; then
    cmssw_ver=$(grep /cvmfs/cms.cern.ch/ cmssw.rel | tail -1 | awk '{print $2}' || true)
    boot_repo="cms"
  fi
  if ! sh -ex $WORKSPACE/bootstrap.sh -r ${boot_repo} -a $SCRAM_ARCH setup ; then
    FAILED="${FAILED} ${SCRAM_ARCH}"
    continue
  fi
  echo "======================================================="
  if [ "${cmssw_ver}" = "" ] ; then
    echo "Warnings: No CMSSW version available for $SCRAM_ARCH"
    touch $WORKSPACE/${SCRAM_ARCH}.OK
    PASSED="${PASSED} ${SCRAM_ARCH}"
    continue
  fi
  echo "Found release: ${cmssw_ver}"
  INSTALL_PACKAGES="$($WORKSPACE/inst/$SCRAM_ARCH/common/cmspkg -a $SCRAM_ARCH search gcc-fixincludes | sed 's| .*||' | grep 'gcc-fixincludes' | sort | tail -1)"
  $WORKSPACE/inst/$SCRAM_ARCH/common/cmspkg -a $SCRAM_ARCH install -y cms+cmssw+${cmssw_ver}
  if [ "${INSTALL_PACKAGES}" != "" ] ; then
    $WORKSPACE/inst/$SCRAM_ARCH/common/cmspkg -a $SCRAM_ARCH install -y ${INSTALL_PACKAGES}
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
        cp -r $CMSSW_RELEASE_BASE/src/$p/* $CMSSW_BASE/src/$p/
      fi
    done
    if scram build -j $(nproc) ; then
      touch ${WORKSPACE}/${SCRAM_ARCH}.OK
      PASSED="${PASSED} ${SCRAM_ARCH}"
    else
      FAILED="${FAILED} ${SCRAM_ARCH}"
    fi
  )
  rm -rf $SCRAM_ARCH
done
[ "${parch}" != "" ] && rm -rf ${parch}
echo "Passed: $PASSED"
echo "Failed: $FAILED"
if [ "$FAILED" != "" ] ; then exit 1 ; fi
echo "ALL_OK"
