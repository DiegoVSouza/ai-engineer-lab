# P04 — Mensageria e sistemas assíncronos

## Resumo de 1 página
A API só aceita e enfileira (202); workers executam tarefas longas de agente com checkpoint, retry, DLQ e idempotência. Derrubar um worker no meio da tarefa não duplica efeitos.

## Conceitos
- **At-least-once + idempotência ≈ exactly-once efetivo**: a fila pode entregar 2×; o efeito não pode ocorrer 2×. Chave de idempotência por tarefa/efeito, gravada na mesma transação do efeito.
- **Visibility timeout / heartbeat** (SQS): se o worker morre, a mensagem reaparece; tarefas longas precisam estender o timeout.
- **DLQ**: mensagens venenosas vão para análise após N tentativas; alarme na profundidade da DLQ.
- **Checkpoint**: persistir estado por passo para retomar sem refazer (e sem repetir chamadas LLM caras).
- **Outbox pattern**: gravar evento e mudança de estado na mesma transação, publicar depois — evita "gravou mas não publicou".
- **Saga**: compensações para ações multi-sistema (ex.: reembolso + notificação).
- **Backpressure**: limitar concorrência por worker/tenant; rate limits do provedor LLM.
- **SQS vs Kafka**: SQS = fila simples, gerenciada, sem replay; Kafka = log, replay, ordenação por partição, mais operação.

## Perguntas de entrevista
1. *How do you guarantee no duplicate refunds?* — Idempotency key + unique constraint + transactional outbox.
2. *Worker crashes mid-task — what happens?* — Visibility timeout expires, another worker claims, resumes from last checkpoint.
3. *SQS or Kafka for AI jobs?* — SQS for task queues; Kafka when you need event replay/streams/multiple consumers.
4. *How to handle rate-limited LLM providers?* — Concurrency caps, backoff with jitter, priority queues.
(≥6 adicionais após execução.)

## Números para citar
`PENDING`: tempo de recuperação após crash, throughput, taxa de DLQ.
