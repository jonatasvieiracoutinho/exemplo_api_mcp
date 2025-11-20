# Checklist de seguranca / industrializacao

Use esta lista antes de expor qualquer parte do projeto fora do laboratorio.

1. **HTTPS em todas as superficies**
   - Coloque API REST, frontend e MCP Server atras de proxy/gateway com TLS.

2. **Autenticacao e autorizacao**
   - Escolha o padrao da empresa (OAuth2/OIDC, API Gateway com API Key, JWT com provider interno).
   - Restrinja quem pode usar o MCP Server (rede privada, tokens, controle na IDE).

3. **Rate limiting, WAF e CORS**
   - Limite chamadas por IP/token.
   - Ative WAF ou filtros equivalentes.
   - Configure CORS apenas para dominios autorizados (nada de `*`).

4. **Segredos e configuracoes**
   - Guarde `DATABASE_URL`, tokens e chaves em Key Vault/secret manager.
   - Nao versione `.env`. Injete variaveis no runtime.

5. **Observabilidade**
   - Registre todas as chamadas (REST e MCP).
   - Ative metricas e traces para monitorar latencia/erros.

6. **Protecao de dados**
   - Planeje backup/restore do banco.
   - Criptografe dados em repouso (dependendo do banco escolhido).

7. **Processo de deploy**
   - Scripts `.bat` sao apenas para laboratorio; crie pipelines de deploy adequados (CI/CD, containers, IaC).

8. **Governanca das tools MCP**
   - Documente quem pode chamar cada tool.
   - Revise permissoes periodicamente.
   - Se as tools acessarem APIs externas, injete as chaves via Key Vault e nao devolva segredos ao cliente.

Este checklist e um ponto de partida. Adapte aos requisitos de compliance, privacidade e auditoria da sua organizacao.
