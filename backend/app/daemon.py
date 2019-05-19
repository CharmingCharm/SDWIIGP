from .extension import db, rq
from .model import Submission, TestSet, TestSet
from flask import current_app, json
from .helper import random_string
from .controller import str_time
from datetime import datetime
import os, subprocess

def log_system_error(msg):
	print('=== System error!')
	print(msg)
	print()

@rq.job
def judge(sid):
	print('\n=== Judge submission #' + str(sid))
	judge_dir = current_app.config['JUDGER_DIR']
	if not os.path.exists(judge_dir):
		os.mkdir(judge_dir)
	sub = Submission.query.filter_by(sid = sid).first()
	if not sub:
		log_system_error('The submission is not found.')
		return 1
	if not sub.problem:
		log_system_error('The problem of the submission is not found.')
		sub.result = 'system_error'
		return 2
	if not sub.problem.testset:
		log_system_error('The related problem is not linked to any testset.')
		sub.result = 'system_error'
		return 3
	sub.result = 'running'
	sub.testset = sub.problem.testset
	result = []
	score = 0.0
	for test in sub.testset.tests.all():
		test_code = sub.code + '\n\n' + test.code
		test_file = os.path.join(judge_dir, random_string() + '_' + str(sid) + '.py')
		f = open(test_file, 'w')
		f.write(test_code)
		f.close()

		p = subprocess.Popen('python3 ' + test_file, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		output = p.communicate()[1].decode(encoding = "utf-8", errors = "ignore")
		returncode = p.returncode
		test_score = float(str(test.score)) * (0 if returncode or output else 1)
		print('{ test_id: ', test.test_id, ', returncode: ', returncode, ', score:', test_score, ' }', sep='')

		score = score + test_score
		result.append({
			'test_id': test.test_id,
			'score': test_score,
			'output': output,
		})
		os.remove(test_file)
	print()
	sub.result = json.dumps(result)
	sub.score = score
