# Installation

## Production

Install pipenv

    pip install --user pipenv

Install packages

    pipenv sync

## Development

Install hooks:

    pipenv run pre-commit install -t pre-commit
    pipenv run pre-commit install -t pre-push

# Deployment

Run ansible playbook:

    ansible-playbook ansible.yaml

It requires host `tcb` to be in your inventory. Put the secrets in `/etc/environment`.
