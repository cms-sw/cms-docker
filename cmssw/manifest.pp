# An example puppet file which installs CMSSW into 
# /opt/cms.

#package {["HEP_OSlibs_SL6", "e2fsprogs"]:
#  ensure => present,
#}->
file {"/etc/sudoers.d/999-cmsbuild-requiretty":
   content => "Defaults:root !requiretty\n",
}->
package {"cms+cmssw+CMSSW_7_3_0":
  ensure             => present,
  provider           => cmsdist,  
  install_options    => [{
    "install_prefix" => "/opt/cms",
    "install_user"   => "cmsbuild",
    "architecture"   => "slc6_amd64_gcc491",    
    "server"         => "cmsrep.cern.ch",
    "server_path"    => "cmssw/cms",
  }]
}->
package {"cms+local-cern-siteconf+sm111124":
  ensure             => present,
  provider           => cmsdist,
  install_options    => [{
    "install_prefix" => "/opt/cms",
    "install_user"   => "cmsbuild",
    "architecture"   => "slc6_amd64_gcc491",
    "server"         => "cmsrep.cern.ch",
    "server_path"    => "cmssw/cms",
  }]
}->
file {"/etc/profile.d/scram.sh":
  ensure   => present,
  content  => "source /opt/cms/cmsset_default.sh\n\n",
  mode     => 755
}->
file {"/etc/profile.d/scram.csh":
  ensure   => present,
  content  => "source /opt/cms/cmsset_default.csh\n\n",
  mode     => 755
}
