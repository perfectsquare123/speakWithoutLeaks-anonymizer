# speakWithoutLeaks-data-level-privacy-preserving-pipeline-for-llm

1. Create a python virtual environment and activate it
   Navigate to the root directory of the project and execute the following commands:

```bash
 python -m venv .venv
 ./.venv/Scripts/activate
```

2. Download necessary package

```bash
pip install -r requirements.txt

# install NER model that intended to use
python -m spacy download en_core_web_sm
```

3. Run

```bash
PYTHONPATH=. python cli/run_pipeline.py \
  --input data/sample_test_input.csv \
  --output output/sanitized_test_output.csv \
  --config config/default_config.yaml \
  --text-column text \
  --label-column label \
  --num-classes 4
```

```bash
PYTHONPATH=. python cli/reverse_text_cli.py \
  --input output/sanitized_model_response.txt \
  --output output/reversed_model_response.txt \
  --mapping output/mapping
```

```bash
PYTHONPATH=. python cli/decrypt_text_cli.py \
  --input output/encrypted.txt \
  --output output/decrypted.txt \
  --method fpe \
  --config config/default_config.yaml
```
