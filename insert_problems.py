template_problem_code = 'hungry'
cloned_problem_code_prefix = 'v1clonehungry'
cloned_problem_name_prefix = 'Clone Problem '
cloned_problems_quantity = 2000

from init_db import db
cursor = db.cursor()
sql = 'insert into judge_problem values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    
# get template problem
cursor.execute("select * from judge_problem where code = '{}'".format(template_problem_code))
template_problem_values = cursor.fetchall()[0]

i = 1
while i <= cloned_problems_quantity:
    try:
        cloned_code = cloned_problem_code_prefix + str(i)
        cloned_name = cloned_problem_name_prefix + str(i)
        cloned_values = (None, cloned_code, cloned_name) +  template_problem_values[3:]
        cursor.execute(sql, cloned_values)
        db.commit()
        print('success {}'.format(i))
    except: 
        print("problem already exists {}".format(cloned_code))
    finally: 
        i += 1
        
    
# insert problem types and lanuages
problemtype_id = 1

# get all lanuage ids
cursor.execute('select id from judge_language')
language_ids = list(map(lambda item: item[0], cursor.fetchall()))
language_ids.sort()


j = 1
while j <= cloned_problems_quantity:
    # types
    try:
        created_problem_code = cloned_problem_code_prefix + str(j)
        cursor.execute("select * from judge_problem where code = '{}'".format(created_problem_code))
        created_problem_id = cursor.fetchall()[0][0]
        cursor.execute('insert into judge_problemtype values (%s, %s, %s)', (None, created_problem_id, problemtype_id))
        db.commit()
        print('add type for problem {}'.format(created_problem_code))
    except Exception as ex: 
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    
    # languages
    for language_id in language_ids:
        try:
            cursor.execute("insert into judge_problem_allowed_languages values (%s, %s, %s)", (None, created_problem_id, language_id))
            db.commit()
            print("added allowed language: {} - {}".format(created_problem_id, language_id))
        except Exception as ex: 
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
    j += 1
    
