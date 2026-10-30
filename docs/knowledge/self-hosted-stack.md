# Stack self-hosted do SupportOps

Execute na raiz do lab, com Docker Desktop em modo Linux e os seis repositórios dentro de `projects/`:

```powershell
python scripts/stack.py checkout
python scripts/stack.py up
python scripts/stack.py status
```

`checkout` clona os projetos ausentes nas revisões registradas em `ops/stack/projects.lock.json`. Diretórios existentes são verificados e preservados. Você precisa ter acesso aos repositórios Git indicados nesse arquivo.

A primeira subida constrói as imagens, gera senhas e certificado e cria os bancos. O Keycloak pode demorar alguns minutos para importar o realm. O Compose espera os serviços necessários ficarem saudáveis.

## O que roda

P00 fornece os contratos e os dados de exemplo. P01 executa a orquestração e P02 aplica as regras das ferramentas; os três são bibliotecas instaladas na imagem do P05. O serviço `packages` verifica suas versões, hashes e um fluxo fake antes de liberar a aplicação. Ele terminar com código 0 é o resultado esperado.

P03 fornece a instrumentação, dashboards e alertas. P04 tem API e worker próprios. P05 tem API, worker e servidor MCP, com PostgreSQL/pgvector, Redis e filas locais. Cada aplicação usa usuário e banco próprios no PostgreSQL. O Keycloak usa um terceiro banco para manter usuários, sessões e configuração.

| Acesso | Endereço | Conta |
| --- | --- | --- |
| P05 Swagger | http://localhost:48000/docs | Token de `agent-a` ou `approver-a` |
| P04 Swagger | http://localhost:48004/docs | API técnica local sem autenticação |
| Keycloak | https://localhost:38443/admin/ | `lab-admin` |
| Grafana | http://localhost:43000 | `lab-admin` |
| Prometheus | http://localhost:49090 | Acesso local |
| Jaeger | http://localhost:46686 | Acesso local |

As portas publicadas aceitam conexões apenas da própria máquina. Os bancos, Redis, broker e MCP ficam na rede interna do Compose.

## Senhas, login e tokens

```powershell
python scripts/stack.py credentials
```

Esse comando mostra as senhas geradas para Keycloak, Grafana e usuários de exemplo. Elas ficam em volumes Docker, fora do Git. Evite salvar essa saída em logs de evidência ou publicar capturas de tela com os valores.

No Keycloak, entre como `lab-admin` e selecione o realm `supportops`. Há três usuários iniciais: `agent-a` e `approver-a` pertencem ao `tenant-a`; `agent-b` pertence ao `tenant-b`. O agente solicita a análise. O aprovador decide o reembolso. A API impede que o solicitante aprove a própria solicitação.

Para obter um token e testar no Swagger do P05:

```powershell
python scripts/stack.py token agent-a
```

Copie o token para o botão **Authorize** em `/docs`. Para aprovar, use um token de `approver-a`. O cliente `supportops-api` permite o grant de senha para esse roteiro local e também tem fluxo padrão habilitado. Uma aplicação de usuário deve usar Authorization Code com PKCE; esse lab não inclui uma interface de login própria.

O certificado HTTPS é assinado pela CA gerada no lab. Os containers validam essa CA automaticamente. Para exportar apenas o certificado público:

```powershell
python scripts/stack.py ca | Set-Content -Encoding ascii artifacts/stack-ca.crt
```

Você pode importar esse certificado no armazenamento de autoridades confiáveis do seu usuário para o navegador aceitar `https://localhost:38443`. A chave privada continua no volume Docker. A conta administrativa criada no bootstrap serve ao ambiente local; antes de expor uma instância pública, crie um administrador permanente e configure domínio/certificado públicos.

## Verificar o fluxo

```powershell
python scripts/stack.py check
```

A checagem cria dados de exemplo, autentica no Keycloak, envia tarefas ao P04 e ao P05, espera os workers, testa isolamento de tenants e aprovação humana. Depois revoga um token e exige HTTP 401 na API e no MCP. Também consulta métricas, dashboards e o trace distribuído. Ela usa apenas dados locais e modelo fake.

O snapshot de autorização dos jobs dura 15 minutos desde o aceite inicial. Uma aprovação depois do prazo recebe HTTP 409. O solicitante precisa reenviar a tarefa com autenticação atual e uma nova chave de idempotência. Revogar um token bloqueia novas chamadas da API/MCP; a execução já aceita segue a política desse prazo.

