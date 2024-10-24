README


# 1. Architecture

....

# 2. How To

Install Conda (https://docs.anaconda.com/miniconda/)
Activate Conda (Linux eval "$(/home/malisha/miniforge3/bin/conda shell.bash hook)")

Init environemnt:
```
conda env create --file environment.yaml -n hackathon_venv
conda activate hackathon_venv
(go base) conda activate
(delete) conda env remove --name hackathon_venv
```


Install package from cmd
```
run.bat install
```


Build project from cmd

* Windows
    ```
    run.bat build
    ```
* Linux
    ```
    bash run.sh build
    ```

Install package
```
pip install genai_hackathon
```

Setup 
```
AZURE_ENDPOINT=https://azure-openai-my-test.openai.azure.com/
AZURE_OPENAI_API_KEY=xxxxxxx
AZURE_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_API_VERSION=2024-02-01
```

Run streamlit UI

```
run.bat streamlit
```

Get help

```
run.bat build --help
```
