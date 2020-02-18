# marathon-haproxy-healthcheck

A utility for checking the health of HAProxy routes and restarting haproxy if necessary.

Can be extended to do more but for now, it's mainly a cron-job that restarts haproxy if any one of the public urls is down.

## Deployment

This is meant to be deployed on marathon and takes the following environment variables:

```bash
# periodicity of execution in cron notation
export CRON=
# set to 1 when deploying in cron mode
export FORCE_CRON=
# marathon API settings
export MARATHON_URL=
export MARATHON_USERNAME=
export MARATHON_PASSWORD=
```
