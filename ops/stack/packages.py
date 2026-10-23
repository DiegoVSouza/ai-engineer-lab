"""Exercise installed portfolio packages without sibling source imports."""

import subprocess
import sys

from supportops_foundation.testkit.dataset import generate_dataset
from supportops_platform.agents.triage import run_fake_triage
from supportops_platform.contracts import Ticket
from supportops_platform.rag.retrieval import KnowledgeDocument, LocalRetriever
from supportops_toolkit.sample_tools import lookup_invoice

subprocess.run([sys.executable, 'scripts/verify_packages.py'], check=True)
dataset = generate_dataset(seed=42)
assert dataset.tickets and dataset.golden_cases
print('P00 seeded domain dataset: PASS')
assert lookup_invoice(invoice_id='inv-100')['status']=='paid'
print('P02 typed local tool: PASS')
retriever = LocalRetriever([KnowledgeDocument('invoice-policy','tenant-a','Invoice','Invoice billing support policy.')])
run = run_fake_triage(Ticket('tenant-a','customer-a','Invoice question','Please review my invoice.'),retriever)
assert run.result.trace and run.citations
print('P01 fake orchestration with P02 policies and P03 instrumentation: PASS')
