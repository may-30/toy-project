import boto3

def sso(aws_access_key_id, aws_secret_access_key, aws_session_token):
    # 1. common variables.
    # boto3 session.
    session = boto3.session(
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        aws_session_token = aws_session_token
    )
    # client.
    sso_admin_client = session.client('sso-admin')
    identity_store_client = session.client('identitystore')
    
    # 2. identity store.
    identity_store_id_responses = sso_admin_client.list_instances()
    for response in identity_store_id_responses['Instances']:
        identity_store_id = response['IdentityStoreId']
    
    # 3. group list.
    sso_group_id_dict = {}
    sso_group_list_responses = identity_store_client.list_groups(
        IdentityStoreId = identity_store_id
    )
    for response in sso_group_list_responses['Groups']:
        sso_group_id_dict[response['GroupId']] = response['DisplayName']
    sso_group_id_lists = list(sso_group_id_dict.keys())

    # 4. group membership.
    user_id_lists = []
    for sso_group_id in sso_group_id_lists:
        sso_group_memberships_list_responses = identity_store_client.list_group_memberships(
            IdentityStoreId = identity_store_id,
            GroupId = sso_group_id
        )

        for response in sso_group_memberships_list_responses['GroupMemberships']:
            user_id_value = response['GroupId'] + ':' + response['MemberId']['UserId']
            user_id_lists.append(user_id_value)
    user_id_lists = sorted(user_id_lists)
    
    # 5. refine data for group name, user id.
    sso_group_name_lists = []
    sso_user_id_lists = []

    for idx in user_id_lists:
        sso_group_name_lists.append(sso_group_id_dict[idx.split(':', 1)[0]])
        sso_user_id_lists.append(idx.split(':', 1)[1])
    
    # 6. username.
    sso_user_name_lists = []

    for user_id in sso_user_id_lists:
        user_name_list_responses = identity_store_client.describe_user(
            IdentityStoreId = identity_store_id,
            UserId = user_id
        )

    sso_user_name_lists.append(user_name_list_responses['UserName'])

    # 7. refine data for combine group name & user name
    sso_lists = []
    sso_length = len(sso_group_name_lists)
    for idx in range(sso_length):
        sso_lists.append(sso_group_name_lists[idx] + ':' + sso_user_name_lists[idx])
    # sso_lists.sort()
    sso_lists = sorted(sso_lists)

    # 8. return.
    return sso_lists