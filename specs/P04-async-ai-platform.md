# P04 — Plataforma assíncrona e eventos (Bloco 4)

## Objetivo
Desacoplar tarefas longas de IA da API, com resiliência, idempotência e deploy reproduzível.

## Entregáveis
- `projects/p04-async-platform/` com pacote `supportops_async`.
- `api/`: FastAPI com `POST /tasks` (202 + `task_id`, `Idempotency-Key`), `GET /tasks/{id}` (status, progresso, resultado), `POST /tasks/{id}/cancel`.
- `queue/`: abstração `Broker` com implementação **SQS/SNS (LocalStack)**; Kafka opcional como segunda implementação (ADR).
- `worker/`: consumo, visibility timeout/heartbeat, retries com backoff, **DLQ**, idempotência (tabela de chaves em Postgres), persistência de estado/checkpoint por passo, recuperação após crash.
- `events/`: SNS tópicos `task.created|completed|failed`, consumidor de exemplo.
- `infra/`: Dockerfiles multi-stage não-root, `docker-compose.async.yml`, Terraform (`plan` apenas) para SQS/SNS/IAM mínimo.
- `.github/workflows/p04.yml`: build, testes, build/push de imagem (push só com autorização), `terraform plan`.
- Worker executa um runner "fake" de agente de longa duração (stub até integração).

## Public API
```python
class Broker(Protocol): publish(msg), consume(), ack(handle), nack(handle, delay), dead_letter(handle)
class TaskStore(Protocol): create(task, idem_key), claim(id, worker), checkpoint(id, step, state), complete(id, result), fail(id, err)
POST /tasks -> 202 {task_id}; GET /tasks/{id} -> {status: queued|running|retrying|done|failed|cancelled, step, result?}
```

## Fases
- **001 api+store** (contrato HTTP, Postgres, idempotência na criação).
- **002 broker+worker** (SQS LocalStack, retries, DLQ).
- **003 durability** (checkpoint, crash recovery, idempotência de efeitos).
- **004 infra+cicd** (Docker, compose, Terraform plan, workflow).

## Verificação
- **Teste de crash**: matar worker no meio da tarefa → outra instância retoma do checkpoint; efeito colateral (ex.: reembolso simulado) ocorre **exatamente uma vez**.
- Mensagem duplicada entregue 2× → 1 efeito.
- Falha permanente → vai para DLQ após N tentativas; teste negativo.
- Mesma `Idempotency-Key` → mesmo `task_id`.
- `docker build` ok; `terraform validate/plan` ok sem credenciais reais (provider mock/LocalStack); CI verde.

## README exigido
Diagrama de sequência (Mermaid), semântica de entrega (at-least-once + idempotência), como derrubar um worker e ver a recuperação, estados da tarefa, passos de deploy (e o que exige autorização).

## Documentação de conhecimento
`docs/knowledge/P04-async.md`: at-least-once vs exactly-once, idempotência, DLQ, visibility timeout, SQS vs Kafka, outbox pattern, saga, backpressure, trade-offs de filas em sistemas de IA.

## Fora de escopo
Deploy real na AWS (precisa autorização), auth, RAG, tracing avançado.
