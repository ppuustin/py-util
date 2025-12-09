import os, sys, time

def main(props):
    print(props)

# ------------------------------------------

if __name__ == '__main__':
    props = {} 
    props['prop'] = 'xxx'

    start = time.time()
    main(props)
    print('DONE in:', time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))

'''

aws credentials:

[src-acc]
aws_access_key_id = xxx
aws_secret_access_key = yyy

[some-dev]
credential_process = <usr>/vegas-credentials assume --profile=some-dev

aws config:

[profile src-acc]
mfa_serial = arn:aws:iam::zzz:mfa/some.name

[default]
region = eu-west-1
duration_seconds=28800
credential_process = <usr>/vegas-credentials assume --profile=default
role_session_name = "some.name@domain.com"
vegas_source_profile=src-acc

[profile my-dev]
region = eu-west-1
duration_seconds = 28800
credential_process = <usr>/vegas-credentials assume --profile=some-dev
role_session_name = "some.name@domain.com"
vegas_role_arn = arn:aws:iam::yyy:role/SRC-ROLE
vegas_source_profile = src-acc


set AWS_PROFILE=my-dev

:: set tfenv=%UserProfile%\tfenv\tf117
set tfenv=%UserProfile%\tfenv\tf119
set PATH=%PATH%;%penv%\Scripts;%penv%\Lib\site-packages\keyrings;%tfenv%

terraform init -reconfigure && ( pause ) || ( pause )
terraform init build.yaml && ( pause ) || ( pause )
terraform build build.yaml && ( pause ) || ( pause )
terraform apply && ( pause ) || ( pause )
terraform force-unlock <some-id> && ( pause ) || ( pause )

'''
