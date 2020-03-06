#!/usr/bin/env bash
echo "Loading environment vars.."
source /home/ec2-user/secrets.sh
echo "Performing backup.."
cd /webapps/dbhelpers/src
python3 create_backup.py
echo "Running migrations.."
python3 run_migrations.py
echo "Performing backup.."
python3 create_backup.py
echo "All done!"
