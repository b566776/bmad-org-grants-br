# bmad-org-grants-br
Módulo BMAD v6 para análise de editais e redação de projetos para organizações (foco: Amigos da Vida)
Integração com install-custom e fluxo de uso
Criar o repositório https://github.com/SUA_ORG/bmad-org-grants-br.git com a estrutura acima.
​

Dentro de um projeto BMAD já instalado, rodar:

bash
npx bmad-method@alpha install-custom \
  --from git \
  --repo https://github.com/SUA_ORG/bmad-org-grants-br.git
Isso copia agents/, workflows/, memories/ e templates/ para _bmad/modules/bmad-org-grants-br.
​

Em seguida, rodar:

bash
npx bmad-method@alpha install
e escolher compilar todos os agentes para aplicar a customização (bmm-pm.customize.yaml).
​

No dia a dia:

Para um novo edital:

Criar .bmad-custom/memories/editais/<nome-do-edital>.md com resumo extraído do PDF.
​

Acionar o menu analisar-edital no agente para gerar resumo e checklist.
​

Acionar ideias-projeto para gerar ideias de projetos.
​

Usar o menu projeto-completo para preencher o TEMPLATE_PROJETO_EDITAL.md com o rascunho final.
