.PHONY: install
install:
	brew install qsv
	pip install -r requirements.txt

.PHONY: download
download:
	wget https://www.data.gouv.fr/fr/datasets/r/f868cca6-8da1-4369-a78d-47463f19a9a3 -O export-dataset.csv

.PHONY: data
QSV_FILTER="archived == 'False' and tonumber(resources_count) > 0"
QSV_COLUMNS=id,title,description,tags
data: download
	qsv luau filter -d";" $(QSV_FILTER) export-dataset.csv | qsv select $(QSV_COLUMNS) > datasets-filtered.csv
