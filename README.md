# CMPS-460-Project

uv run flask --app app run


curl -i -X POST http://127.0.0.1:5000/tags \
  -H 'Content-Type: application/json' \
  -d '{"name":"The cooler demo tag"}'