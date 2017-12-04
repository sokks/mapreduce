prepare:
	echo sudo for pip installations
	sudo pip install -r requirements.txt
task1:
	echo running two workers in background
	./runworker.sh & ./runworker.sh &
	python task1.py
task2:
	echo running two workers in background
	./runworker.sh & ./runworker.sh &
	python task2.py
gen:
	mkdir -p matricies
	python gen_matricies.py --size 10
task3:
	echo running two workers in background
	./runworker.sh & ./runworker.sh &
	python task3.py --file AB.csv --m1 A --m2 B
