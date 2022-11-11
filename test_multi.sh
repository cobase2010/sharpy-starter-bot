#!/bin/bash

for run in {1..250};
do
python bot_vs_bot.py
ps -ef |grep SC2 |awk '{print $2}' |xargs kill -9
sleep 10;
done

