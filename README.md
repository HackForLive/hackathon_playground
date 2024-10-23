README


# 1. Architecture

Application should be structured logically into separate modules.
We should have frontend - user interface which is decoupled from backend (streamlit could a good
candidate) and a backend which exposes HTTP API and extracts user inputs, tranform them into data form to call AI services (here we can utilize RAG or other architectures which leverages external DB storage). Retrieves response, process the results and send them back to user (here FAST Api could be a good candidate). As storage for the data we can use local sqlite db or connect to azure db (should be driven by configuration).


Components
* Frontend (streamlit)
* Backend (FastAPI)
* Database (sqlite or azure db)
* AI service (Azure Open AI / other)

# 1.1 DB

- map objects by schemas from database
- create a correct model (storing date for instance to have most relevant data by query)
- handling objects in db should be database agnostic (does not matter whether use local sqlite instance or cloud db instance)


# 1.2 Backend

- Expose public HTTP endpoints for frontend (marshall objects as json)
- Manage data in dabatase (CRUD operations)
- Connect and query to OPEN AI or other service endpoints
- Orchestrate query from frontend 


# 1.3 User Interface 

- async communication with backend (better user experience while waiting for command to be executed) 

# 1.4 Configuration

Create configuration files for different scenarios, DO NOT hardcode them in application.

- db connection (local or azure db)
- exposed HTTP port by backend (shared between backend and frontend)
- exposed frontend/backend host name (expected to be same)
- AI service configuration
- secrets (API tokens)

# 1.5 Nice to Have

- docker containerization


# 2. How To

To install package
create venv
```
python3 -m venv venv
```

activate
```
source ./venv/bin/activate
```

to install module
```
pip install -e .
```


To run Fast API from root directory with hot reload exposed on HTTP port 8000
```
uvicorn examples.frontend.fast_api:app --reload --host=0.0.0.0 --port=8000
```

To run stream lit application
```
streamlit run examples/frontend/stream_lit.py
```

# 3. To Check

sqlalchemy/fastapi + azure db/ sqlite

