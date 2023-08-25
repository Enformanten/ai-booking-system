#! /usr/bin/bash

for i in buildings/*; do
	if [[ -e "$i/dvc.yaml" ]]; then
		echo "Running dvc workflow for ${i##*/}."
  		poetry run dvc exp run $i/dvc.yaml --force --dry
	else
		echo "No dvc workflow exists for ${i##*/}."
fi
done
