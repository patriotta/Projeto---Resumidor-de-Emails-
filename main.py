import time
import os
from google.colab import userdata
from google import genai

# === CONFIGURAÇÃO DA API ===
def configurar_API():
  api_key = userdata.get('Gemini_API_KEY')
  os.environ['GOOGLE_API_KEY'] = api_key
  return genai.Client()

# === FUNÇÃO PARA RESUMIR EMAIL ===
def gerar_resumo(client, corpo_email, max_tentativas = 3):
  prompt = f"""Resuma o email recebido sem perder a ideia principal do corpo {corpo_email}"""

  for tentativa in range(max_tentativas):
    try:
      resposta = client.models.generate_content(
          model = 'gemini-2.5-flash',
          contents = prompt
      )
      return resposta.text.strip()

    except Exception as e:
      print(f"Erro ao resumir (tentativa {tentativa + 1}): {e}")
      time.sleep(2)

  return 'Não foi possível resumir o email'

# === PROCESSAR LISTA DE EMAILS ===
def processar_emails(client, caixa_de_entrada):
  resumos = []

  print('\n=== RESUMO DOS EMAILS ===')
  for email in caixa_de_entrada:
    resumo = gerar_resumo(client, email['corpo'])

    resultado = {
        'id': email['id'],
        'tipo': email['tipo'],
        'resumo': resumo

    }
    resumos.append(resultado)

    print(f"\n[ID: {email['id']}]  Tipo: {email['tipo']}")
    print(f"Resumo: {resumo}")
    print('-' * 50)

    # === DELAY PARA NÃO SOBRECARREGAR A API ===
    time.sleep(1)
  return resumos

# === SALVAR RESUMO EMAIL EM ARQUIVO .TXT ===
def salvar_arquivo_txt(emails_resumidos, nome_arquivo = 'resumos.txt'):
  with open(nome_arquivo, 'w', encoding = 'utf-8') as arquivo:
        for email in emails_resumidos:
            resumo_formatado = f"{email['id']} - {email['tipo']}: {email['resumo']}\n"
            arquivo.write(resumo_formatado)

# === EMAILS TESTE ===
emails_recebidos = [
    {"id": 1, "tipo": "Corporativo", "corpo": "Assunto: Reunião de Alinhamento\nOlá equipe, nossa reunião será amanhã às 10h."},
    {"id": 2, "tipo": "Marketing", "corpo": "Assunto: Ofertas\nDescontos de até 70% em toda a loja."},
    {"id": 3, "tipo": "Suporte", "corpo": "Assunto: Ticket\nSua solicitação foi processada com sucesso."}
]

# === EXECUÇÃO ===
def main():
    client = configurar_API()

    lista_emails_resumidos = processar_emails(client, emails_recebidos)

    salvar_arquivo_txt(lista_emails_resumidos)

    print("\nResumos salvos com sucesso!")


if __name__ == "__main__":
    main()