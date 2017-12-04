task1:
	echo sudo for pip installations
	sudo pip install -r requirements.txt
	echo running two workers in background
	./runworker.sh & ./runworker.sh &
	python task1.py
task2:
	echo sudo for pip installations
	sudo pip install -r requirements.txt
	echo running two workers in background
	./runworker.sh & ./runworker.sh &
	python task2.py
