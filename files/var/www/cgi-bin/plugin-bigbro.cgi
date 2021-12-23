#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="bigbro"
page_title="BigBro"
config_file="/etc/${plugin}.cfg"
[ ! -f "$config_file" ] && touch ${config_file}

if [ -n "$POST_pin" ]; then
  pin="$POST_pin"
  signature=$(echo -ne "$pin" | md5sum | awk '{print $1}')
  sed -d /^${pin}:/ ${config_file}
  echo "${pin}:${signature}" >> ${config_file}
  redirect_to "?pin=${pin}"
fi
%>
<%in _header.cgi %>
<div class="alert alert-warning">Attention! This is only a proof of concept for the prospective subsystem of additional services. No real functionality here.</div>
<%
if [ -n "$GET_new" ]; then
  page_title="Add a device"
%>
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-3">
  <div class="col">
    <div class="card h-100">
      <div class="card-header">Add Device</div>
      <div class="card-body">
        <form action="/cgi-bin/plugin-bigbro.cgi" method="post" enctype="multipart/form-data">
          <div class="row mb-3">
            <p>Please enter access PIN to add a device.</p>
            <label class="col-md-3 form-label" for="pin">Access PIN</label>
            <div class="col-md-9">
              <input class="form-control" type="text" name="pin" id="pin" pattern="[A-Za-z0-9]+">
              <div class="hint">letters and numbers, no punctuation or special characters</div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary">Add Device</button>
        </form>
      </div>
    </div>
  </div>
</div>
<%
elif [ -n "$GET_pin" ]; then
  pin="$GET_pin"
  signature=$(grep "^${pin}" ${config_file} | cut -d: -f2)
%>
<h3><%= ${pin} %></h3>
<p><%= ${signature} %></p>
<p><a href="?">List of devices</a></p>
<% else %>
<h3>List of devices</h3>
<p><a href="?new=device">add a device</a></p>
<dl>
<% for device in $(cat ${config_file}); do %>
<dt><a href="?pin=<%= ${device%:*} %>"><%= ${device%:*} %></a></dt>
<dd><%= ${device##*:} %></dd>
<% done %>
</dl>
<% fi %>
<%in _footer.cgi %>
