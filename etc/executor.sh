#!/bin/bash

while read line
do
  set -- $line

  ns=$1
  action=$2
  shift 2

  case $ns in
  tap)
    case $action in
      short)
        case $1 in
          1)
            xdotool click 2
            ;;
          2)
            xdotool key Super+Page_Down
            ;;
          3)
            xdotool key ctrl+alt+l
            ;;
        esac
        ;;
      long)
        case $1 in
          1)
            xdotool key Ctrl+F8
            ;;
          2)
            xdotool key Super+Page_Up
            ;;
        esac
        ;;
    esac
    ;;
  swipe)
    case $action in
      up)
        if [[ $1 == '0' ]]; then
          xdotool key Super+Tab
        else
          xdotool key Ctrl+F8
        fi
        ;;
      down)
        ACTIVE_WINDOW=`xprop -root | grep "_NET_ACTIVE_WINDOW(WINDOW)" | awk '{print $5}'`
        STATE=`xprop -id $ACTIVE_WINDOW | grep "_NET_WM_STATE"`

        if echo $STATE | grep "_NET_WM_STATE_MAXIMIZED_VERT" > /dev/null; then
          wmctrl -i -r $ACTIVE_WINDOW -b remove,maximized_vert,maximized_horz
        else
          wmctrl -i -r $ACTIVE_WINDOW -b add,maximized_vert,maximized_horz
        fi
        ;;
      left)
        if [[ $1 == '0' ]]; then
          num_desktops=`xdotool get_num_desktops`
          desktop=`xdotool get_desktop`
          desktop=$((($desktop + 1) % $num_desktops))
          xdotool set_desktop $desktop
        else
          xdotool key Alt+Right
        fi
        ;;
      right)
        if [[ $1 == '0' ]]; then
          num_desktops=`xdotool get_num_desktops`
          desktop=`xdotool get_desktop`
          desktop=$((($desktop + $num_desktops - 1) % $num_desktops))
          xdotool set_desktop $desktop
        else
          xdotool key Alt+Left
        fi
        ;;
    esac
    ;;
  esac
done < "${1:-/dev/stdin}"
