# Copy sensible bits in cmsbuild home.
# Notice you need to do (as root) the following:
#
#     sudo mkdir -p /var/www/html/cms/cpt/Software
#     sudo ln -sf /data/cmssw /var/www/html/cms/cpt/Software/download
#
# Because sources.list file in apt still contains the old URL.
#
rsync -av --delete $SOURCE_USER@$SOURCE_SERVER:/home/$SOURCE_USER/.ssh/ /home/$SOURCE_USER/.ssh/
mkdir -p /data/cmssw
ln -sfT /afs/cern.ch/cms/slc5_amd64_gcc462/external/apt/429-cms /data/cmssw/apt
ln -sfT /afs/cern.ch/cms/slc5_amd64_gcc462/external/apt/429-cms /data/cmssw/apt
ln -sfT /afs/cern.ch/cms/slc5_amd64_gcc462/external/apt/429-cms /data/cmssw/apt.new
ln -sfT /afs/cern.ch/cms/slc5_amd64_gcc462/external/apt/429 /data/cmssw/apt.old

# Rsync a few mirrors we have:
for x in apt beecrypt millepede oracle pyqt pysqlite; do
  rsync -av $SOURCE_USER@$SOURCE_SERVER:/data/cmssw/$x-mirror/ /data/cmssw/$x-mirror/ 
done

# First do CMSSW
cd /data/cmssw
FIXED_LINK=`ssh $SOURCE_USER@SOURCE_SERVER readlink /data/cmssw/cms`
echo $FIXED_LINK 
DEST=/data/cmssw/cms-cache/cms.0000000000000000000000000000000000000000000000000000000000000000-0000000000000000000000000000000000000000000000000000000000000000
mkdir -p $DEST
rsync -av --delete --prune-empty-dirs $FIXED_LINK/ $DEST/
ssh $MIRROR_SERVER ln -sfT $DEST /data/cmssw/cms
mkdir -p $DEST/WEB
mkdir -p $DEST/TARS
mkdir -p $DEST/SOURCES
mkdir -p $DEST/RPMS
mkdir -p $DEST/SRPMS

BASE=$DEST
# Then copy cms.week0
FIXED_LINK=`readlink /data/cmssw/cms.week0`
echo $FIXED_LINK 
DEST=/data/cmssw/cms.week0-cache/cms.week0.0000000000000000000000000000000000000000000000000000000000000000-0000000000000000000000000000000000000000000000000000000000000001
ssh $MIRROR_SERVER mkdir -p $DEST
rsync -av --delete --prune-empty-dirs $FIXED_LINK/ --link-dest $BASE/ $MIRROR_SERVER:$DEST/
ssh $MIRROR_SERVER ln -sfT $DEST /data/cmssw/cms.week0
mkdir -p $DEST/WEB
mkdir -p $DEST/TARS
mkdir -p $DEST/SOURCES
mkdir -p $DEST/RPMS
mkdir -p $DEST/SRPMS

# And copy cms.week1
FIXED_LINK=`readlink /data/cmssw/cms.week1`
echo $FIXED_LINK 
DEST=/data/cmssw/cms.week1-cache/cms.week1.0000000000000000000000000000000000000000000000000000000000000000-0000000000000000000000000000000000000000000000000000000000000002
ssh $MIRROR_SERVER mkdir -p $DEST
rsync -av --delete --prune-empty-dirs $FIXED_LINK/ --link-dest $BASE/ $MIRROR_SERVER:$DEST/
ssh $MIRROR_SERVER ln -sfT $DEST /data/cmssw/cms.week1
mkdir -p $DEST/WEB
mkdir -p $DEST/TARS
mkdir -p $DEST/SOURCES
mkdir -p $DEST/RPMS
mkdir -p $DEST/SRPMS

# Then do comp
FIXED_LINK=`readlink /data/cmssw/comp`
echo $FIXED_LINK
DEST=/data/cmssw/comp-cache/comp.0000000000000000000000000000000000000000000000000000000000000000-0000000000000000000000000000000000000000000000000000000000000000
ssh $MIRROR_SERVER mkdir -p $DEST
rsync -av --delete --prune-empty-dirs $FIXED_LINK/ $MIRROR_SERVER:$DEST/
ssh $MIRROR_SERVER ln -sfT $DEST /data/cmssw/comp
BASE=$DEST
mkdir -p $DEST/WEB
mkdir -p $DEST/TARS
mkdir -p $DEST/SOURCES
mkdir -p $DEST/RPMS
mkdir -p $DEST/SRPMS

# And comp.pre
FIXED_LINK=`readlink /data/cmssw/comp.pre`
echo $FIXED_LINK
DEST=/data/cmssw/comp.pre-cache/comp.pre.0000000000000000000000000000000000000000000000000000000000000000-0000000000000000000000000000000000000000000000000000000000000001
ssh $MIRROR_SERVER mkdir -p $DEST
rsync -av --delete --prune-empty-dirs $FIXED_LINK/ --link-dest $BASE/ $MIRROR_SERVER:$DEST/
ssh $MIRROR_SERVER ln -sfT $DEST /data/cmssw/comp.pre
mkdir -p $DEST/WEB
mkdir -p $DEST/TARS
mkdir -p $DEST/SOURCES
mkdir -p $DEST/RPMS
mkdir -p $DEST/SRPMS

# Create working web server
#ln -sf /data/cmssw /var/www/html/cmssw
#scp /var/www/html/index.html $MIRROR_SERVER:/var/log/html/index.html
#scp /var/www/html/robots.txt $MIRROR_SERVER:/var/log/html/robots.txt
