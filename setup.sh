service_path="/etc/systemd/system/fujiac.service"

# Create service file
printf "%s\n" "[Unit]
Description=Fujitsu AC
After=network.target

[Service]
User=root
ExecStart=/usr/bin/python3 /home/pi/fujitsu-ac-mqtt-server/server.py

[Install]
WantedBy=multi-user.target" > "$service_path"

# Print
printf "fujiac.service created\n" 

sleep 3

# Reload deamon and enable service
systemctl daemon-reload
systemctl enable fujiac.service

# Print
printf "fujiac.service enabled\n"
