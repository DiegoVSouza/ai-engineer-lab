# Programa produto primeiro

Em 2026-10-31 o foco do lab mudou de campanhas de avaliação para produto utilizável. Esta nota explica o que foi construído e o que ainda falta.

## O que existe agora

O SupportOps tem interface: o P06 é um console React servido por nginx. O navegador fala com o P05 pelo mesmo domínio, por `/api/`, então o P05 não ganhou superfície de CORS. O login usa Authorization Code com PKCE em um cliente público do Keycloak.

O contrato vem primeiro. O P06 guarda uma cópia fixada do `openapi.yaml` do P05 e gera o cliente TypeScript. Se o P05 mudar, `npm run contract:check` reprova até a cópia ser atualizada. Essa disciplina expôs duas lacunas reais: o aprovador não conseguia ver o valor do reembolso antes de decidir, e várias respostas não tinham tipo. O P05 ganhou `GET /v1/approvals` e modelos de resposta, sem alterar nenhum payload existente.

## Um comando para subir e derrubar

Local e Fly têm a mesma interface: `python scripts/stack.py up` e `down`, `fly-up` e `fly-down`. O Fly só aceita apps de um inventário único. `down` preserva dados e apagar exige flag explícita, com confirmação no Fly. Veja a tabela em [self-hosted-stack.md](self-hosted-stack.md).

## O que os testes ensinaram

- O e2e no navegador real achou um defeito que nenhum teste unitário pegaria: o worker usa os scopes de quem pediu, e o console não pedia `billing:read` e `crm:read`. A tarefa terminava em `worker_failure`.
- O ciclo real de `down` e `up` achou um vazamento: imagens com `VOLUME` deixam um volume anônimo órfão a cada `down`.
- A falha Git 128 do P00 era o limite de 260 caracteres do Windows no caminho do snapshot, não um defeito de produto.
- `--import-realm` ignora um realm existente, então o cliente do console é aplicado pela API de administração.

## O que ainda não está pronto

O sistema não está pronto para clientes reais. A lista concreta fica em [production-readiness.md](../harness/lab-stack/production-readiness.md). Qualidade de modelo, avaliação humana, holdout e promoção seguem adiados por decisão do usuário. O console no Fly nunca foi publicado.

## Resposta de entrevista

**PT:** Quando a plataforma ganhou interface, tratei o OpenAPI como fonte de verdade e gerei o cliente, então o desvio de contrato reprova o gate. Testar no navegador real contra o stack real achou um defeito de scopes que os testes unitários não pegavam, e um ciclo real de reinício achou um vazamento de volumes. Fechei com um checklist em que cada item tem comando e evidência, e o veredito honesto foi que ainda não está pronto para clientes reais, com oito bloqueios concretos.

**EN:** When the platform gained a UI, I treated OpenAPI as the source of truth and generated the client, so contract drift fails the gate. Testing in a real browser against the real stack found a scope defect that unit tests missed, and a real restart cycle found a volume leak. I finished with a checklist where every item has a command and evidence, and the honest verdict was not ready for real customers yet, with eight concrete blockers.
