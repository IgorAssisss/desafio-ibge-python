"""
Created on Mon Jan 12 22:44:05 2026

@author: Assis
"""


import requests
import csv
import unicodedata
import json
from difflib import get_close_matches

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6ImR0TG03UVh1SkZPVDJwZEciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL215bnhsdWJ5a3lsbmNpbnR0Z2d1LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiIwMjQwYTU0Mi04YThhLTQ5NGQtOGI1OC1mMDE2NTgxYjY2OTEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY4Mjc1MzE0LCJpYXQiOjE3NjgyNzE3MTQsImVtYWlsIjoiaWdvci5zaWx2YTI1MTFAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6Imlnb3Iuc2lsdmEyNTExQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJub21lIjoiSWdvciBBc3NpcyBlIFNpbHZhIiwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiIwMjQwYTU0Mi04YThhLTQ5NGQtOGI1OC1mMDE2NTgxYjY2OTEifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc2ODI3MTcxNH1dLCJzZXNzaW9uX2lkIjoiYzhiYjkwYjMtYmQ0Zi00NmZkLWE3YzAtYzBlZDg2M2Y5YjliIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.Wch66do6CuQagTcQ93MxmzcA6UlRiN3sgR61guO1EW4" 

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc2MiOiJzdXBhYmFzZSIsInJvbGUiOiJhbm9uIiwiaWF0IjE1bnhsdWJ5a3lsbmNpbnR0Z2d1LlcpYXQiojE3NjUxODg2NzAsImV4cCI6MjA3NDY3MDU4MH0.Z-zqiD6_tjnF2WLU167z7jT5NzZaG72dWH0dpQW1N-Y"
URL_CORRECAO = "https://mynxlubykylncinttggu.functions.supabase.co/ibge-submit"


conteudo_input = """municipio,populacao
Niteroi,515317
Sao Gonçalo,1091737
Sao Paulo,12396372
Belo Horzionte,2530701
Florianopolis,516524
Santo Andre,723889
Santoo Andre,700000
Rio de Janeiro,6718903
Curitba,1963726
Brasilia,3094325"""

with open('input.csv', 'w', encoding='latin-1') as f:
    f.write(conteudo_input)
def normalizar(texto):
    """Remove acentos e padroniza o texto"""
    texto = str(texto).strip().lower()
    return "".join(c for c in unicodedata.normalize('NFD', texto) 
                   if unicodedata.category(c) != 'Mn')

try:
    resp = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")
    resp.raise_for_status()
    municipios_ibge = resp.json()
except Exception as e:
    print(f"Erro ao acessar API: {e}")
    municipios_ibge = []

mapa_ibge = {normalizar(m['nome']): m for m in municipios_ibge}
nomes_ibge_norm = list(mapa_ibge.keys())

resultados = []
stats = {
    "total_municipios": 0,
    "total_ok": 0,
    "total_nao_encontrado": 0,
    "total_erro_api": 0,
    "pop_total_ok": 0,
    "medias_por_regiao": {}
}

pop_por_regiao = {} 

with open('input.csv', mode='r', encoding='latin-1') as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        stats["total_municipios"] += 1
        m_input = linha['municipio']
        pop_input = int(linha['populacao'])
        m_norm = normalizar(m_input)
        
        match = get_close_matches(m_norm, nomes_ibge_norm, n=1, cutoff=0.8)
        
        status = "NAO_ENCONTRADO"
        dados = {"nome": "", "uf": "", "regiao": "", "id": ""}
        
        if match:
            status = "OK"
            stats["total_ok"] += 1
            stats["pop_total_ok"] += pop_input
            info = mapa_ibge[match[0]]
            
            dados = {
                "nome": info['nome'],
                "uf": info['microrregiao']['mesorregiao']['UF']['sigla'],
                "regiao": info['microrregiao']['mesorregiao']['UF']['regiao']['nome'],
                "id": info['id']
            }
            
            reg = dados["regiao"]
            if reg not in pop_por_regiao: pop_por_regiao[reg] = []
            pop_por_regiao[reg].append(pop_input)
        else:
            stats["total_nao_encontrado"] += 1

        resultados.append({
            "municipio_input": m_input,
            "populacao_input": pop_input,
            "municipio_ibge": dados["nome"],
            "uf": dados["uf"],
            "regiao": dados["regiao"],
            "id_ibge": dados["id"],
            "status": status
        })

for regiao, pops in pop_por_regiao.items():
    stats["medias_por_regiao"][regiao] = round(sum(pops) / len(pops), 2)

with open('resultado.csv', mode='w', newline='', encoding='utf-8-sig') as f:
    escritor = csv.DictWriter(f, fieldnames=resultados[0].keys(), delimiter=',')
    escritor.writeheader()
    escritor.writerows(resultados)

payload_final = {"stats": stats}

print("\n--- JSON PARA ENVIO ---")
print(json.dumps(payload_final, indent=2, ensure_ascii=False))

headers = {
    "Content-Type": "application/json",
    "apikey": API_KEY,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

print("\nEnviando para a API de correção")
envio = requests.post(URL_CORRECAO, json=payload_final, headers=headers)
print(f"Status do Envio: {envio.status_code} - Resposta: {envio.text}")
