# Agentic Kubernetes Troubleshooter - Agent Framework

## Overview

The Agentic Kubernetes Troubleshooter is a multi-skill agent framework designed to automatically identify, analyze, and diagnose issues in Kubernetes clusters. The agent orchestrates specialized skills to examine different layers of the infrastructure and provide actionable insights.

## Agent Architecture

### Core Components

1. **Agent Orchestrator** (`agent.py`)
   - Central decision-making entity
   - Skill management and invocation
   - Result aggregation and reporting
   - Cluster scanning and issue prioritization

2. **Skills** - Specialized diagnostic modules
   - Compute Skill
   - Storage Skill
   - Network Skill

3. **Utilities** - Supporting infrastructure
   - Kubernetes API wrapper
   - Data models and types
   - Report generation

## Agent Workflow

```
┌─────────────────────────────────────────────────────┐
│         Agent: Cluster Troubleshooter               │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ Compute │  │ Storage │  │ Network │
   │  Skill  │  │  Skill  │  │  Skill  │
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        └────────────┼────────────┘
                     │
                ┌────▼────┐
                │ Analyzer│
                └────┬────┘
                     │
                ┌────▼─────────────────┐
                │ Priority Report      │
                │ - Critical Issues    │
                │ - Anomalies         │
                │ - Inefficiencies    │
                └─────────────────────┘
```

## Agent Responsibilities

### 1. Cluster Scanning
- Enumerate nodes, deployments, statefulsets, daemonsets
- Gather resource requests, limits, and actual usage
- Collect current pod states and events
- Monitor service endpoints and ingress configurations

### 2. Issue Detection
- Identify failed pods, pending pods, crash loops
- Detect resource constraints and bottlenecks
- Find configuration mismatches and errors
- Discover network connectivity problems

### 3. Anomaly Analysis
- Detect unusual resource consumption patterns
- Identify scaling issues and autoscaler problems
- Find health check failures
- Spot resource fragmentation

### 4. Efficiency Scoring
- Evaluate resource utilization
- Measure overprovisioning
- Assess workload distribution
- Calculate waste factors

### 5. Report Generation
- Prioritize issues by severity (Critical, High, Medium, Low)
- Provide remediation suggestions
- Generate detailed skill reports
- Create actionable insights

## Agent Initialization

```python
from agent import Agent

agent = Agent(kubeconfig_path="~/.kube/config")

# Run full cluster analysis
results = agent.scan_cluster()

# Get prioritized issues
issues = agent.get_priority_issues()

# Generate report
report = agent.generate_report()
print(report)
```

## Skill Specifications

### Compute Skill

**Purpose**: Analyze CPU and memory usage, pod scheduling, and node health

**Detects**:
- CPU throttling and OOMKilled pods
- Unschedulable pods (insufficient resources)
- Node disk pressure, memory pressure, PID pressure
- Pods without resource requests/limits
- Over-provisioned resources
- Unbalanced workload distribution

**Methods**:
- `analyze_pod_resources()` - Pod resource analysis
- `analyze_node_health()` - Node status and conditions
- `detect_scheduling_issues()` - Pending pod analysis
- `calculate_resource_utilization()` - Cluster resource metrics

**Output**:
```json
{
  "critical_issues": [
    {
      "type": "OOMKilled",
      "pod": "app-replica-1",
      "namespace": "production",
      "memory_limit": "512Mi",
      "severity": "critical"
    }
  ],
  "anomalies": [...],
  "recommendations": [...]
}
```

### Storage Skill

**Purpose**: Analyze persistent volumes, claims, and disk I/O

**Detects**:
- Unbound PersistentVolumeClaims (PVCs)
- Storage class misconfigurations
- Low disk space on nodes or volumes
- I/O performance degradation
- Storage quota violations
- Missing or failed volume mounts

**Methods**:
- `analyze_pvc_status()` - PVC binding and provisioning
- `analyze_storage_classes()` - Storage class configuration
- `analyze_disk_usage()` - Volume usage patterns
- `detect_io_issues()` - I/O performance analysis

**Output**:
```json
{
  "storage_issues": [
    {
      "type": "UnboundPVC",
      "pvc": "data-claim",
      "namespace": "database",
      "reason": "no storage class",
      "severity": "high"
    }
  ],
  "capacity_warnings": [...],
  "recommendations": [...]
}
```

### Network Skill

**Purpose**: Analyze service connectivity, DNS, and network policies

**Detects**:
- Service endpoint failures
- DNS resolution issues
- Network policy misconfigurations
- Ingress routing problems
- Service selector mismatches
- Port conflicts and binding issues
- Cluster IP allocation issues

**Methods**:
- `analyze_service_endpoints()` - Service connectivity
- `analyze_dns_resolution()` - DNS functionality
- `analyze_network_policies()` - Network policy enforcement
- `analyze_ingress_routes()` - Ingress configuration and routing
- `detect_connectivity_issues()` - Cross-pod communication

