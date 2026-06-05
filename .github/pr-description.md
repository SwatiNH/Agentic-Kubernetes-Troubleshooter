.github/PULL_REQUEST_TEMPLATE.md
# Pull Request: Add Diagnostic Skills Framework

## 🎯 Overview

This PR introduces the core diagnostic skills framework for the Agentic Kubernetes Troubleshooter. These skills enable the agent to analyze different layers of Kubernetes infrastructure and identify issues, anomalies, and inefficiencies.

## 📋 Changes

### Skills Added

#### 1. **Compute Skill** (`skills/compute_skill.py`)
- **Purpose**: Analyzes CPU and memory resource utilization
- **Detects**:
  - Pod scheduling issues and unschedulable pods
  - Node health and conditions (memory pressure, disk pressure)
  - Crash loops, OOMKilled events, and excessive restarts
  - Resource constraint violations
  - Missing resource requests/limits
- **Key Methods**:
  - `analyze_node_health()` - Monitor node conditions
  - `analyze_pod_resources()` - Validate resource allocation
  - `analyze_scheduling_issues()` - Detect pending pods
  - `analyze_crashes_and_restarts()` - Track pod failures
  - `calculate_metrics()` - Aggregate cluster metrics

#### 2. **Storage Skill** (`skills/storage_skill.py`)
- **Purpose**: Analyzes persistent volumes, claims, and disk I/O
- **Detects**:
  - Unbound PersistentVolumeClaims (PVCs)
  - StorageClass misconfigurations
  - Low disk space on nodes or volumes
  - I/O performance degradation
  - Storage quota violations
  - Volume mount failures
- **Key Methods**:
  - `analyze_pvc_status()` - Check PVC binding and provisioning
  - `analyze_pv_status()` - Validate PV state
  - `analyze_storage_classes()` - Verify StorageClass config
  - `analyze_disk_usage()` - Monitor capacity and utilization
  - `calculate_metrics()` - Aggregate storage metrics

#### 3. **Network Skill** (`skills/network_skill.py`)
- **Purpose**: Analyzes service connectivity, DNS, and network policies
- **Detects**:
  - Service endpoints with no ready pods
  - DNS resolution failures (CoreDNS issues)
  - Network policy misconfigurations
  - Ingress routing problems
  - Service selector mismatches
  - Cluster IP allocation issues
  - Cross-namespace connectivity problems
- **Key Methods**:
  - `analyze_service_endpoints()` - Validate service connectivity
  - `analyze_dns_resolution()` - Check CoreDNS health
  - `analyze_network_policies()` - Verify policy enforcement
  - `analyze_ingress_routes()` - Validate ingress configuration
  - `calculate_metrics()` - Aggregate network metrics

#### 4. **Base Skill Interface** (`skills/base_skill.py`)
- **BaseSkill** - Abstract class defining the skill contract
  - `analyze()` - Execute skill analysis
  - `get_issues()` - Retrieve identified issues
  - `get_metrics()` - Get aggregated metrics
  - `filter_issues_by_severity()` - Filter by severity
  - `filter_issues_by_type()` - Filter by issue type
  - `get_issue_summary()` - Get severity distribution

- **SkillRegistry** - Manages available skills
  - `register()` - Register new skills
  - `get_skill()` - Look up by name
  - `get_skills_by_type()` - Get skills by category
  - `list_all_skills()` - Enumerate registered skills

- **SkillExecutor** - Executes skills with error handling
  - `execute_skill()` - Run single skill
  - `execute_all_skills()` - Run all skills
  - `execute_skills_by_type()` - Run skills by category
  - `aggregate_results()` - Combine results

- **IssueAggregator** - Processes issues from multiple skills
  - `deduplicate_issues()` - Remove duplicate issues
  - `prioritize_issues()` - Sort by severity and impact
  - `correlate_issues()` - Link related issues
  - `get_severity_distribution()` - Count by severity

#### 5. **Package Initialization** (`skills/__init__.py`)
- Exports main skill classes and utilities
- Enables clean imports: `from skills import BaseSkill, SkillRegistry`

