cd ~/dev/brasilprev-challenge

docker build -t bprev . 

docker run -it -e TZ=America/Sao_Paulo --rm -p 5000:5000 --name bprev --env-file .env bprev
