﻿# ethics4everyone

サイバーセキュリティ研究倫理の決定木

This repository houses the open sourced knowledge base and interface for
ethical decision making for cyber security research that was created during the course of
the below research

https://arxiv.org/ftp/arxiv/papers/2011/2011.02661.pdf

https://www.usenix.org/system/files/soups2020_poster_ramirez.pdf

https://arxiv.org/ftp/arxiv/papers/2011/2011.13925.pdf （日本語）

This research was originally conducted at Secom IS Laboratory:

https://www.secom.co.jp/isl/en/research/ethics/

可視化の決定木のツールの実行について、ドッカーのイメージの実行について.docxまでご参照ください。

The purpose of this repository is to provide version control, crowdsourcing, and
public verification of the knowledge base, and  to allow for a publicly accessible server
hosting the decision tree tool used to navigate the knowledge base.

The current master database is stored in master-benchmark_updated_translated_v0.90.csv
It contains both the Japanese and the English versions of the tree.
The first column is Japanese, and the second is English. The third is notes.

xlsx_to_json.py is used to convert the csv knowledge base to JSONs

jsonlabeler.py can then be used to label the json file with the numbering scheme
that the knowledge base/decision tree tool uses

Both xlsx_to_json.py and jsonlabeler.py are used by manually changing the names of the input and output files in the
program file, to convert the knowledge base csv into English and Japanese jsons,
which are placed in graph_server/www/data/

The current incarnation of the visualization tool is based on cytoscape and flask.
The knowledge base files are hard-coded into graph_server/www/app.py and graph_server/www/graph.py
Currently this needs to be manually changed if the file names are changed.

Currently the files used have the name:
eng_labeled_benchmark.json for the English version of the tool
labeled_benchmark.json for the Japanese version.

The tool is hosted at port 5000.
Users can switch between the English and Japanese versions of the tool at any time.

For information about the meaning of each component of the tree and how to 
append to it, see Documentation/DraftingRules.docx

See also https://www.usenix.org/system/files/soups2020_poster_ramirez.pdf for details in English
and https://arxiv.org/ftp/arxiv/papers/2011/2011.13925.pdf for Japanese

The design proposal for crowdsourcing additions to the knowlege base is located in
Documentation/database_maintenance_process.docx

For a detailed description of each of the references listed in this initial 
public release of the tree, see Documentation/EthicalSummaries.docx