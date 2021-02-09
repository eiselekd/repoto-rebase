all:
	rm -rf r r_work
	mkdir -p r; cd r; git init --bare
	git clone r r_work
	cp Readme.txt $(CURDIR)/r_work/Readme.txt
	git -C $(CURDIR)/r_work add Readme.txt
	git -C $(CURDIR)/r_work commit -m 'init master'
	git -C $(CURDIR)/r_work push origin HEAD:master
	git -C $(CURDIR)/r_work checkout -b branch_a
	cp file_a.txt $(CURDIR)/r_work/file_a.txt
	git -C $(CURDIR)/r_work add file_a.txt
	git -C $(CURDIR)/r_work commit -m 'master_file_a.txt'
	git -C $(CURDIR)/r_work push origin HEAD:branch_a
	git -C $(CURDIR)/r_work checkout -b branch_b
	cp file_b.txt $(CURDIR)/r_work/file_b.txt
	git -C $(CURDIR)/r_work add file_b.txt
	git -C $(CURDIR)/r_work commit -m 'master_file_b.txt'
	git -C $(CURDIR)/r_work push origin HEAD:branch_b
	# master
	git -C $(CURDIR)/r_work checkout master
	cp Readme_master0.txt $(CURDIR)/r_work/Readme.txt
	git -C $(CURDIR)/r_work commit --all -m 'init master'
	git -C $(CURDIR)/r_work push origin HEAD:master
