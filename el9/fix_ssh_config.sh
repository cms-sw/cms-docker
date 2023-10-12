#!/bin/bash
function fix_ssh_config()
{
  cat "$1" | while read line ; do
    if [ $(echo "$line" | grep '^\s*Include\s\s*' | wc -l) -eq 0 ] ; then
      echo "$line"
    else
      echo "#${line}"
      cfgs=$(echo "$line" | sed 's|^\s*Include\s\s*||')
      for cfg in $(ls $cfgs 2>/dev/null) ; do
        echo "###  Start of $cfg  ###"
        fix_ssh_config "$cfg"
         echo "###  End of $cfg  ###"
      done
     fi
  done
}
if [ -e "$1" ] ; then
  fix_ssh_config $1 > $1.tmp
  mv $1.tmp $1
fi
