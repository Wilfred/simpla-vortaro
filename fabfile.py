from fabric.api import env, cd, run


env.hosts = ['simplavortaro@server.simplavortaro.org']
env.directory = "/home/simplavortaro/src/simpla-vortaro"
env.activate   = "source /home/simplavortaro/venv/bin/activate"


def virtualenv(command):
    run(env.activate + ' && ' + command)


def deploy():
    with cd(env.directory):
        run('git checkout master')        
        run('git fetch')
        run('git reset --hard origin/master')
        virtualenv('pip install -r requirements.pip')

        virtualenv('python manage.py syncdb')

    restart()


def restart():
    run("sudo supervisorctl restart simplavortaro")

