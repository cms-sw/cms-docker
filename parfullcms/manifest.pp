# An example puppet file which installs CMSSW into 
# /opt/cms.

#package {["HEP_OSlibs_SL6", "e2fsprogs"]:
#  ensure => present,
#}->

file {"/etc/sudoers.d/999-cmsbuild-requiretty":
   content => "Defaults:root !requiretty\n",
}->
package {"external+geant4-parfullcms+2014.01.27-ddloan":
  ensure             => present,
  provider           => cmsdist,
  install_options    => [{
    "install_prefix" => "/opt/cms",
    "install_user"   => "cmsbuild",
    "architecture"   => "slc6_amd64_gcc491",    
    "server"         => "cmsrep.cern.ch",
    "server_path"    => "cmssw/cms.week0",
  }]
}
