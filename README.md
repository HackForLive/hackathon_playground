README


# 1. Architecture

....

# 2. How To

# 2.1 Conda (Miniconda) Installation

Install conda from (https://docs.anaconda.com/miniconda/)

# 2.2 Activate Conda

Windows example:
```
cd C:\Users\<User>\miniconda3\condabin
.\conda.bat init powershell
```

Linux example:
```
Activate Conda (Linux eval "$(/home/malisha/miniforge3/bin/conda shell.bash hook)")
```

# 2.3 Create Conda Environment

This is one time action. To create environment named hackathon_venv:
```
conda env create --file .\environment.yaml -n hackathon_venv
conda activate hackathon_venv
```

Optional Commands:
```
(go base) conda activate
(delete) conda env remove --name hackathon_venv
```

# 2.4 Install Python Module named genai_hackthon

To install package, run 
```
run.bat install
```


# 2.5 Build And Run

After each change project needs to be build! To build the project run:
```
run.bat build
```

Now you need to setup free azure account for month (we can of course create alternative way).
In your azure account you need to provision Azure OpenAI service with some model deployment.After you create azure account and Azure OpenAI service, you need to create file name .env with following content:
 
```
AZURE_ENDPOINT=https://azure-openai-my-test.openai.azure.com/
AZURE_OPENAI_API_KEY=xxxxxxx
AZURE_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_API_VERSION=2024-02-01
```

where azure endpoint is available in your Azure OpenAI service settings, azure openai api key is secret also available in you Azure OpenAI service, azure deployment name and azure api version should be also available (I will check).
The config is ignored in .gitignore because it contains secrets so anyone could use it on your behalf! 


Run streamlit UI

```
run.bat streamlit
```

Get help

```
run.bat build --help
```
