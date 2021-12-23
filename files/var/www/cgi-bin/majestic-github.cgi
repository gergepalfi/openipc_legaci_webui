#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="Downloading latest majestic"
get_soc() {
  case "$soc" in
    gk7605v100 | gk7205v300 | gk7202v300 | gk7205v200)
      soc="gk7205v200"
      ;;
    hi3516dv100 | hi3516av100)
      soc="hi3516av100"
      ;;
    hi3518cv200 | hi3518ev200 | hi3518ev201 | hi3516cv200)
      soc="hi3516cv200"
      ;;
    hi3516ev100 | hi3516cv300)
      soc="hi3516cv300"
      ;;
    hi3516dv300 | hi3516av300 | hi3516cv500)
      soc="hi3516cv500"
      ;;
    hi3516ev200 | hi3518ev300 | hi3516dv200 | hi3516ev300)
      soc="hi3516ev300"
      ;;
    nt98562 | nt98566)
      soc="nt9856x"
      ;;
    ssc337 | ssc335)
      soc="ssc335"
      ;;
    xm530 | xm550)
      soc="xm550"
      ;;
    *)
      soc=
      ;;
  esac
  [ ! -z "$soc" ] && return=${soc}
}
check_url() {
  status_code=$(curl --silent --head http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc}.master.tar.bz2)
  status_code=$(echo "$status_code" | grep "HTTP/1.1" | cut -d " " -f 2)

  [ ${status_code} = "200" ] && return=1
} %>
<%in _header.cgi %>
<h4>Please wait...</h4>
<progress id="timer" max="90" value="0" class="w-100"></progress>
<pre>
<%
soc=$(ipcinfo --chip_id 2>&1)
if [ -f /rom/usr/bin/majestic ] && get_soc ; then
  if check_url ; then
    killall majestic

    free_space=$(df | grep /overlay | xargs | cut -d " " -f 4)
    old_majestic_size=0
    [ -f /overlay/root/usr/bin/majestic ] && old_majestic_size=$(ls -s /usr/bin/majestic | xargs | cut -d " " -f 1)
    available_space=$(( $free_space + $old_majestic_size - 1 ))

    curl -k -L -o /tmp/majestic.tar.bz2 http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc}.master.tar.bz2

    bunzip2 -c /tmp/majestic.tar.bz2 | tar -x -C /tmp/ ./majestic
    if [ $? -eq 0 ]; then
      new_majestic_size=$(ls -s /tmp/majestic | xargs | cut -d " " -f 1)

      if [ ! $new_majestic_size -gt $available_space ]; then
       # bunzip2 -ck /tmp/majestic.tar.bz2 | tar -xk -C /usr/lib/ ./lib*
        [ -f /overlay/root/usr/bin/majestic ] && rm -f /usr/bin/majestic
        mv -f /tmp/majestic /usr/bin/majestic
      else
        error="Not enough space to update majestic."
      fi
    else
      error="Cannot extract majestic."
    fi
    rm -f /tmp/majestic
    rm -f /tmp/majestic.tar.bz2
    nohup majestic -s 2>&1 >/dev/null &
  else
    error="Can't get update from server."
  fi
else
  error="Majestic is not support this system."
fi
%>
</pre>
<%
if [ ! -z "$error" ]; then
  report_error "$error"
fi
%>
<script>
function tick() {
    tock += 1;
    $('#timer').value = tock;
    (tock === max) ? window.location.replace("/cgi-bin/progress.cgi") : setTimeout(tick, 1000);
}
function engage() {
    max = $('#timer').max;
    setTimeout(tick, 1000);
}
window.onload = engage;
</script>
<%in _footer.cgi %>
