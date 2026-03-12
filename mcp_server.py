import json
import os
import oracledb

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("OracleQueryServer")


def _get_connection():
    """Cria e retorna uma conexão com o banco Oracle."""
    connection_string = os.getenv("ORACLE_CONNECTION_STRING")
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    return oracledb.connect(f"{user}/{password}@{connection_string}")



@mcp.tool()
def executar_query(query: str, maxRows: int = 1000) -> str:
    """
    Executa uma query SQL no Oracle e retorna os resultados em JSON.

    Args:
        query: Comando SQL a ser executado
        maxRows: Número máximo de linhas a retornar (padrão: 1000)

    Returns:
        JSON string com os resultados da query
    """
    try:
        connection = _get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchmany(maxRows)
        results = []
        for row in rows:
            row_dict = {}
            for col_name, col_value in zip(columns, row):
                if hasattr(col_value, 'isoformat'):  # datetime
                    row_dict[col_name] = col_value.isoformat()
                else:
                    row_dict[col_name] = col_value
            results.append(row_dict)
        cursor.close()
        connection.close()

        return json.dumps({
            "success": True,
            "columns": columns,
            "rows": results,
            "row_count": len(results)
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
