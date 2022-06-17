#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="yadisk"
page_title="$tPageTitlePluginYandexDisk"
config_file="/etc/${plugin}.cfg"; [ ! -f "$config_file" ] && touch $config_file
url=/cgi-bin/plugin-${plugin}.cgi

if [ -n "$POST_action" ] && [ "$POST_action" = "reset" ]; then
  mv $config_file ${config_file}.backup
  redirect_to $url
fi

if [ "POST" = "$REQUEST_METHOD" ]; then
  :> $config_file
  for v in enabled login password path socks5_enabled socks5_server socks5_port socks5_login socks5_password; do
    eval echo "${plugin}_${v}=\$POST_${plugin}_${v}" >> $config_file  
  done
  redirect_to $url
fi
%>
<%in _header.cgi %>
<%
eval $(grep = $config_file)

form_ $url "post"
  row_ "row-cols-1 row-cols-xl-3 g-3"
    col_card_ "$tHeaderYandexDiskSettings"
      field_switch "yadisk_enabled"
      field_text "yadisk_login"
      field_text "yadisk_password"
      field_text "yadisk_path"
    _col_card
    col_card_ "$tHeaderYandexDiskProxy"
      field_switch "yadisk_socks5_enabled"
      field_text "yadisk_socks5_server"
      field_number "yadisk_socks5_port"
      field_text "yadisk_socks5_login"
      field_text "yadisk_socks5_password"
    _col_card
    col_card_ "$tHeaderYandexDiskPluginConfig"
      pre_
        echo "$(cat $config_file)"
      _pre
    _col_card
  _row
  
  button_submit "$tButtonFormSubmit" "primary"
_form
%>
<%in _footer.cgi %>
