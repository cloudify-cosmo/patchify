from __future__ import print_function
import os
import sys
import tempfile
import subprocess

CRON_USER = 'root'  # has to be root to be able to stop mgmtworker
SCHEDULE = '*/10 * * * *'
SCRIPT_NAME = '/etc/cloudify/watchdog.sh'
WATCHDOG_SCRIPT = """
#!/bin/bash
set -eux

# if mgmtworker isn't running, there is nothing to do. We must be a replica.
systemctl status cloudify-mgmtworker || exit 0

BLUEPRINT_DIR=
BLUEPRINT_NAME=watchdog-test-bp
DEPLOYMENT_NAME=watchdog-test-dep

function cleanup {
   # if the execution was stuck, remove it from the db
   sudo -upostgres psql cloudify_db -c "delete from executions e using deployments d where e._deployment_fk = d._storage_id and d.id='$DEPLOYMENT_NAME';"
   cfy dep del $DEPLOYMENT_NAME || true
   sleep 3 # allow the deployment to be deleted
   cfy blu del $BLUEPRINT_NAME
   [ -d $BLUEPRINT_DIR ] && rm -rf $BLUEPRINT_DIR
}

function make_bp_file {
    cat >$1 <<EOF
tosca_definitions_version: cloudify_dsl_1_3
imports:
  - http://www.getcloudify.org/spec/cloudify/4.3.1/types.yaml
node_templates: {}
EOF
}

function upload_blueprint {
    BLUEPRINT_DIR=$(mktemp -d)
    make_bp_file $BLUEPRINT_DIR/bp.yaml
    cfy blu up -b $BLUEPRINT_NAME $BLUEPRINT_DIR/bp.yaml
}

function create_deployment {
    cfy dep cre -b $BLUEPRINT_NAME $DEPLOYMENT_NAME
}

function all_executions_finished {
    cfy exec li -d $1 | grep create_deployment_environment | grep -E 'terminated|completed'
}

function wait_for_deployment {
    for i in $(seq 0 10); do
       all_executions_finished $DEPLOYMENT_NAME && break
       sleep 1
       if [ $i -eq 10 ]; then
          false
       fi
    done
}
function on_failure {
    systemctl stop cloudify-mgmtworker
}

# cleanup first in case a previous run was forcibly aborted and left the bp/dep around
cleanup || true
trap cleanup EXIT

upload_blueprint
create_deployment
wait_for_deployment || on_failure


"""


def deploy_script():
    with open(SCRIPT_NAME, 'w') as f:
        f.write(WATCHDOG_SCRIPT)
    subprocess.check_output(['chmod', '+x', SCRIPT_NAME])

def setup_cron():
    try:
        previous_cron = subprocess.check_output(['crontab', '-lu', CRON_USER])
    except subprocess.CalledProcessError as e:
        previous_cron = ''
    if SCRIPT_NAME in previous_cron:
        print('Already set up, exiting')
        sys.exit(1)
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(previous_cron)
        f.write('{0} {1}\n'.format(SCHEDULE, SCRIPT_NAME))
    subprocess.check_output(['crontab', f.name])
    os.unlink(f.name)
    print('Added {0} to cron for {1}'.format(SCRIPT_NAME, CRON_USER))


def main():
    deploy_script()
    setup_cron()

if __name__ == '__main__':
    main()

