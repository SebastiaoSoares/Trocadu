"""
Este módulo inicia o servidor de desenvolvimento para a aplicação Trocadu. API utilizando Uvicorn. Ele configura o host, a porta e habilita o
recarregamento automático para facilitar o desenvolvimento.
"""

import uvicorn

if __name__ == "__main__":
    APP_TARGET = "src.infrastructure.api.app:app"
    
    print(f"Iniciando servidor Trocadu em modo de desenvolvimento...")
    print(f"Alvo: {APP_TARGET}")
    
    uvicorn.run(
        APP_TARGET,
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )
