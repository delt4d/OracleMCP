import sys, os, oracledb, csv, io
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Oracle")

def log(mensagem):
    print(f"[DEBUG] {mensagem}", file=sys.stderr)

@mcp.tool()
def execute_query(query: str, params: dict|None = None, max_rows: int = 1000) -> str:
    """
    Executa SQL no Oracle e retorna o resultado em CSV.
    
    Inputs:
    - query (str): Comando SQL (ex: "SELECT * FROM tab WHERE id = :id").
    - params (dict): Mapeamento de bind variables (ex: {"id": 1}).
    - max_rows (int): Limite de linhas para o fetch.
    
    Output:
    - String em formato CSV (UTF-8).
    - Primeira linha: Nomes das colunas.
    - Linhas subsequentes: Valores dos registros.
    - Em caso de erro, retorna string iniciando com 'ERRO:'.
    """
    log(f"\nExecutando query: {query}")
    if params: log(f"Parametros: {params}")

    try:
        conn = oracledb.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_CONNECTION_STRING")
        )
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

        with conn.cursor() as cur:
            cur.execute(query, params or {})
            
            if cur.description:
                writer.writerow([d[0] for d in cur.description])
                for row in cur.fetchmany(max_rows):
                    writer.writerow([
                        v.isoformat() if hasattr(v, 'isoformat') else v 
                        for v in row
                    ])
            
        res = output.getvalue()
        conn.close()

        log(f"\nQuery executada com sucesso: {query}")

        return res if res else "Sucesso: Comando executado (sem retorno)."

    except Exception as e:
        log(f"\nErro ao executar query: {query}")
        return f"ERRO: {str(e)}"

if __name__ == "__main__":
    log("Iniciando servidor MCP Oracle...")
    mcp.run()