## 🎯 Key Features

✅ **Modular Design** - Each skill operates independently  
✅ **Consistent Interface** - All skills implement BaseSkill contract  
✅ **Severity Classification** - Issues categorized as Critical/High/Medium/Low  
✅ **Metrics Collection** - Aggregates cluster-wide performance data  
✅ **Actionable Insights** - Provides recommendations for each issue  
✅ **Extensible Architecture** - Easy to add new skills  
✅ **Error Resilience** - Graceful degradation if API calls fail  

## 📊 Issue Detection Capabilities

### Compute Skill Detects:
- 🔴 **Critical**: Pod OOMKilled, node NotReady, unschedulable pods
- 🟠 **High**: Excessive restarts, CPU/memory constraints
- 🟡 **Medium**: Missing resource limits, unbalanced load
- 🟢 **Low**: Overprovisioning, suboptimal scheduling

### Storage Skill Detects:
- 🔴 **Critical**: Unbound PVCs, storage class not found
- 🟠 **High**: Low disk space (<10% remaining), I/O errors
- 🟡 **Medium**: Storage quota violations, slow I/O
- 🟢 **Low**: Underutilized volumes, fragmentation

### Network Skill Detects:
- 🔴 **Critical**: Services with no endpoints, CoreDNS down
- 🟠 **High**: DNS resolution failures, network policy blocks
- 🟡 **Medium**: Ingress misconfigurations, endpoint delays
- 🟢 **Low**: Unused services, routing inefficiencies

## 🔧 Data Models

### Issue Object
```python
{
    "id": "uuid",
    "type": "error_type",
    "severity": "critical|high|medium|low",
    "namespace": "namespace",
    "resource_name": "resource",
    "description": "Issue description",
    "affected_resources": ["pod1", "pod2"],
    "recommendations": ["Action 1", "Action 2"],
    "timestamp": "ISO8601"
}
```

### Metrics Object
```python
{
    "total_resources": 100,
    "healthy_resources": 95,
    "utilization_percent": 75.5,
    "timestamp": "ISO8601"
}
```

## 🚀 Usage Example

```python
from skills import BaseSkill, SkillRegistry, SkillExecutor
from skills.compute_skill import ComputeSkill
from skills.storage_skill import StorageSkill
from skills.network_skill import NetworkSkill

# Initialize registry
registry = SkillRegistry()

# Register skills
registry.register(ComputeSkill(k8s_client))
registry.register(StorageSkill(k8s_client))
registry.register(NetworkSkill(k8s_client))

# Execute all skills
executor = SkillExecutor(registry)
results = executor.execute_all_skills()

# Get aggregated results
aggregated = executor.aggregate_results()
print(f"Total issues: {aggregated['total_issues']}")
print(f"Critical: {len([i for i in aggregated['issues'] if i['severity']=='critical'])}")
```

## 🧪 Testing Approach

- Skills use placeholder implementations for Kubernetes API calls
- Can be tested with mock Kubernetes clients
- Support for integration testing with real clusters
- Custom analysis rules can be implemented per environment

## 📚 Documentation

- **agent.md** - Framework overview and architecture
- **STRUCTURE.md** - Project structure and file descriptions
- **Code Comments** - Comprehensive docstrings in all classes

## ✅ Checklist

- [x] Compute skill implementation with node/pod analysis
- [x] Storage skill implementation with PVC/PV analysis
- [x] Network skill implementation with service/DNS analysis
- [x] Base skill interface and utilities
- [x] Skill registry and executor
- [x] Issue aggregator with deduplication
- [x] Dataclass models for issues and metrics
- [x] Package initialization and exports
- [x] Comprehensive code documentation
- [x] Usage examples and patterns

## 🔗 Related Issues

Addresses: Build a skeleton Agentic framework with skills and agent.md file

## 📖 Next Steps

1. Implement actual Kubernetes API integration (replace placeholders)
2. Add metrics-server integration for real-time metrics
3. Create unit tests for each skill
4. Add configuration file support
5. Integrate with main agent orchestrator
6. Add webhook/notification support
