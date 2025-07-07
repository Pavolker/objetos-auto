import os
import re
import requests
import ast

# === CONFIGURAÇÕES ===
SUPABASE_URL = 'https://SEU-PROJETO.supabase.co'  # Altere para a URL do seu projeto
SUPABASE_API_KEY = 'SEU-API-KEY'  # Altere para sua API Key (service role de preferência)
TABELA = 'objetos_autoconhecimento'
PASTA_OBJETOS = 'objetos'

# === FUNÇÕES DE EXTRAÇÃO ===
def extrair_objeto_md(conteudo):
    # Regex para cada campo
    padroes = {
        'titulo': r'^# (.+)$',
        'nome_tecnico': r'\*\*Nome Técnico:\*\* (.+)',
        'foco_de_atencao': r'\*\*Foco de atenção:\*\* (.+)',
        'perspectiva': r'\*\*Perspectiva:\*\* (.+)',
        'descricao_expandida': r'## Descrição expandida\n(.+?)\n## Perguntas Reflexivas',
        'perguntas_reflexivas': r'## Perguntas Reflexivas\n((?:- .+\n)+)',
        'praticas_sugeridas': r'## Práticas sugeridas\n((?:- .+\n)+)',
        'fundamentacao_academica': r'## Fundamentação Acadêmica\n([\s\S]+)$',
    }
    dados = {}
    for campo, regex in padroes.items():
        m = re.search(regex, conteudo, re.MULTILINE)
        if m:
            if campo in ['perguntas_reflexivas', 'praticas_sugeridas']:
                # Extrai lista
                lista = [linha[2:].strip() for linha in m.group(1).split('\n') if linha.strip()]
                dados[campo] = lista
            else:
                dados[campo] = m.group(1).strip()
        else:
            dados[campo] = None
    return dados

# === FUNÇÃO DE ENVIO ===
def enviar_para_supabase(objeto):
    url = f"{SUPABASE_URL}/rest/v1/{TABELA}"
    headers = {
        'apikey': SUPABASE_API_KEY,
        'Authorization': f'Bearer {SUPABASE_API_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    # Ajusta campos para o formato correto
    payload = {
        'titulo': objeto['titulo'],
        'nome_tecnico': objeto['nome_tecnico'],
        'foco_de_atencao': objeto['foco_de_atencao'],
        'perspectiva': objeto['perspectiva'],
        'descricao_expandida': objeto['descricao_expandida'],
        'perguntas_reflexivas': objeto['perguntas_reflexivas'],
        'praticas_sugeridas': objeto['praticas_sugeridas'],
        'fundamentacao_academica': objeto['fundamentacao_academica'],
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code >= 200 and resp.status_code < 300:
        print(f"Sucesso: {payload['titulo']}")
    else:
        print(f"Erro ao enviar {payload['titulo']}: {resp.status_code} - {resp.text}")

# === MAIN ===
def main():
    arquivos = [f for f in os.listdir(PASTA_OBJETOS) if f.endswith('.md')]
    print(f"Encontrados {len(arquivos)} arquivos.")
    for arquivo in arquivos:
        caminho = os.path.join(PASTA_OBJETOS, arquivo)
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        objeto = extrair_objeto_md(conteudo)
        enviar_para_supabase(objeto)

if __name__ == '__main__':
    main() 