#!/bin/bash -ex
if [ "$WORKSPACE" = "" ] ; then WORKSPACE=$(/bin/pwd) ; fi
cd $WORKSPACE
GET_CMD="wget -q -O"
if wget --help >/dev/null 2>&1 ; then
  $GET_CMD cmsos https://raw.githubusercontent.com/cms-sw/cmsdist/master/cmsos.file
else
  GET_CMD="curl -s -k -L -o"
  $GET_CMD cmsos https://raw.githubusercontent.com/cms-sw/cmsdist/master/cmsos.file
fi
chmod +x cmsos
HOST_CMS_ARCH=$(./cmsos 2>/dev/null)
$GET_CMD bootstrap.sh http://cmsrep.cern.ch/cmssw/bootstrap.sh

INVALID_ARCHS='cms/slc6_amd64_gcc461 cms/slc6_amd64_gcc810'
for repo in cms ; do
  echo "############# REPO $repo ##################"
  mkdir -p $repo
  pushd $repo
    $GET_CMD archs http://cmsrep.cern.ch/cgi-bin/repos/$repo
    for arch in $(grep ">${HOST_CMS_ARCH}_" archs |  sed "s|.*>${HOST_CMS_ARCH}_|${HOST_CMS_ARCH}_|;s|<.*||") ; do
      if [ $(echo ${INVALID_ARCHS} | tr ' ' '\n' | grep "${repo}/${arch}$" | wc -l) -gt 0 ] ; then continue ; fi
      echo "============= $arch ================"
      mkdir -p $arch
      pushd $arch
        sh -ex $WORKSPACE/bootstrap.sh -debug -a $arch setup
      popd
    done
  popd
done
echo "ALL_OK"
