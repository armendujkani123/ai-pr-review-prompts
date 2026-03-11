.PHONY: test smoke

test:
	python3 -m unittest discover -s tests -v

smoke:
	python3 pr_review_cli.py --title "Refactor checkout flow" --summary "Moves discount logic into a service object" --mode general
