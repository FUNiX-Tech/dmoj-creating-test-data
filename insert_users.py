user_quantity = 5
cloned_username_prefix = 'v3niceclone'
password = 'pbkdf2_sha256$260000$oWs6Mt5UsuhMFMG9rI1DLk$pFoobYSv5RZ+lr1oLNc/JmGNZs1KUvGEF5oIW0e9smg=' # funix.edu.vn

# profile
profile_sql = "insert into judge_profile (id, timezone ,points , performance_points, problem_count, ace_theme, last_access, ip, display_rank, mute, is_unlisted, user_script, is_totp_enabled, language_id, user_id, is_webauthn_enabled, last_totp_timecode, username_display_override, is_banned_from_problem_voting, site_theme, math_engine) values (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s, %s, %s, %s)"

from init_db import db
cursor = db.cursor()

# get template user data
cursor.execute("select * from auth_user where is_superuser = 0 and is_active = 1 and is_staff = 0 limit 1")
template_user_values = cursor.fetchall()[0]

# get template profile data
cursor.execute("select * from judge_profile where user_id = {}".format(int(template_user_values[0])))
template_profile_values = cursor.fetchall()[0]

i = 1
while i <= user_quantity: 
    try:
        # insert user
        cloned_username = cloned_username_prefix + str(i)
        cloned_email = cloned_username + '@gmail.com'
        values = list(map(lambda item: str(item), list(template_user_values)[1:]))
        print(values)
        values[0] = password
        values[3] = cloned_username
        values[4] = 'Cloned Firsname'
        values[5] = 'Cloned Lastname'
        values[6] = cloned_email
        values = tuple(values)
        
        cursor.execute("insert into auth_user values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (None,)+ values)
        db.commit()
        print('insert user {}'.format(cloned_username))
        
        # get created user_id 
        select_sql = "SELECT * FROM auth_user where username = '{}'".format(cloned_username)
        cursor.execute(select_sql)
        created_user = cursor.fetchall()[0]
        created_user_id = created_user[0]
        
        # insert profile
        profile_values = list(template_profile_values)
        profile_values[0] = created_user_id
        profile_values[20] = created_user_id
        profile_values = tuple(profile_values)

        cursor.execute("insert into judge_profile values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", profile_values)
        db.commit()
        print('insert profile {}'.format(created_user_id))
        
    except Exception as ex: 
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    i += 1