# HISBusTourCrawler

## Setup Environment

Setup the nessary aws secrets to connect to bucket

```shell=
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
$ export AWS_DEFAULT_REGION=us-west-2
```

Get you github OAuth token(bearer) - [tutorial](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## Crawl HIS Bus Tour

```shell=
$ ./trigger_his_bus_tour_crawler.sh [YOUR GITHUB TOKEN] [THE CONFIG FILE NAME (can be any file in s3://BUCKET/search_params/)]
```

## Collect The Result

The data crawled would be upload to `s3://BUCKET/tour_details/`.
