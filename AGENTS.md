# AGENTS.md

## Repository Purpose

Template for pulling research article pdfs and assessing them to output a CSV file with categories filled in for particular types of information extracted from each article.
See **TASKS.md** for a plain-English description of the pipeline.

---

## Core Steps

1. **Use text files for downloaded research articles to extract patterns per the input/output specifications.**


## After It Runs

1. **Append to `PROMPT_ACTION_LOG.md`** — date, user's exact prompt, model name, actions taken.

---

## Directory Structure

```
scripts/                          Helper scripts
inputs/                           Original CSV file with all journals published in Environmental Data Science journal as of 5/13/26.
outputs/                          Output CSV file with analyzed data. Output JSON file that was used as intermediate to convert to CSV.
examples/                         Examples of output CSV file expectations. Also contains an errors.log file for errors.
```

---

## Input Requirements

Text files for extraction are located at /home/jovyan/data-store/home/shared/esiil/Innovation_Summit_2026/Group_1/extracted_text

---

## Output Requirements


One row per file: A separate line in an output CSV file for each text file (article) assessed, as represented by each object in the JSON STRUCTURE defined below. Each object should include the fields represented in the JSON STRUCTURE that are extracted from the text files. 

Output columns for each text file:

JSON STRUCTURE that will be translated to CSV:
    [{
      "title": "Title of the article.",
      "authors": "Authors of the article.",
      "doi": "DOI of the article.",
      "year": "Year the article was published.",
      "volume": "Volume of the journal the article was published in.",
      "data_type": "Data type analyzed within the article - some options include but are not limited to: images, remote sensing, tabular, text, genomic, etc.",
      "data_type_quote": "Direct quote/s from the article where the data type/s is/are mentioned.",
      "analytical_method": "Analytical method used on the data - some options include but are not limited to: random forest, image classification, prompt engineering, linear regression, graph neural network, etc.",
      "analytical_method_quote": "Direct quote/s from the article where the analytical method/s is/are mentioned.",
      "performance_metrics": "Performance metrics mentioned for the analytical method used - some options include but are not limited to: R^2, AUC, False positive rate, runtime",
      "performance_metrics_quote": "Direct quote/s from the article where the performance metric/s is/are mentioned.",
      "energy_consumption_bool": "Boolean indicating that the article mentions that in it's analytical modeling they assessed the energy consumption of that model.",
      "energy_consumption_quote": "Direct quote/s from the article where the article mentions that in it's analytical modeling they assessed the energy consumption of that model.",
      "hardware_or_system_size_bool": "Boolean indicating that the article mentions the hardware or system size used for analysis.",
      "hardware_or_system_size_quote": "Direct quote/s from the article where the article mentions the hardware or system size used for analysis."
    }]  

---

## Failure Handling

Output failures to the errors.log file in /outputs folder.