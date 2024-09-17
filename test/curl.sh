curl -v -X 'POST' \
 'http://localhost:31976/v1/en/dico_pos/postag?input=terms' \
  -H "Content-Type: text/csv" \
  -d 'id	text
http://data.loterre.fr/ark:/67375/P66#xl_en_9278939f	qualities
http://data.loterre.fr/ark:/67375/P66#xl_en_60f6687f	quality
http://data.loterre.fr/ark:/67375/P66#xl_en_696ab94f	material entities
http://data.loterre.fr/ark:/67375/P66#xl_en_c0a4dac9	material entity
http://data.loterre.fr/ark:/67375/P66#xl_en_ded9af98	processes'


cat <<EOF | curl --proxy "" -X POST --data-binary @- 'http://localhost:31976/v1/en/dico_pos/postag?input=terms'
id	text
http://data.loterre.fr/ark:/67375/P66#xl_en_9278939f	qualities
http://data.loterre.fr/ark:/67375/P66#xl_en_60f6687f	quality
http://data.loterre.fr/ark:/67375/P66#xl_en_696ab94f	material entities
http://data.loterre.fr/ark:/67375/P66#xl_en_c0a4dac9	material entity
http://data.loterre.fr/ark:/67375/P66#xl_en_ded9af98	processes
EOF
