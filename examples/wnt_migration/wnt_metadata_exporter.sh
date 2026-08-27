#!/usr/bin/env bash
##H Copyright Wirepas Oy 2026 licensed under Apache 2.0
##H
##H Please see file LICENSE for full license details.
##H
##H Exports metadata from WNT tables in CSV format
##H
##H Options:
##H   -h : help message
##H   -u : WNT postgres database user name from wnt.env POSTGRES_USER
##H
##H Usage:
##H   wnt_metadata_exporter.sh -u $POSTGRES_USER
##H
##H

POSTGRES_USER=${POSTGRES_USER:-clrobusr324xxd}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-}

usage() {
  grep "^##H" <"$0" | sed -e "s,##H,,g"
  exit 0
}

while getopts "h:u:p:" o; do
  case "${o}" in
  h) usage ;;
  u) POSTGRES_USER=${OPTARG} ;;
  p) POSTGRES_PASSWORD=${OPTARG} ;;
  :)
    echo -e "ERROR: Option -$OPTARG requires an argument \n"
    usage
    ;;
  \?)
    echo -e "ERROR: Invalid option -$OPTARG \n"
    usage
    ;;
  esac
done

# -------------------------------------------------------------
# Available tables
WIREPAS_META=(areas mapbindata mapgroups maps networks nodemeta nodemetamaps systemparameters)

# SQL query to get nodemeta together with building, map and floor information
SQL_LOCATION_AND_METADATA_QUERY="
SELECT
  n.*, mg.mapgroupid as mapgroupid,
  mg.mapgroupname as mapgroupname,
  m.mapid as mapid,
  m.mapname as mapname,
  m.mapfloorindex as mapfloorindex
FROM
  nodemeta n
  LEFT JOIN nodemetamaps nmm ON nmm.nodemetaid = n.id
  LEFT JOIN maps m           ON m.mapid = nmm.maphashid
  LEFT JOIN mapgroups mg     ON mg.mapgroupid = m.mapgroupid;
"

function export() {
  # create metadata directory if not exists
  mkdir -p exported_data
  for table in "${WIREPAS_META[@]}"; do
    table=$(echo -n "${table//[[:space:]]/}")
    echo "Exporting wirepas_meta table: ${table} into ${table}.csv.gz"
    docker exec -t wnt_postgres psql -U "$POSTGRES_USER" -d wirepas-meta -P pager=off -t -c "\copy ${table} TO STDOUT  CSV HEADER;" >exported_data/"$table".csv
  done
  docker exec -t wnt_postgres psql -U "$POSTGRES_USER" -d wirepas-meta -P pager=off --csv -c "$SQL_LOCATION_AND_METADATA_QUERY" >exported_data/JOINED_META.csv
}

export
