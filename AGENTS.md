# AGENTS.md — regras de atuação do AI Engineer Lab

Leia este arquivo primeiro. O lab é uma fábrica de projetos independentes de IA; `harness-kit/` é a fonte versionada do kit e cada diretório em `projects/` é um produto separado.

## Arquitetura do lab

O kit organiza quatro camadas: **Kit** (reutilizável e versionado), **Builder** (SDD, checks e estado de construção), **Product** (runtime, prompts, tools, evals e traces) e **Shared** (políticas, skills e contratos que o Builder e o Product reutilizam). O perfil `harness.yaml` de cada projeto é a fonte de verdade para ativar módulos.

Crie um projeto com:

```powershell
python scripts/harness/new-project.py <nome> --type <perfil>
```

Perfis disponíveis: `agent-app`, `mcp-server`, `rag-pipeline`, `workflow-automation`, `eval-infra`, `agent-saas` e `internal-agent`.

## Regras inegociáveis

1. **Intake e spec antes de código.** Todo projeto começa completando `harness.yaml`, `docs/harness/decisions.md` e uma fase com `SPEC.md` + `PLAN.md` + `VERIFY.md`. Exceção: modo rápido, registrado em `decisions.md`.
2. **Uma fonte de verdade por responsabilidade.** Perfil em `harness.yaml`; estado do builder em `docs/harness/`; contrato do agente em `agent-card.md`; execução e métricas em `artifacts/` do projeto.
3. **Posse de caminhos.** Cada plano declara `allowed_write_paths`. Não edite o kit ao implementar um produto. Alterações em `harness-kit/` exigem fase própria e validação em pelo menos dois projetos reais.
4. **Nada de “pronto” sem evidência.** Evidência é comando executado, exit code e saída salva em `artifacts/`. Sem isso, o resultado é `incomplete`.
5. **Números só de execuções reais.** Métricas, custos e benchmarks vêm de runs registrados. Sem run, use `PENDING`.
6. **Teste vermelho é sinal.** Corrija a causa raiz; não apague nem enfraqueça o teste para passar.
7. **Prompt e tool são código.** Prompts vivem em `agent/prompts/`, tools têm spec e teste de contrato, e toda mudança passa por regressão.
8. **Segredos fora do código.** Só `.env.example`; nunca commite chaves.
9. **Autorização para efeitos externos.** Não faça deploy real, publique, abra PR/merge, envie mensagem externa ou ultrapasse o orçamento configurado sem autorização explícita do usuário.
10. **Verifique, não presuma.** Confirme versões, flags e convenções atuais antes de depender delas; registre-as no projeto.

## Modos de LLM

`LLM_MODE=fake` é o padrão em testes e CI; `replay` usa cassettes; `live` usa provedor real dentro do orçamento. Lógica de controle deve ser testável em `fake`.

## Idiomas

- Código, comentários, commits, `README.md` e docs de portfólio: inglês.
- `README.pt-BR.md` e `docs/knowledge/**`: português, com respostas de entrevista nos dois idiomas.

## Fluxo por projeto

Cada projeto possui Git próprio; o Git do lab ignora `projects/`. Use a skill `lab-commits` em `harness/skills/lab-commits/SKILL.md` (instalada também em `.agents/skills/`). Toda tarefa concluída deve gerar commit local atômico `type(scope): imperative English description`, após validação e revisão do staged diff. Push continua exigindo autorização. Hooks `commit-msg` validam a sintaxe. Não use `--no-verify`.

`intake → sdd-plan → sdd-plan-check → sdd-execute → sdd-verify → sdd-gate → docs/knowledge`.

Use `harness/GSD-LITE-PLUS.md` para o processo SDD e `harness-kit-v2.1.md` para o desenho e critérios do kit. As specs `P00–P05` são currículo arquivado: podem inspirar projetos, mas não criam dependência entre projetos novos.
