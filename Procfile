worker: chmod +x ./run.sh && chmod +x web.sh
worker: trap '' SIGTERM; bash ./run.sh & bash ./web.sh & wait -n; kill -SIGTERM -$$; wait
