python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
mkdir logs

crontab -l > mycron
echo "0       *       *       *       *       /root/vk-header-group-control/run.sh" >> mycron
crontab mycron
rm mycron
