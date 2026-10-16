# F9 — independent DynamoDB trusted-head backend (candidate, NOT deployed)

## Implementation and author/authority split

- The user is the **original Meu Artigo creator and researcher**: article design,
  research methods, scientific requirements, human validation and decisions
  about authorizing cloud providers, IAM, paid infrastructure and production.
- The assistant authored the optional \`scripts/drive_f9_dynamo_head.py\`,
  \`tests/test_drive_f9_dynamo_head.py\`, this runbook and related engineering
  notes in a **Draft PR**. The code is not an assertion of scientific efficacy
  or independent engineering certification.
- CI demonstrates deterministic mock tests only. AWS infrastructure, paid
  services, security permissions and account resources were **not created**.
  No real Drive folder creation or journal restoration was performed.

## Design

A separately authorized executor may use the optional boto3 DynamoDB low-level
client as a backend implementing the F8 \`read_head\` /
\`compare_and_set(previous,new)\` contract.

Provisioning is an **out-of-band, explicitly approved administrator task**.
The table must have a single string partition key \`ProjectKey\`, and each
authorized project must have **exactly one pre-existing item** containing
\`HeadSha256\` (lowercase 64-digit SHA-256 of the latest confirmed F7 receipt).
Do not silently create a missing item or replace an unknown existing head.

For every project, construct the exact partition-key string using
`drive_f9_dynamo_head.scoped_key(plan, audit_parent_id, audit_file_id)`.
This hashes the canonical delivery plan and separately provisioned audit
parent/file IDs into a deterministic `ma-f9-` scope. A changed plan, remote
file ID or audit parent produces a different key and cannot silently reuse
the old trusted head. Provision the exact new record independently and do
not bootstrap it from unverified remote data.

The adapter implements:

- \`GetItem(ConsistentRead=True)\` with an exact scoped project key, and
  rejects missing, corrupt or malformed records.
- \`UpdateItem\` with condition
  \`attribute_exists(ProjectKey) AND HeadSha256 = previous_head\`,
  sets the new digest and requests \`ReturnValues=ALL_NEW\`.
- Treats exactly \`ConditionalCheckFailedException\` as a concurrency conflict
  (false). A timeout, permission denial, partial reply, throttling or unknown
  response is **unverified**, never interpreted as successful.
- The F8 caller still issues a fresh strongly consistent read and compares the
  exact new head. This is required even if the update returned attributes.

Use IAM policies scoped to the specific table and authorized project key;
require encryption, audit logs and retention appropriate to the organization.
The archive holding the HMAC receipts and HMAC secret must remain independent
of the trusted-head store and of any scientific manuscript data.

No secure initialization command is provided here: bootstrapping the first
trusted digest needs prior verification of the F7 initial receipt, audit
authority approval and external immutability expectations.

## Limitations

DynamoDB conditional updates can provide per-item concurrency control **if**
the real table and permissions are configured correctly. This is not a
transaction spanning Google Drive folder creation, Drive journal PATCH and
a DynamoDB record. A successful conditional write in AWS is not a guarantee
that another service committed its own write. Network partitions, writer
collusion, obsolete clients and operator misconfiguration remain risks.

The default \`drive_f5_operator.py\` CLI still has **no enabled real trusted
backend loader**, and thus does not issue synthetic folder POST requests even
when the create flag is specified. Do not inject an in-memory mock as if it
were a real production-authoritative store.

Reference docs for exact provider behavior:
https://docs.aws.amazon.com/boto3/latest/reference/services/dynamodb/client/update_item.html
https://docs.aws.amazon.com/boto3/latest/reference/services/dynamodb/table/get_item.html

## Acceptance remaining

1. Human review and approval for cost, tenancy and IAM scopes.
2. Provision an independent isolated synthetic table and pre-existing key,
   recorded outside research projects.
3. Test two genuinely independent authorized executors racing on the same
   \`previous_head\`: exactly one update may succeed.
4. Verify strongly consistent cross-executor readback after process restart
   and after ambiguous network response.
5. Wire an explicitly reviewed real backend loader to the synthetic-only F5
   host with the F7 HMAC archive and authorized Drive OAuth.
6. Independently verify provider-all-types pagination, journal readback and
   one fault-injected create; do not test on a real manuscript corpus.
7. Separate maintainer approval for merge, release and installed update.

Status: **CODE CANDIDATE — NOT LIVE-ACCEPTED**.
