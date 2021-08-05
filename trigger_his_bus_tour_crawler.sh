#!/usr/bin/env bash

GITHUB_TOKEN="$1"
SEARCH_PARAMS="$2"
IMAGE="mi_comet_crawler:0.3"
BUCKET_NAME="vrcrawler-info"

# Trigger request sender function
function start_crawler() {

payload=$( cat <<EOF
{
    "ref":"main",
    "inputs": {
        "image": "$2",
        "script": "$3",
        "storage_config": "$4",
        "crawl_config": "$5"
    }
}
EOF
)

    echo "$payload"

    curl -H "Authorization: token $1" \
      -X POST \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/repos/miComet/HISBusTourCrawler/actions/workflows/generalCrawler.yml/dispatches \
      -d "$payload"
}


# Download search param
aws s3 cp s3://$BUCKET_NAME/search_params/$SEARCH_PARAMS ./

if [ $? -ne 0 ]; then
    exit 1
fi


# Set script name and storage config
script_name='crawl_his_bus_tour.py'
storage_config_raw=$( cat <<EOF
{
    "type": "s3",
    "key": "$AWS_ACCESS_KEY_ID",
    "secret": "$AWS_SECRET_ACCESS_KEY",
    "bucket_name": "$BUCKET_NAME",
    "dir": "tour_details/"
}
EOF
)


# Crawl detail urls
start_crawler \
    "$GITHUB_TOKEN" \
    "$IMAGE" \
    "$script_name" \
    "$( echo $storage_config_raw | base64 | sed 's/"//g' | awk '{print}' ORS='' )" \
    "$( cat $SEARCH_PARAMS | base64 | sed 's/"//g' | awk '{print}' ORS='' )"
