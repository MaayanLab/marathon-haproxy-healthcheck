USER=app

cd /app/

# Use .env.example to get relevant env args and put them in .env for runtime loading
awk -F'=' '{ print $1"="ENVIRON[$1] }' /app/.env.example > /app/.env

if [ "$1" == "bash" ]; then
  echo "Running in bash mode..."
  bash
elif [ "$1" == "cron" ] || [ "${FORCE_CRON}" -eq 1 ]; then
  echo "Running in cron mode..."
  date
  set -x
  (
    echo "${CRON} (date && cd /app/ && sudo -u ${USER} /app/healthcheck.py) >> /proc/1/fd/1 2>/proc/1/fd/2"
  ) >> /etc/cron.d/healthcheck
  chmod 700 /etc/cron.d/healthcheck
  crontab /etc/cron.d/healthcheck
  cron -f
else
  echo "Running in single-shot mode..."
  set -x
  sudo -u $USER /app/healthcheck.py $@
fi
