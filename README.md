# Miniprojeto de DevOps com IA generativa

Atividade da Unidade 5 do curso *Testes de Software Automatizados com Inteligência Artificial Generativa* (AKCIT). Um pipeline de CI no GitHub Actions roda os testes de uma aplicação Python e, quando eles falham num pull request, um agente de IA generativa lê o log e o diff, diagnostica a causa e comenta uma sugestão de correção no PR.

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `app.py` | `OrderService`: subtotal, frete com taxa administrativa e total do pedido |
| `test_app.py` | testes da aplicação (pytest) |
| `genai_analyst.py` | agente de diagnóstico: recorta o log, esconde segredos, chama a LLM e comenta no PR |
| `test_genai_analyst.py` | testes do próprio agente (máscara de segredos e recorte do log) |
| `.github/workflows/ci.yml` | pipeline com os jobs `unit_test` e `ai_debugger` |
| `requirements.txt` | dependências |

## Como o pipeline funciona

1. `unit_test` roda o pytest com `set -o pipefail` (para a falha não se perder no `tee`) e guarda o `pytest.log` como artefato, mesmo quando falha.
2. `ai_debugger` só roda quando `unit_test` falha num pull request. Ele baixa o log, gera o diff do PR e chama `genai_analyst.py`.
3. O agente envia à LLM só o trecho do log a partir das falhas, com tokens e chaves mascarados, e avisa no prompt que log e diff são dados não confiáveis. A resposta vira comentário no PR e resumo da execução.
4. Se a chave não estiver configurada ou o comentário falhar, o job falha de forma explícita.

A chamada usa a API compatível com a da OpenAI. Por padrão vai para o Gemini (`gemini-flash-latest`); para usar a OpenAI, basta criar as variáveis de repositório `OPENAI_BASE_URL` e `OPENAI_MODEL`.

## Configuração

Um único segredo em *Settings → Secrets and variables → Actions*: `OPENAI_API_KEY`. O comentário no PR usa o `GITHUB_TOKEN` que o próprio Actions fornece, com permissão `pull-requests: write` só no job do agente.

## Rodar localmente

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v 2>&1 | tee pytest.log
python genai_analyst.py --log pytest.log --diff pr.diff --dry-run   # mostra o que seria enviado à LLM
```
