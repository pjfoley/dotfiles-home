#!/bin/bash
set -e
#Error message colour setup
RED='\033[0;31m'
RESET='\033[0m'

#Get script name using BASH substring Removal
case "${0##*/}" in
  *TV)
    SOURCE="${HOME}/Downloads/Site/TV"
    DESTINATION="/srv/Newsgroups/Complete/TV/"
    unrar_func=unrar_tv
    cleanup_func=cleanup_tv
    ;;

  *MOVIES)
    SOURCE="${HOME}/Downloads/Site/Movies/"
    DESTINATION="/srv/Movies"
    unrar_func=unrar_movie
    cleanup_func=cleanup_movie
    ;;

  *)
    echo "Not supported - ${0##*/}"
    exit 0
esac

unrar_tv() {
  local sfilename=$1
  unrar e -inul -o+ "${sfilename}" "${DESTINATION}"
}

unrar_movie() {
  local sfilename=$1
  local directory="$(echo "$sfilename" | sed -n -e '1p' | sed  -e 's#//*#/#g' -e 's#\(.\)/$#\1#' -e 's#^[^/]*$#.#' -e 's#\(.\)/[^/]*$#\1#' -)"
  unrar e -inul -o+ "${sfilename}" "${directory}"
}

cleanup_tv() {
  local directory=$1
  rm -R "${directory}"
}

cleanup_movie(){
  local directory=$1
  set +e
  rm -R "${directory}/"*.r* "${directory}/"\[COMPLETE* "${directory}/"rushchk.log "${directory}/"*.sfv
  set -e
  if $(cp -f -R --no-preserve=mode,ownership "${directory}" "${DESTINATION}"); then
    rm -R "${directory}"
  else
    echo -e "${RED}ERROR cleaning up - ${directory}${RESET}"
    echo
  fi
}

find "${SOURCE}" -maxdepth 2 -type d -name '\[COMPLETE*' -print0| while read -r -d $'\0' matched
do
  SUCCESS=0
  # Get last directory - dirname
  directory="$(echo "$matched" | sed -n -e '1p' | sed  -e 's#//*#/#g' -e 's#\(.\)/$#\1#' -e 's#^[^/]*$#.#' -e 's#\(.\)/[^/]*$#\1#' -)"

  # Find the rar file
  sfilename=$(find "${directory}" -depth -name "*.rar" -print -quit)

  if ${unrar_func} "${sfilename}"; then
     ${cleanup_func} "${directory}"
  else
    if ! [ -f "${sfilename}" ]; then 
      echo -e "${RED}No RAR file - $(basename ${directory})${RESET}"
      continue
    else
      errno=$?
      echo -e "${RED}Unrar error (${errno}) - $(basename ${directory})${RESET}"
      continue
    fi
  fi
  echo "Extracted - $(basename ${directory})"
done
