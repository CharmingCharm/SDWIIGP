from .extension import db, rq
from .model import Submission, TestSet, TestSet
from flask import current_app, json
from .helper import random_string
from .controller import str_time
from datetime import datetime
import os, subprocess

@rq.job
def judge(sid):
	sub = Submission.query.filter_by(sid = sid).first()
	sub.result = 'running'
	sub.testset = sub.problem.testset
	result = []
	for test in sub.testset.tests.all():
		test_code = sub.code + '\n\n' + test.code
		test_file = os.path.join(current_app.config['JUDGER_DIR'], random_string() + '_' + str(sid) + '.py')
		f = open(test_file, 'w')
		f.write(test_code)
		f.close()

		p = subprocess.Popen('python3 ' + test_file, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		output = p.communicate()[0]
		returncode = p.returncode
		print('returncode =', returncode, 'output: ' + str(output))
		test_score = 0 if returncode or output else 1
		result.append({
			'test_id': test.test_id,
			'score': float(str(test.score)) * test_score,
			'output': output.decode(encoding = "utf-8", errors = "ignore"),
		})
		os.remove(test_file)
	sub.result = json.dumps(result)
