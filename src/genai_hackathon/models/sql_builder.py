import json
import sqlite3

from genai_hackathon.services.azure_openai_service import AzureOpenAIService
from genai_hackathon.utils.environment import get_env_var


def json_to_sql(query_json):
    # Extract main components from JSON
    if 'columns_of_global_oil_and_gas_main' in query_json:
        retrieved_columns = query_json['columns_of_global_oil_and_gas_main']
    else:
        retrieved_columns = query_json['columns_of_global_oil_and_gas_reserves']

    table_name = query_json["table_name"]
    columns = ", ".join(retrieved_columns)
    conditions = query_json["conditions"]
    order_by = query_json.get("order_by", "asc")

    # Build WHERE clause from conditions
    where_clauses = []
    for condition in conditions:
        column = condition["column"]
        operator = condition["operator"]
        value = condition["value"]

        # Handle column vs static value conditions
        if isinstance(value, dict) and "column_name" in value:
            value_clause = f"{value['column_name']}"
        else:
            value_clause = f"'{value}'" if isinstance(value, str) else str(value)

        where_clauses.append(f"{column} {operator} {value_clause}")

    where_clause = " AND ".join(where_clauses)

    # Construct SQL query
    sql_query = f"SELECT {columns} FROM {table_name} WHERE {where_clause} ORDER BY id {order_by};"
    return sql_query


def execute_query(sql_query):
    # Connect to your database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch all results
    results = cursor.fetchall()

    # Close the connection
    conn.close()
    
    return results


def sql_pipeline(query_json):
    # Convert JSON to SQL
    sql_query = json_to_sql(query_json)
    
    # Execute the SQL query and get results
    results = execute_query(sql_query)
    
    return results


class SQLBuilder:
    def __init__(self) -> None:

        self._service = AzureOpenAIService(
            api_key=get_env_var("AZURE_OPENAI_API_KEY"),
            api_version=get_env_var("AZURE_API_VERSION"),
            azure_endpoint=get_env_var("AZURE_ENDPOINT")
        )
        self.deployment_name = get_env_var("AZURE_DEPLOYMENT_NAME")

    def build_execute_sql(self, prompt: str) -> str:
            # Creating a request with structured output for guardrail check
            response = self._service.client.chat.completions.create(
                model = "gpt-4o-2024-08-06",
                messages = [
                  {
                    "role": "system",
                    "content": prompt
                  },
                  {
                    "role": "user",
                    "content": "look up all my orders in may of last year that were fulfilled but not delivered on time"
                  }
                ],
                tools = [
                  {
                    "type": "function",
                    "function": {
                      "name": "query",
                      "description": "Execute a query.",
                      "strict": True,
                      "parameters": {
                        "type": "object",
                        "properties": {
                          "table_name": {
                            "type": "string",
                            "enum": ['global_oil_and_gas_main', 'global_oil_and_gas_reserves']
                          },
                          "columns_of_global_oil_and_gas_main": {
                            "type": "array",
                            "items": {
                              "type": "string",
                              "enum": [
                                  '',
                                  "Unit ID",
                                  "Unit Name",
                                  "Unit name local script",
                                  "Fuel type",
                                  "Unit type",
                                  "Country",
                                  "Subnational unit (province, state)",
                                  "Latitude",
                                  "Longitude",
                                  "Location accuracy",
                                  "Status",
                                  "Status year",
                                  "Discovery year",
                                  "FID Year",
                                  "Production start year",
                                  "Operator",
                                  "Owner",
                                  "Parent",
                                  "Basin",
                                  "Concession / block",
                                  "Project or complex",
                                  "Government unit ID",
                                  "Wiki URL"
                              ]
                            }
                          },
                          "columns_of_global_oil_and_gas_reserves": {
                            "type": "array",
                            "items": {
                              "type": "string",
                              "enum": [
                                  '',
                                  "Unit ID", 
                                  "Unit name", 
                                  "Country", 
                                  "Wiki URL", 
                                  "Production/reserves",
                                  "Fuel description", 
                                  "Reserves classification (original)",
                                  "Quantity (original)", 
                                  "Units (original)", "Data year",
                                  "Quantity (converted)", 
                                  "Units (converted)"
                              ]
                            }
                          },
                          "conditions": {
                            "type": "array",
                            "items": {
                              "type": "object",
                              "properties": {
                                "column": {
                                  "type": "string"
                                },
                                "operator": {
                                  "type": "string",
                                  "enum": ["=", ">", "<", ">=", "<=", "!="]
                                },
                                "value": {
                                  "anyOf": [
                                    {
                                      "type": "string"
                                    },
                                    {
                                      "type": "number"
                                    },
                                    {
                                      "type": "object",
                                      "properties": {
                                        "column_name": {
                                          "type": "string"
                                        }
                                      },
                                      "required": ["column_name"],
                                      "additionalProperties": False
                                    }
                                  ]
                                }
                              },
                              "required": ["column", "operator", "value"],
                              "additionalProperties": False
                            }
                          },
                          "order_by": {
                            "type": "string",
                            "enum": ["asc", "desc"]
                          }
                        },
                        "required": ["table_name", "columns_of_global_oil_and_gas_main", "columns_of_global_oil_and_gas_reserves", "conditions", "order_by"],
                        "additionalProperties": False
                      }
                    }
                  }
                ]
            )

            query_result = sql_pipeline(response.choices[0].message.tools[0].function.parameters)
            return query_result

