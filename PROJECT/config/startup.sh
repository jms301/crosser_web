#!/bin/bash

crosser_web/manage.py runfcgi host=127.0.0.1 port=8090

echo "DID YOU REMEMBER TO COLLATE THE STATIC FILES??"