**Output**:
```json
{
  "connectivity_issues": [
    {
      "type": "NoReadyEndpoints",
      "service": "api-service",
      "namespace": "production",
      "selected_pods": 3,
      "ready_pods": 0,
      "severity": "critical"
    }
  ],
  "dns_issues": [...],
  "recommendations": [...]
}
```

## Issue Classification

### Severity Levels

- **Critical**: Cluster/workload unavailable, data at risk, cascading failures
- **High**: Significant performance degradation, potential data loss
- **Medium**: Configuration issues, resource constraints, reliability concerns
- **Low**: Optimization opportunities, best practice violations

### Issue Categories

1. **Errors** - Functional failures
   - Pod crashes and restart loops
   - Failed deployments
   - Service failures
   - Storage binding failures

2. **Anomalies** - Unexpected patterns
   - Unusual resource consumption
   - Unbalanced load distribution
   - Unexpected scale changes
   - Performance degradation

3. **Inefficiencies** - Suboptimal configurations
   - Missing resource limits
   - Overprovisioning
   - Unused resources
   - Suboptimal scheduling

## Agent Configuration

Create `config/agent_config.yaml`:

```yaml
kubeconfig: ~/.kube/config
namespaces:
  - all  # Scan all namespaces, or list specific ones
  
scan_settings:
  include_system_namespaces: false
  deep_analysis: true
  collect_metrics: true
  
thresholds:
  cpu_utilization_high: 80
  memory_utilization_high: 85
  disk_usage_high: 90
  node_pressure_check: true
  
report:
  severity_filter: "all"  # all, critical, high, medium, low
  include_recommendations: true
  output_format: "json"  # json, yaml, html
```

## Usage Examples

### Basic Cluster Scan
```python
from agent import Agent

agent = Agent()
results = agent.scan_cluster()
print(f"Found {len(results['issues'])} issues")
```

### Skill-Specific Analysis
```python
# Analyze only compute resources
compute_results = agent.skills['compute'].analyze()

# Analyze only storage
storage_results = agent.skills['storage'].analyze()

# Analyze only network
network_results = agent.skills['network'].analyze()
```

### Custom Issue Queries
```python
# Get only critical issues
critical = agent.get_issues_by_severity('critical')

# Get issues in specific namespace
ns_issues = agent.get_issues_by_namespace('production')

# Get specific issue type
compute_issues = agent.get_issues_by_type('compute')
```

### Generate Reports
```python
# Full detailed report
full_report = agent.generate_report(include_all=True)

# Executive summary
summary = agent.generate_summary()

# Export for external tools
agent.export_report('report.json', format='json')
```

## Data Models

### Issue Object
```python
{
    "id": "issue_uuid",
    "type": "compute|storage|network",
    "category": "error|anomaly|inefficiency",
    "severity": "critical|high|medium|low",
    "title": "Issue title",
    "description": "Detailed description",
    "affected_resources": ["namespace/resource"],
    "root_cause": "Analysis of root cause",
    "recommendations": ["Remediation steps"],
    "skill": "skill_name",
    "timestamp": "ISO8601",
    "metrics": {}
}
```

### Report Object
```python
{
    "timestamp": "ISO8601",
    "cluster_info": {...},
    "summary": {
        "total_issues": 42,
        "critical": 3,
        "high": 8,
        "medium": 15,
        "low": 16
    },
    "by_skill": {
        "compute": [...],
        "storage": [...],
        "network": [...]
    },
    "recommendations": [...],
    "metrics": {...}
}
```

## Integration Points

### Kubernetes API
- Uses `kubernetes` Python client
- Requires proper RBAC permissions
- Caches API responses for performance

### Metrics Collection
- Integrates with Prometheus/metrics-server
- Collects resource utilization data
- Analyzes historical trends

### External Tools
- Export results in standard formats (JSON, YAML)
- Webhook support for automation
- Integration with monitoring/alerting systems

## Extension Points

### Adding New Skills

1. Create skill file: `skills/new_skill.py`
2. Implement `BaseSkill` interface
3. Register with agent
4. Add configuration

### Custom Analysis Rules

Extend skill analysis methods to implement custom checks relevant to your environment.

### Integration Workflows

Chain agent results with remediation automation or external ticketing systems.

## Performance Considerations

- **Caching**: API responses cached to reduce Kubernetes API load
- **Batch Operations**: Cluster scan performed in parallel across namespaces
- **Incremental Updates**: Supports delta scanning for continuous monitoring
- **Resource Limits**: Configurable resource consumption for agent itself

## Error Handling

- Graceful degradation when APIs unavailable
- Detailed error logs and diagnostics
- Fallback analysis methods
- Report generation even with partial data

## Security Considerations

- RBAC: Agent requires read-only permissions on cluster resources
- Kubeconfig: Secure storage and access control
- Data: No sensitive data in logs or reports (optional redaction)
- Network: Optional: TLS for external integrations
