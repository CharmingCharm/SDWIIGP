while True:
	path = input()
	print("{{ url_for('static', filename='%s') }}" % path.lstrip('/').replace('static/', ''))
