#!/bin/bash
trap "exit 1" HUP INT
python3 fake_agent_init.py
sleep 30
while true
do
    scrapy crawl rightnow_spider
    sleep 600    
done
