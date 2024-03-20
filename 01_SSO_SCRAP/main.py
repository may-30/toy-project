from modules import sso, excel

if __name__ == '__main__':
    # 1. input variables
    ct_url = input('ct url: ')
    email_id = input('email id: ')
    email_pw = input('email pw: ')
    otp = input('otp: ')
    account_id = input('account id: ')
    profile_name = input('profile name: ')

    # 2. crowl
    aws_access_key_id, aws_secret_access_key, aws_session_token = crowl.crowl(ct_url, email_id, email_pw, otp, account_id, profile_name)

    # 3. sso
    sso_lists = sso.sso(aws_access_key_id, aws_secret_access_key, aws_session_token)

    # 4. excel
    excel.excel(sso_lists)