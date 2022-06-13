#!/bin/bash

curl -o minifam.hmm.7z https://uk1s3.embassy.ebi.ac.uk/deciphon/minifam.hmm.7z
curl -o minifam.dcp.bz2 https://uk1s3.embassy.ebi.ac.uk/deciphon/minifam.dcp.bz2
curl -o prods_file.tsv https://raw.githubusercontent.com/EBI-Metagenomics/deciphon-api/main/deciphon_api/resources/prods_file.tsv

7z x minifam.hmm.7z -y
bunzip2 minifam.dcp.bz2 -f

curl -X 'POST' \
  'http://127.0.0.1:49329/api/hmms/' \
  -H 'accept: application/json' \
  -H 'X-API-Key: change-me' \
  -H 'Content-Type: multipart/form-data' \
  -F 'hmm_file=@minifam.hmm'

curl -X 'PATCH' \
  'http://127.0.0.1:49329/api/jobs/1/state' \
  -H 'accept: application/json' \
  -H 'X-API-Key: change-me' \
  -H 'Content-Type: application/json' \
  -d '{
  "state": "run",
  "error": ""
}'

curl -X 'POST' \
  'http://127.0.0.1:49329/api/dbs/' \
  -H 'accept: application/json' \
  -H 'X-API-Key: change-me' \
  -H 'Content-Type: multipart/form-data' \
  -F 'db_file=@minifam.dcp'

curl -X 'PATCH' \
  'http://127.0.0.1:49329/api/jobs/1/state' \
  -H 'accept: application/json' \
  -H 'X-API-Key: change-me' \
  -H 'Content-Type: application/json' \
  -d '{
  "state": "done",
  "error": ""
}'

curl -X 'POST' \
  'http://127.0.0.1:49329/api/scans/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "db_id": 1,
  "multi_hits": true,
  "hmmer3_compat": false,
  "seqs": [
    {
      "name": "Homoserine_dh-consensus",
      "data": "CCTATCATTTCGACGCTCAAGGAGTCGCTGACAGGTGACCGTATTACTCGAATCGAAGGGATATTAAACGGCACCCTGAATTACATTCTCACTGAGATGGAGGAAGAGGGGGCTTCATTCTCTGAGGCGCTGAAGGAGGCACAGGAATTGGGCTACGCGGAAGCGGATCCTACGGACGATGTGGAAGGGCTAGATGCTGCTAGAAAGCTGGCAATTCTAGCCAGATTGGCATTTGGGTTAGAGGTCGAGTTGGAGGACGTAGAGGTGGAAGGAATTGAAAAGCTGACTGCCGAAGATATTGAAGAAGCGAAGGAAGAGGGTAAAGTTTTAAAACTAGTGGCAAGCGCCGTCGAAGCCAGGGTCAAGCCTGAGCTGGTACCTAAGTCACATCCATTAGCCTCGGTAAAAGGCTCTGACAACGCCGTGGCTGTAGAAACGGAACGGGTAGGCGAACTCGTAGTGCAGGGACCAGGGGCTGGCGCAGAGCCAACCGCATCCGCTGTACTCGCTGACCTTCTC"
    },
    {
      "name": "AA_kinase-consensus",
      "data": "AAACGTGTAGTTGTAAAGCTTGGGGGTAGTTCTCTGACAGATAAGGAAGAGGCATCACTCAGGCGTTTAGCTGAGCAGATTGCAGCATTAAAAGAGAGTGGCAATAAACTAGTGGTCGTGCATGGAGGCGGCAGCTTCACTGATGGTCTGCTGGCATTGAAAAGTGGCCTGAGCTCGGGCGAATTAGCTGCGGGGTTGAGGAGCACGTTAGAAGAGGCCGGAGAAGTAGCGACGAGGGACGCCCTAGCTAGCTTAGGGGAACGGCTTGTTGCAGCGCTGCTGGCGGCGGGTCTCCCTGCTGTAGGACTCAGCGCCGCTGCGTTAGATGCGACGGAGGCGGGCCGGGATGAAGGCAGCGACGGGAACGTCGAGTCCGTGGACGCAGAAGCAATTGAGGAGTTGCTTGAGGCCGGGGTGGTCCCCGTCCTAACAGGATTTATCGGCTTAGACGAAGAAGGGGAACTGGGAAGGGGATCTTCTGACACCATCGCTGCGTTACTCGCTGAAGCTTTAGGCGCGGACAAACTCATAATACTGACCGACGTAGACGGCGTTTACGATGCCGACCCTAAAAAGGTCCCAGACGCGAGGCTCTTGCCAGAGATAAGTGTGGACGAGGCCGAGGAAAGCGCCTCCGAATTAGCGACCGGTGGGATGAAGGTCAAACATCCAGCGGCTCTTGCTGCAGCTAGACGGGGGGGTATTCCGGTCGTGATAACGAAT"
    },
    {
      "name": "23ISL-consensus",
      "data": "CAGGGTCTGGATAACGCTAATCGTTCGCTAGTTCGCGCTACAAAAGCAGAAAGTTCAGATATACGGAAAGAGGTGACTAACGGCATCGCTAAAGGGCTGAAGCTAGACAGTCTGGAAACAGCTGCAGAGTCGAAGAACTGCTCAAGCGCACAGAAAGGCGGATCGCTAGCTTGGGCAACCAACTCCCAACCACAGCCTCTCCGTGAAAGTAAGCTTGAGCCATTGGAAGACTCCCCACGTAAGGCTTTAAAAACACCTGTGTTGCAAAAGACATCCAGTACCATAACTTTACAAGCAGTCAAGGTTCAACCTGAACCCCGCGCTCCCGTCTCCGGGGCGCTGTCCCCGAGCGGGGAGGAACGCAAGCGCCCAGCTGCGTCTGCTCCCGCTACCTTACCGACACGACAGAGTGGTCTAGGTTCTCAGGAAGTCGTTTCGAAGGTGGCGACTCGCAAAATTCCAATGGAGTCACAACGCGAGTCGACT"
    }
  ]
}'

curl -X 'PATCH' \
  'http://127.0.0.1:49329/api/jobs/2/state' \
  -H 'accept: application/json' \
  -H 'X-API-Key: change-me' \
  -H 'Content-Type: application/json' \
  -d '{
  "state": "run",
  "error": ""
}'

curl -X 'POST' \
  'http://127.0.0.1:49329/api/prods/' \
  -H 'accept: application/json' \
  -H 'X-API-Key: change-me' \
  -H 'Content-Type: multipart/form-data' \
  -F 'prods_file=@prods_file.tsv;type=text/tab-separated-values'

curl -X 'PATCH' \
  'http://127.0.0.1:49329/api/jobs/2/state' \
  -H 'accept: application/json' \
  -H 'X-API-Key: change-me' \
  -H 'Content-Type: application/json' \
  -d '{
  "state": "done",
  "error": ""
}'
