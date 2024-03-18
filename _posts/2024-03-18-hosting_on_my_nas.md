---
title: "Hosting things on my Synology NAS"
tags: [diy, ddns, Synology, NAS, certificates, DuckDNS, lets-encrypt]
---

I use the domain `elhult.duckdns.org` to host things for private use. It points to my NAS, a DS214+ running DSM 7.1 from Synology. It is useful for backing up photos, running a Dropbox-like service and more.

The user interface is very friendly, but the simplest solution for remote access is via Synologys cloud, and the purpose of a NAS was partially to not be reliant on a specific cloud provider with lock in effects. So this blog post is some notes on how to get remote access for free, reasonably reliantly.

## Port forwarding

Port forwarding is the mechanism of forwarding traffic that comes to my home network via WAN to some specific host on my local network. This allows remote devices (e.g. my smartphone via cell data traffic) to connect to the NAS using my home network public IP address.

By default, my home router does not accept connections from the outside world. To set this up, I went to `192.168.0.1` which points to my home router, logged in as admin, navigated `Access Control` > `Port Forwarding`. There, I disable UPnP because [that is not safe](https://www.upguard.com/blog/what-is-upnp). And enabled port forwarding to the NAS (check its IP!) for the administrative interface and for the Synology Drive function. These services are exposed over TCP port 5001 and TCP/UDP port 6690.

While you are at it, you can pin IP of the NAS via the MAC address. Either go in to DHCP settings (`Home` > `Gateway` > `LAN`) or via (`Home`>`Network Map`>`press the nas icon`>`Reserve IP`).


## Dynamic DNS via DuckDNS

DNS is the mechanism of resolving a host name such as `elhult.duckdns.org` into a IP, such as my home network public IP. Since my ISP give me a new IP now and then, I need to update the DNS record regularly. This is called dynamic DNS or DDNS.

My router has support for DDNS settings. But only from the service providers DynDNS, NoIP and DtDNS. That is not good enough. I want to use [DuckDNS](http://www.duckdns.org/). I need a service running from time to time sending a certain HTTPS request to the DuckDNS server saying "hey, please send traffic on elhult.duckdns.org to me"! You show that you control that specific IP by sending traffic from that IP. It is super simple and you could do it manually with curl using a cron job. You need a computer running the job all the time, and you have the NAS, which can do this job for you!

Connect to the NAS web admin interface. Navigate `Control Panel`>`External Access`>`DDNS`. There is a list of different DDNS providers there if you press `Add`. It is updated sometimes, so maybe DuckDNS is in that list.
They used to not support DuckDNS out of the box, and in that case you need a config hack. Log in to the NAS via SSH and edit a certain config file to create a new DDNS provider. I believe I followed [this guide](https://medium.com/@unrecondite/using-synology-to-update-your-dynamic-ip-to-the-free-duckdns-service-66b9c5c4be4) when I set it up some year ago, and it has worked reliably since.

## Certificate via Let's Encrypt

When you connect to the NAS, you want to serve traffic on secure channels, e.g. https. For that, you will need a certificate.

Use [Let's Encrypt](https://letsencrypt.org/)! You need a service that regularly downloads updated certificates. It is a little complicated to do manually. Either use certbot from Let's Encrypt (see their guides on their home page), or simply use the NAS! Navigate `Control Panel`>`Security`>`Certificates`>`Add` and in the modal, you select `Add new certificate` and then `Get a certificate from Lets Encrypt` and continue through the wizard.

My NAS was powered down when I was abroad, and I got a warning email from Let's Encrypt that my certificate was about to expire. When I came home, I booted up the NAS, and it renewed the certificate. It just works.

## Serving content

Most of the content I serve on the NAS is via the web portal (HTTPS over port 5001) I can access all the "Apps" on the NAS, such as photo gallery, calendar, and more. 

I have also deployed web servers temporarily. The Synology app WebStation is essentially a ngnix proxy server that can redirect traffic to php or python web servers (flask, specifically), or serve static content.
I decided to run a build script on a separate computer to make a static web page, and then serve it statically on the NAS. That way, I needed minimal config on the NAS, and I reduce the risk of messing up security. Remember that you might need to open up extra ports in the router forwarding rules if you add extra services and want to access them over the internet.