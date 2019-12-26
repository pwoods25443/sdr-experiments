#SatNOGS Station

### Create an account at satnogs.org and create a new ground station

### Setup the raspberry Pi Target
Following [these instructions](https://wiki.satnogs.org/Raspberry_Pi_3)

### Setup up MacOS Host
Using python 3.6, install ansible in a virtualenv
```buildoutcfg
virtualenv ansible
source ansible/bin/activate
pip install ansible
```

Inastalling sshpass in osx so that ssh login from host to target can be automated.  Probably better to use propoer ssh keys

```buildoutcfg
brew install http://git.io/sshpass.rb
```
Install the satnogs client on the host following [this](https://wiki.satnogs.org/SatNOGS_Client_Ansible#Updating_SatNOGS_Client_software)
```buildoutcfg
git clone https://gitlab.com/librespacefoundation/satnogs/satnogs-client-ansible.git
cd satnogs-client-ansible
cp -r production.dist production
```
Edit the anisible hosts file to change `ansible_host`
```
nano production/inventory/hosts
```

Set up the raspberry pi target system
```buildoutcfg
ansible-playbook -i production/inventory -K site.yml 
ssh -t pi@raspberrypi.local sudo satnogs-setup
```
Select Basic Configuration and set all the parameters, then go back to the main menu and select Apply


### Operation