## Subir e derrubar com um comando

| | Local (Docker Compose) | Fly.io |
| --- | --- | --- |
| Subir | `python scripts/stack.py up` | `python scripts/stack.py fly-up` |
| Derrubar, mantendo dados | `python scripts/stack.py down` | `python scripts/stack.py fly-down` |
| Ver estado | `python scripts/stack.py status` | `python scripts/stack.py fly-status` |
| Derrubar, apagando dados | `python scripts/stack.py down --volumes` | `python scripts/stack.py fly-down -DestroyData -ConfirmDestroy supportops-lab` |
| Pré-visualizar | Não precisa; nada sai da máquina | Acrescente `-DryRun` |

Os dois lados têm as mesmas garantias. Cada um só mexe na própria aplicação: o Compose se limita ao projeto, e os comandos Fly recusam qualquer app fora de `ops/fly/stack-apps.ps1`. O `down` simples preserva os dados, em volumes nomeados no local e em volumes Fly na nuvem, e o Fly lista ao final cada volume preservado. Dados só somem com a flag explícita. Etapa com erro retorna exit code diferente de zero.

No local, `down` remove containers e redes desta aplicação. No Fly, `down` para todas as machines e desliga o autostart público, para que requisições externas não acordem o stack. O `fly-up` pode ser repetido: cria o que falta, publica de novo, inicia na ordem de dependência e espera a saúde dos serviços. Os comandos `fly-*` chamam `pwsh -File ops/fly/deploy.ps1 -Action Up|Down|Status`; `ops/fly/power.ps1 -Action Start|Stop|Status` retoma ou suspende machines sem deploy. Eles exigem `flyctl` e PowerShell 7, geram custo real e alteram um ambiente público, então só devem rodar com decisão explícita.

## Parar, retomar e consultar logs

```powershell
python scripts/stack.py logs api worker keycloak
python scripts/stack.py stop
python scripts/stack.py start
```

As senhas, CA e registros do PostgreSQL são reaproveitados. Reiniciar um container preserva seus volumes. `python scripts/stack.py down` também preserva volumes; `python scripts/stack.py down --volumes` apaga bancos e credenciais e deve ser tratado como reset destrutivo.

LocalStack emula SQS/SNS e não oferece persistência garantida nessa configuração. Aguarde os jobs terminarem antes de parar o broker. Resultados já concluídos permanecem no PostgreSQL. O Jaeger usa armazenamento de traces em memória; Grafana e Prometheus têm volumes próprios.

Para backup, guarde um dump dos bancos `p04`, `p05` e `keycloak` e os volumes de credenciais/CA correspondentes, mantendo o conjunto consistente. Um dump dos bancos sem as senhas originais não basta para reconstruir essa configuração. Mantenha backups de credenciais privados e criptografados.

## Portas e escopo

Copie `.env.example` para `.env` antes da primeira subida se precisar mudar portas. O issuer do Keycloak é `https://localhost:<LAB_IDP_PORT>/realms/supportops`. Após mudar a porta, execute novamente `python scripts/stack.py up` para atualizar a configuração gerada.

Os projetos mantêm repositórios independentes e dependências instaladas por wheel. O Compose da raiz precisa desses diretórios locais para construir as imagens. O IdP é uma instância self-hosted real; a aceitação aqui é local. Hospedagem pública com DNS, política de backup, filas de produção e interface de login é outra etapa. Avaliação de qualidade de modelo continua PENDING por decisão do projeto.

## Resposta de entrevista

**PT:** Centralizei a operação em um Compose, mantendo o código dos produtos independente. As bibliotecas entram por wheels com proveniência, e o Keycloak mantém identidade em PostgreSQL. A API verifica o token por introspection HTTPS, enquanto o worker usa uma delegação curta e um snapshot de autorização com prazo. Verifiquei revogação, isolamento e execução com serviços reais locais; os modelos continuam fake e as filas são emuladas.

**EN:** I consolidated local operations into one Compose application while preserving independent product repositories. Libraries enter through provenance-checked wheels, and Keycloak persists identity in PostgreSQL. The API introspects tokens over verified HTTPS; the worker uses short-lived delegation and a bounded authorization snapshot. Acceptance covers revocation, tenant isolation and real local service execution. Models remain fake and queues are emulated.
