template_problem_code = 'hungry'
cloned_problem_code_prefix = 'clonehungry'
cloned_problem_name_prefix = 'Clone Problem '
cloned_problems_quantity = 2000

from init_db import db
cursor = db.cursor()
sql = 'insert into judge_problem values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    
# get template problem
cursor.execute("select * from judge_problem where code = '{}'".format(template_problem_code))
template_problem_values = cursor.fetchall()[0]

i = 1
while i <= cloned_problems_quantity:
    cloned_code = cloned_problem_code_prefix + str(i)
    cloned_name = cloned_problem_name_prefix + str(i)
    cloned_values = (cloned_code, cloned_name) +  template_problem_values[3:]
    cursor.execute(sql, cloned_values)
    db.commit()
    print('success {}'.format(i))
    i += 1