#! /usr/bin/bash

for i in buildings/*; do
	if [[ -e "$i/dvc.yaml" ]]; then
		echo "Running dvc workflow for ${i##*/}."
		cd buildings/i
  		poetry run dvc exp run dvc.yaml --force --dry
		cd ../..
	else
		echo "No dvc workflow exists for ${i##*/}."
fi
done
