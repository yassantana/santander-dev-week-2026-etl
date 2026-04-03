import requests
import ssl
import os
import time
import json
import csv
from datetime import datetime
from requests.adapters import HTTPAdapter
# Adicione esta nova importação aqui:
from dotenv import load_dotenv 

# 1. Carrega as variáveis do arquivo .env que está na mesma pasta do script
load_dotenv()

# --- Configurações de Acesso (Agora protegidas via Variáveis de Ambiente) ---

# 2. O código agora busca o valor dentro do seu arquivo .env secreto
TOKEN_FIXO = os.getenv("TOKEN_FIXO")
CPF_CNPJ_EMPRESA = os.getenv("CPF_CNPJ_EMPRESA")

# 3. Este comando cria um caminho que funciona em qualquer computador (Windows/Mac/Linux)
# Ele vai criar a pasta "desafio_santander" na Área de Trabalho de quem rodar o código
PASTA_DESAFIO = os.path.join(os.path.expanduser("~"), "Desktop", "desafio_santander")

# Mantemos as URLs e o Limit como estavam
LIMIT = 50
URL_TOKEN = "https://cadimo.imobsoft.com.br:8053/ValidaParceiro"
URL_IMOVEIS = "https://cadimo.imobsoft.com.br:8053/CarregaImoveis"

# Cria a pasta caso ela não exista
os.makedirs(PASTA_DESAFIO, exist_ok=True)

# --- AJUSTE DE SEGURANÇA (O segredo para não dar erro de SSL) ---
class TLS12Adapter(HTTPAdapter):
    def __init__(self, ciphers=None, *args, **kwargs):
        self.ciphers = ciphers
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        ctx = ssl.create_default_context()
        try:
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        except Exception:
            pass
        if self.ciphers:
            ctx.set_ciphers(self.ciphers)
        pool_kwargs['ssl_context'] = ctx
        return super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)

# --- TRANSFORMAÇÃO ---
def gerar_proposta_ia(imovel):
    bairro = imovel.get("bairro", "Excelente localização")
    tipo = imovel.get("tipo", "Imóvel")
    finalidade = imovel.get("finalidade", "Oportunidade")
    valor_raw = imovel.get("valor")
    
    try:
        if valor_raw:
            valor_fmt = f"R$ {float(valor_raw):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            valor_fmt = "sob consulta"
    except:
        valor_fmt = "sob consulta"

    return f"✨ Destaque: {tipo} para {finalidade} em {bairro}! Valor: {valor_fmt}. Não perca essa chance!"

def get_temp_token(session):
    headers = {"token-conta": TOKEN_FIXO}
    r = session.get(URL_TOKEN, headers=headers, timeout=30, verify=True)
    r.raise_for_status()
    return r.text.strip()

def baixar_dados(session, token_temp):
    offset = 0
    pagina = 1
    todos_imoveis = []
    
    print("⏳ Baixando imóveis (isso pode levar alguns minutos)...")
    
    while True:
        headers = {
            "Authorization": f"Bearer {token_temp}",
            "cpf_cnpj_empresa": CPF_CNPJ_EMPRESA,
            "limit": str(LIMIT),
            "token-conta": TOKEN_FIXO,
            "offset": str(offset)
        }
        r = session.get(URL_IMOVEIS, headers=headers, timeout=60, verify=True)
        r.raise_for_status()
        data = r.json()
        
        imoveis = data.get("imoveis", [])
        if not imoveis: 
            break
            
        todos_imoveis.extend(imoveis)
        
        # Esse print vai te mostrar que o código está vivo!
        print(f"📦 Página {pagina} processada... ({len(todos_imoveis)} imóveis acumulados)")
        
        offset += LIMIT
        pagina += 1
        
        if offset >= data.get("total", 0): 
            break
            
        time.sleep(0.1) # Pausa curta para não sobrecarregar a API
        
    return todos_imoveis