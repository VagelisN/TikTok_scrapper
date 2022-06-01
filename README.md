# TikTok Crawler
This is a project that contains a crawler that extracts challenge trends from TikTok.com, along with a rest API which exposes the gathered data. 

# Installation guide

You need to have Python 3.8+ installed (along with pip for installing dependencies) and playwright. Even if you playwright is present in your system, you might need to run the following unix commands: 
> playwright install-deps
> playwright install

Additionally you need to install the following python dependencies:
* flask
* pymongo
* "pymogno[srv]"
* TikTokApi
* moviepy
* matplotlib

For each dependency missing from your system install it using:

> pip3 install {dependency_name}


# Execution

For the crawler, run the following command:

> python3 crawler.py

For the rest API run the following commands:

```
cd flask-api
flask run --without-threads
```
The '--without-threads' parameter is required due to TikTokApi's inabillity to operate in a multi threaded environment. We use it in our rest API for the purpose of getting video data from an existing video ID. If you don't run the 'makeCompilation' service, you can safely remove it.