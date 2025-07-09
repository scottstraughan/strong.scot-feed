---
date: '2021-01-18T01:00:00'
title: 'Yale Alarm API Scheduler'
description: "Automatically enable and disable your alarm on a schedule."
thumbnail: /static/images/rants/2021-01-18-auto-arm-yale-alarm/thumbnail.webp
icon: /static/images/rants/2021-01-18-auto-arm-yale-alarm/icon.webp
tags:
  - python
  - script
  - api
  - automation
---

I love my Yale home alarm system. The system has been rock solid, aside from a few annoying usability quirks, but there is one core feature missing - scheduling. It is a pain in the ass to have to manually arm the system every single night. Rarely do I ever enter/leave my house between the hours of 12:00pm and 6:00am so it makes total sense to always have the system part-armed (where only the door/window sensors are armed - not the motion sensors) during these times. I discovered an excellent Python wrapper that provides a simple and easy way to arm and disarm the system using the Yale account email address and password. Only thing missing, a way to run the script at specific times, provide a notification of the new change of state and a system to host the script so it will always be available. 

I will shorlty be posting a blog that details how you can get this to work using AWS, but for now, we will focus on using a Docker container that can run on any PC, or in my case, a Rasberry PI 4B that I am using as my NAS device.

![Screenshot](/static/images/rants/2021-01-18-auto-arm-yale-alarm/thumbnail.webp)

## Get Its Working

1. Clone my GitHub repo.

    ```git clone https://github.com/scottstraughan/yale-alarm-scheduler.git```

2. Install [Docker](https://www.docker.com)
3. If you are using Windows, install gitbash - just makes life easier.
4. Change into the cloned repo:

    ```cd yale-alarm-scheduler```
5. Update the ```config.json``` file with your credentails and schedule (there are examples of how to do this in the config file). If you wish to have email notifications sent to you when the system is armed or disarmed, please propogate the values for "send_grid" (SendGrid is a super easy way to send emails from an API. You can create a FREE account and get hundreds of free emails per month to use).
5. Build the docker image using the provider Dockerfile:

    ```docker build -t yale-alarm-scheduler .```
6. Create a new container instance based on the previously created image:

    ```docker run --rm yale-alarm-scheduler```
7. Done. The system should now be running and will automatically arm/disarm based on your schedule.

**Next up, AWS Lambda!**
