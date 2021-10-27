#!/bin/bash

echo `date`
cd /home/webpca/ensemble

python3.7 /home/webpca/ensemble/frontline.py > /home/webpca/ensemble/frontline.log 2>&1 &
python3.7 /home/webpca/ensemble/fronttest.py > /home/webpca/ensemble/fronttest.log 2>&1
